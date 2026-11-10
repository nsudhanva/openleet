#!/bin/sh
# Sets up a fresh Ubuntu server for google-cards (run once as root), or, with --units-only,
# refreshes the systemd units and the update script from an unpacked release.
#   sudo ./install.sh            then edit /etc/google-cards.env and run update.sh
set -eu
ROOT=/opt/google-cards
HERE=$(cd "$(dirname "$0")" && pwd)
PYTHON=3.15

units() {
	changed=0
	for unit in google-cards.service google-judge.service google-cards-update.service google-cards-update.timer; do
		if ! cmp -s "$HERE/$unit" "/etc/systemd/system/$unit"; then
			install -m 0644 "$HERE/$unit" "/etc/systemd/system/$unit"
			changed=1
		fi
	done
	install -m 0755 "$HERE/update.sh" "$ROOT/update.sh"
	if [ "$changed" = 1 ]; then systemctl daemon-reload; fi
}

if [ "${1:-}" = "--units-only" ]; then
	units
	exit 0
fi

apt-get install -y --no-install-recommends curl zstd ca-certificates >/dev/null
id cards >/dev/null 2>&1 || useradd --system --home-dir /var/lib/google-cards --shell /usr/sbin/nologin cards
mkdir -p "$ROOT/releases"

# Python for submissions: a uv-managed CPython, world-readable so the sandbox user can run it.
if ! command -v uv >/dev/null; then
	curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh
fi
export UV_PYTHON_INSTALL_DIR="$ROOT/python"
uv python install "$PYTHON"
uv venv --allow-existing --python "$PYTHON" "$ROOT/venv"
uv pip install --python "$ROOT/venv/bin/python" sortedcontainers==2.4.0
chmod -R a+rX "$ROOT/python" "$ROOT/venv"

if [ ! -f /etc/google-cards.env ]; then
	cat >/etc/google-cards.env <<'ENV'
# The site's domain (HTTPS certificate is automatic), or http://host for plain HTTP.
SITE_ADDRESS=google.example.com
# Day boundaries for streaks, such as America/Los_Angeles.
TZ=UTC
# How much slower this machine runs Python than the one that measured reference times.
JUDGE_CPU_SCALE=2.5
ENV
	chmod 0640 /etc/google-cards.env
	chgrp cards /etc/google-cards.env
fi

units
systemctl enable google-cards.service google-judge.service google-cards-update.timer
systemctl start google-cards-update.timer
echo "Edit /etc/google-cards.env, then run $ROOT/update.sh"
