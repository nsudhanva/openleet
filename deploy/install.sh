#!/bin/sh
# Sets up a fresh Ubuntu server for openleet (run once as root):
#   sudo deploy/install.sh    then fill in /etc/openleet.env and run /opt/openleet/update.sh
# With --units-only (update.sh runs it from each release), it only refreshes the systemd units,
# the update script and the judge's Python packages.
set -eu
ROOT=/opt/openleet
ENV_FILE=/etc/openleet.env
UNIT_DIR=/etc/systemd/system
HERE=$(cd "$(dirname "$0")" && pwd)
PYTHON=3.15
# The installer at a fixed version's URL, not the moving latest one.
UV_VERSION=0.13.7

# Every openleet* file next to this script is a unit; the ones with an [Install] section get
# enabled, and sockets, timers and path units started.
install_units() {
	changed=0
	# Units an earlier release installed but this one no longer ships.
	for path in "$UNIT_DIR"/openleet*; do
		[ -e "$path" ] || continue
		unit=${path##*/}
		[ -e "$HERE/$unit" ] && continue
		systemctl disable --now --quiet "$unit" || true
		rm -f "$path"
		changed=1
	done
	for path in "$HERE"/openleet*; do
		unit=${path##*/}
		if ! cmp -s "$path" "$UNIT_DIR/$unit"; then
			install -m 0644 "$path" "$UNIT_DIR/$unit"
			changed=1
		fi
	done
	install -m 0755 "$HERE/update.sh" "$ROOT/update.sh"
	if [ "$changed" = 1 ]; then systemctl daemon-reload; fi
	# Idempotent, so a release that adds a unit enables it too; sockets, timers and path units
	# start now.
	for path in "$HERE"/openleet*; do
		unit=${path##*/}
		grep -q '^\[Install\]' "$path" || continue
		systemctl enable --quiet "$unit"
		case "$unit" in *.timer | *.path | *.socket) systemctl start "$unit" ;; esac
	done
}

# The judge's Python packages, pinned with hashes in judge/py/requirements.txt (exported from
# pyproject.toml). Releases carry that file, so a version change deploys itself like the units;
# a bare copy of deploy/ does not, and the first update.sh installs them instead.
install_judge_packages() {
	requirements="$HERE/../judge/py/requirements.txt"
	if [ -f "$requirements" ]; then
		uv pip sync --quiet --python "$ROOT/venv/bin/python" --require-hashes "$requirements"
		chmod -R a+rX "$ROOT/venv"
	fi
}

if [ "${1:-}" = "--units-only" ]; then
	install_units
	install_judge_packages
	exit 0
fi

apt-get update -qq
apt-get install -y --no-install-recommends curl jq zstd ca-certificates >/dev/null
id openleet >/dev/null 2>&1 || useradd --system --home-dir /var/lib/openleet --shell /usr/sbin/nologin openleet
mkdir -p "$ROOT/releases"

# Python for submissions: a uv-managed CPython, world-readable so the sandbox user can run it.
if ! command -v uv >/dev/null; then
	curl -LsSf "https://astral.sh/uv/$UV_VERSION/install.sh" | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh
fi
export UV_PYTHON_INSTALL_DIR="$ROOT/python"
uv python install "$PYTHON"
uv venv --allow-existing --python "$PYTHON" "$ROOT/venv"
chmod -R a+rX "$ROOT/python" "$ROOT/venv"
install_judge_packages

if [ ! -f "$ENV_FILE" ]; then
	cat >"$ENV_FILE" <<'ENV'
# The site's domain (HTTPS certificate is automatic), or http://host for plain HTTP.
SITE_ADDRESS=openleet.example.com
# Day boundaries for streaks, such as America/Los_Angeles.
TZ=UTC
# How much slower this machine runs Python than the one that measured reference times.
JUDGE_CPU_SCALE=2.5
# Shared with the GitHub secret DEPLOY_SECRET; CI signs its deploy requests with it.
DEPLOY_SECRET=
ENV
	chmod 0640 "$ENV_FILE"
	chgrp openleet "$ENV_FILE"
fi

# Submissions have no use for io_uring, a common kernel attack surface.
echo "kernel.io_uring_disabled = 2" >/etc/sysctl.d/90-openleet.conf
sysctl -q --system

install_units
echo "Fill in $ENV_FILE, then run $ROOT/update.sh"
