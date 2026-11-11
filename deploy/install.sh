#!/bin/sh
# Sets up an Ubuntu server for openleet and starts it, from a clone of the repository:
#   sudo SITE_ADDRESS=openleet.example.com deploy/install.sh
# Optional: TZ (day boundaries for streaks, default UTC) and DEPLOY_SECRET (CI's deploy
# requests). The values go to /etc/openleet.env; running it again keeps that file's values
# unless new ones are given. Releases come from the GitHub repository the clone came from.
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

[ "$(id -u)" = 0 ] || {
	echo "run as root: sudo SITE_ADDRESS=openleet.example.com $0" >&2
	exit 1
}
if [ -z "${SITE_ADDRESS:-}" ] && ! grep -q '^SITE_ADDRESS=.' "$ENV_FILE" 2>/dev/null; then
	echo "set the site's domain: sudo SITE_ADDRESS=openleet.example.com $0" >&2
	echo "(or SITE_ADDRESS=http://HOST for plain HTTP without a certificate)" >&2
	exit 1
fi
# The GitHub repository whose releases this server installs: the clone's origin.
repository=$(git -c safe.directory='*' -C "$HERE" remote get-url origin 2>/dev/null |
	sed -n 's#^.*github\.com[:/]\([^/]*/[^/]*\)$#\1#p' | sed 's/\.git$//')

apt-get update -qq
apt-get install -y --no-install-recommends curl jq zstd ca-certificates >/dev/null
id openleet >/dev/null 2>&1 || useradd --system --home-dir /var/lib/openleet --shell /usr/sbin/nologin openleet
mkdir -p "$ROOT/releases"

# Python for submissions: a uv-managed CPython, world-readable so the sandbox user can run it.
if ! command -v uv >/dev/null; then
	curl -LsSf "https://astral.sh/uv/$UV_VERSION/install.sh" | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh
fi
export UV_PYTHON_INSTALL_DIR="$ROOT/python"
uv python install --no-bin "$PYTHON"
uv venv --allow-existing --python "$PYTHON" "$ROOT/venv"
chmod -R a+rX "$ROOT/python" "$ROOT/venv"
install_judge_packages

if [ ! -f "$ENV_FILE" ]; then
	cat >"$ENV_FILE" <<'ENV'
# The site's domain (HTTPS certificate is automatic), or http://host for plain HTTP.
SITE_ADDRESS=
# Day boundaries for streaks, such as America/Los_Angeles.
TZ=UTC
# Shared with the GitHub secret DEPLOY_SECRET; CI signs its deploy requests with it.
DEPLOY_SECRET=
# The GitHub repository (owner/name) whose "edge" release update.sh installs.
OPENLEET_REPO=nsudhanva/openleet
ENV
fi
chmod 0640 "$ENV_FILE"
chgrp openleet "$ENV_FILE"
# Sets KEY=VALUE in the env file, replacing the line in place or adding it.
set_env() {
	if grep -q "^$1=" "$ENV_FILE"; then
		K=$1 V=$2 awk 'index($0, ENVIRON["K"] "=") == 1 { print ENVIRON["K"] "=" ENVIRON["V"]; next } { print }' \
			"$ENV_FILE" >"$ENV_FILE.new"
	else
		cp "$ENV_FILE" "$ENV_FILE.new"
		printf '%s=%s\n' "$1" "$2" >>"$ENV_FILE.new"
	fi
	chmod 0640 "$ENV_FILE.new"
	chgrp openleet "$ENV_FILE.new"
	mv "$ENV_FILE.new" "$ENV_FILE"
}
if [ -n "${SITE_ADDRESS:-}" ]; then set_env SITE_ADDRESS "$SITE_ADDRESS"; fi
if [ -n "${TZ:-}" ]; then set_env TZ "$TZ"; fi
if [ -n "${DEPLOY_SECRET:-}" ]; then set_env DEPLOY_SECRET "$DEPLOY_SECRET"; fi
if [ -n "$repository" ]; then set_env OPENLEET_REPO "$repository"; fi

# Submissions have no use for io_uring, a common kernel attack surface.
echo "kernel.io_uring_disabled = 2" >/etc/sysctl.d/90-openleet.conf
sysctl -q --system

# 1 GB of swap for the rest of a 1 GB machine (apt, the update's unpacking); the judge never
# swaps (MemorySwapMax=0 in openleet-judge.service).
if [ -z "$(swapon --show --noheadings)" ]; then
	fallocate -l 1G /swapfile
	chmod 0600 /swapfile
	mkswap /swapfile >/dev/null
	swapon /swapfile
fi
if [ -f /swapfile ] && ! grep -q '^/swapfile ' /etc/fstab; then
	echo '/swapfile none swap sw 0 0' >>/etc/fstab
fi

# Ubuntu's unattended-upgrades installs security updates daily; one that needs a reboot (a new
# kernel) reboots the machine at the next 10:00 machine time (UTC on GCP). Every unit starts
# again at boot.
cat >/etc/apt/apt.conf.d/52openleet-reboot <<'APT'
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "10:00";
APT

# The update script installs the newest release, its units (which start the timers) and starts
# the services; the units come from the release, so none run before the env file is complete.
install -m 0755 "$HERE/update.sh" "$ROOT/update.sh"
before=$(readlink -f "$ROOT/current" 2>/dev/null || true)
"$ROOT/update.sh"
# Already up to date: restart anyway, so changed settings take effect.
if [ "$(readlink -f "$ROOT/current")" = "$before" ]; then
	systemctl restart openleet-judge.service openleet.service
fi
site=$(sed -n 's/^SITE_ADDRESS=//p' "$ENV_FILE")
case $site in http://*) ;; *) site=https://$site ;; esac
echo "OpenLeet is running: $site (status: $site/api/health, logs: journalctl -u openleet)"
