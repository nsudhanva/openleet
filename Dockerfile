# syntax=docker/dockerfile:1
# Local development only, for machines that are not Linux: the judge needs Linux (/proc,
# setuid, rlimits), so it runs here while the server runs natively and connects over TCP:
#   docker compose up -d judge
#   JUDGE_SOCKET=tcp://127.0.0.1:7777 cargo run -p openleet
# Production runs both natively under systemd (see deploy/).

FROM rust:1.99-slim-trixie AS build
WORKDIR /src
COPY Cargo.toml Cargo.lock ./
COPY proto proto
COPY judge judge
# Only the judge is built here; the server's crate stays out of this image.
RUN sed -i 's/members = \[.*\]/members = ["judge", "proto"]/' Cargo.toml \
	&& cargo build --release -p openleet-judge

FROM python:3.15-slim-trixie AS judge
RUN pip install --no-cache-dir --root-user-action=ignore sortedcontainers==2.4.0
COPY --from=build /src/target/release/openleet-judge /usr/local/bin/openleet-judge
COPY judge/py /opt/judge
ENV JUDGE_ZYGOTE=/opt/judge/zygote.py JUDGE_PYTHON=/usr/local/bin/python3 \
	JUDGE_SOCKET=tcp://0.0.0.0:7777 PYTHONDONTWRITEBYTECODE=1
CMD ["openleet-judge"]
