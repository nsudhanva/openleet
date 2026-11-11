# syntax=docker/dockerfile:1
# Two images for running OpenLeet in Docker (docker-compose.yml): production runs natively under
# systemd instead (deploy/).
#   app    the server, a fully static musl binary with the web app embedded, plus the data,
#          on an empty base (no shell, no libc)
#   judge  the judge daemon (static) and the Python zygote on a trimmed python:slim
# Both binaries are built natively for the build machine's architecture (amd64 or arm64).

ARG RUST=1.99
ARG PYTHON=3.15
ARG BUN=1.4
ARG ALPINE=3.24

# Web app
FROM oven/bun:${BUN}-alpine AS web
WORKDIR /src
COPY package.json bun.lock ./
COPY web/package.json web/
RUN --mount=type=cache,target=/root/.bun/install/cache \
	bun install --frozen-lockfile --ignore-scripts
COPY web web
RUN bun run build

# Rust: dependencies cached apart from the code (cargo-chef)
# Alpine's toolchain targets musl, and Rust links musl binaries statically by default
# (crt-static is on; setting it in RUSTFLAGS would also hit proc-macros, which cannot be static).
# g++ builds DuckDB's bundled C++ and links libstdc++ statically into it. assert-static checks.
# JOBS caps parallel compiles: DuckDB's C++ takes up to ~1 GB per compiler process.
FROM rust:${RUST}-alpine AS chef
RUN apk add --no-cache g++ make cmake perl linux-headers \
	&& cargo install --locked cargo-chef@0.1.78 \
	&& rm -rf /usr/local/cargo/registry
ENV CARGO_TERM_COLOR=never
WORKDIR /src

FROM chef AS planner
COPY Cargo.toml Cargo.lock ./
COPY proto proto
COPY server server
COPY judge/Cargo.toml judge/
COPY judge/src judge/src
RUN cargo chef prepare --recipe-path recipe.json

# Fails the build unless the binary is static: no program interpreter, no shared libraries.
FROM chef AS static
RUN printf '%s\n' '#!/bin/sh' 'set -eu' 'for f; do' \
	'  if readelf -lW "$f" | grep -q "program interpreter" || readelf -dW "$f" | grep -q NEEDED; then' \
	'    echo "$f is not static" >&2; exit 1; fi' \
	'  echo "$f: static, $(du -h "$f" | cut -f1)"' 'done' >/usr/local/bin/assert-static \
	&& chmod +x /usr/local/bin/assert-static

FROM static AS judge-build
COPY --from=planner /src/recipe.json .
ARG JOBS
RUN cargo chef cook --release --locked ${JOBS:+--jobs $JOBS} -p openleet-judge --recipe-path recipe.json
# Every member's real manifest: the cooked skeleton's have masked versions.
COPY Cargo.toml Cargo.lock ./
COPY server/Cargo.toml server/
COPY proto proto
COPY judge/Cargo.toml judge/
COPY judge/src judge/src
RUN cargo build --release --locked ${JOBS:+--jobs $JOBS} -p openleet-judge \
	&& assert-static target/release/openleet-judge

FROM static AS app-build
COPY --from=planner /src/recipe.json .
ARG JOBS
RUN cargo chef cook --release --locked ${JOBS:+--jobs $JOBS} -p openleet --recipe-path recipe.json
COPY Cargo.toml Cargo.lock ./
COPY judge/Cargo.toml judge/
COPY proto proto
COPY server server
COPY --from=web /src/web/dist web/dist
RUN cargo build --release --locked ${JOBS:+--jobs $JOBS} -p openleet \
	&& assert-static target/release/openleet

# App files: test corpus, time zones, user
FROM alpine:${ALPINE} AS files
# tests.duckdb is a release asset; data/judge/corpus.json names its repository, name and sha256.
RUN --mount=type=bind,source=data/judge/corpus.json,target=/corpus.json \
	set -eu; \
	field() { sed -n "s/.*\"$1\": *\"\([^\"]*\)\".*/\1/p" /corpus.json; }; \
	mkdir -p /rootfs/app/data/judge /rootfs/etc /rootfs/state; \
	wget -q -O /rootfs/app/data/judge/tests.duckdb \
		"https://github.com/$(field repository)/releases/download/corpus/$(field asset)"; \
	echo "$(field sha256)  /rootfs/app/data/judge/tests.duckdb" | sha256sum -c -
RUN set -eu; \
	apk add --no-cache tzdata; \
	mkdir -p /rootfs/usr/share; cp -r /usr/share/zoneinfo /rootfs/usr/share/; \
	echo 'openleet:x:10001:10001::/state:/sbin/nologin' >/rootfs/etc/passwd; \
	echo 'openleet:x:10001:' >/rootfs/etc/group; \
	chown 10001:10001 /rootfs/state

FROM alpine:${ALPINE} AS revision
# The commit, for GET /api/version (the server reads DATA_DIR/../REVISION).
ARG REVISION=dev
RUN echo "$REVISION" >/REVISION

# App image
FROM scratch AS app
COPY --from=files /rootfs /
COPY data/problems.json data/approaches.json /app/data/
COPY data/judge/specs.json /app/data/judge/
COPY --from=revision /REVISION /app/REVISION
COPY --from=app-build /src/target/release/openleet /usr/local/bin/openleet
ENV DATA_DIR=/app/data STATE_DIR=/state HTTP_PORT=8080 SITE_ADDRESS=http://openleet.localhost \
	JUDGE_SOCKET=/run/openleet-judge/judge.sock
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --start-interval=1s \
	CMD ["/usr/local/bin/openleet", "health"]
ENTRYPOINT ["/usr/local/bin/openleet"]

# Judge image
# Trimmed python:slim (no pip, apt, docs, IDLE, Tk or headers), then squashed into one layer.
# glibc, as in production: on musl, CPython assumes a 1 MB C stack for every thread, so recursion
# through C code (a function under @cache) overflows at a depth of about 5,000. The imports the
# zygote makes are precompiled: the root file system is read-only at run time.
FROM python:${PYTHON}-slim AS judge-root
COPY judge/py/requirements.txt /tmp/requirements.txt
RUN set -eu; \
	pip install --no-cache-dir --root-user-action=ignore -r /tmp/requirements.txt; \
	pip uninstall -y --root-user-action=ignore pip; \
	lib=$(python -c 'import sysconfig; print(sysconfig.get_path("stdlib"))'); \
	rm -rf /tmp/requirements.txt "$lib"/ensurepip "$lib"/idlelib "$lib"/tkinter "$lib"/turtledemo \
		"$lib"/turtle.py "$lib"/pydoc_data "$lib"/config-* /usr/local/include /usr/local/bin/idle* \
		/usr/local/bin/pydoc* /usr/local/share /usr/share/doc /usr/share/man /usr/share/info \
		/usr/share/locale /usr/bin/apt* /usr/lib/apt /etc/apt /var/lib/apt /var/cache/* /var/log/*; \
	mkdir -p /run/openleet-judge
COPY judge/py /opt/openleet/judge/py
RUN set -eu; \
	python -m compileall -q -j0 /opt/openleet/judge/py; \
	cd /opt/openleet/judge/py; \
	python -I -c 'import sys, py_compile; sys.path[:0] = [".", "gen"]; import harness, prelude, zygote; [py_compile.compile(m.__file__, quiet=1) for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith(".py")]'
COPY --from=judge-build /src/target/release/openleet-judge /usr/local/bin/openleet-judge

FROM scratch AS judge
COPY --from=judge-root / /
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin LANG=C.UTF-8 \
	JUDGE_PYTHON=/usr/local/bin/python3 JUDGE_ZYGOTE=/opt/openleet/judge/py/zygote.py \
	JUDGE_SOCKET=/run/openleet-judge/judge.sock PYTHONDONTWRITEBYTECODE=1
# Root only inside the container, so the zygote can drop each submission to uid 61000.
CMD ["openleet-judge"]
