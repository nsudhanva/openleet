#!/bin/sh
# Installs the release CI published (github.com/nsudhanva/openleet, release "edge") if it is new:
# unpack next to the others, switch the `current` link, restart.
# Run as root by openleet-update.service (on CI's signed deploy request, and every 5 minutes as
# a fallback); safe to run by hand.
set -eu
ROOT=/opt/openleet
BASE=https://github.com/nsudhanva/openleet/releases/download/edge
# Written by the server after it checks the HMAC of CI's deploy request.
REQUEST=/var/lib/openleet/deploy-request
# Every revision this server has installed, oldest first.
HISTORY=$ROOT/deployed
KEEP=3

# systemd serializes its own runs; the lock also covers invocations by hand.
exec 9>"$ROOT/update.lock"
flock -n 9 || exit 0

# A revision names a directory that gets `rm -rf`: accept only the hex CI writes.
valid() {
	case $1 in '' | *[!0123456789abcdef]*) return 1 ;; esac
}
seen() {
	grep -qx "$1" "$HISTORY" 2>/dev/null
}

# CI's request names its revision exactly. GitHub's download CDN can serve a stale REVISION
# for a few minutes, so that file only drives the timer's checks, and a revision installed
# before is never installed again: a stale copy cannot roll production back.
revision=$(cat "$REQUEST" 2>/dev/null || true)
if ! valid "$revision" || seen "$revision"; then
	revision=$(curl -fsSL "$BASE/REVISION")
	valid "$revision" || {
		echo "bad revision from $BASE/REVISION: '$revision'" >&2
		exit 1
	}
	seen "$revision" && exit 0
fi
echo "updating to $revision"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
trap 'exit 1' HUP INT TERM
archive="openleet-$revision.tar.zst"
# Just-published assets can take a moment to reach the CDN.
fetch() {
	curl -fsSL --retry 8 --retry-delay 5 --retry-all-errors -o "$work/$1" "$BASE/$1"
}
fetch "$archive"
fetch "$archive.sha256"
(cd "$work" && sha256sum -c "$archive.sha256" >/dev/null)

release="$ROOT/releases/$revision"
current=$(readlink -f "$ROOT/current" 2>/dev/null || true)
if [ "$release" != "$current" ]; then
	rm -rf "$release"
	mkdir -p "$release"
	tar --zstd --no-same-owner --no-same-permissions -xf "$work/$archive" -C "$release"
fi
# Root runs parts of the release, so root owns all of it (not CI's uid). The data (reference
# solutions, expected outputs) is readable by the server only, never by submissions.
chown -R root:root "$release"
chgrp -R openleet "$release/data"
chmod -R o-rwx "$release/data"
# Units and this script come with each release, so changes to them deploy themselves.
"$release/deploy/install.sh" --units-only
# mv -T renames over the old link in one step, so `current` always points at a whole release.
ln -sfn "$release" "$ROOT/current.next"
mv -T "$ROOT/current.next" "$ROOT/current"
# The judge first (a submission in flight fails once), then the server: systemd holds its
# sockets, so the restart refuses no connection.
systemctl restart openleet-judge.service
systemctl restart openleet.service
# A failed restart must remain retryable on the next timer tick.
echo "$revision" >>"$HISTORY"

# Keep the newest releases for a quick rollback (point `current` back and restart), never the
# running one. Release names are hex revisions, so parsing ls is safe.
current=$(readlink -f "$ROOT/current")
# shellcheck disable=SC2012
ls -1dt "$ROOT"/releases/* | tail -n +$((KEEP + 1)) | while IFS= read -r old; do
	if [ "$old" != "$current" ]; then rm -rf "$old"; fi
done
