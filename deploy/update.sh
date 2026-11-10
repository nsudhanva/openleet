#!/bin/sh
# Installs the newest release CI published (github.com/nsudhanva/openleet, release "edge"), if it
# is not the one running: unpack next to the others, switch the `current` link, restart.
# Run as root by openleet-update.service; safe to run by hand.
set -eu
ROOT=/opt/openleet
BASE=https://github.com/nsudhanva/openleet/releases/download/edge
KEEP=3

revision=$(curl -fsSL "$BASE/REVISION")
# A revision names a directory that gets `rm -rf`: accept only the hex CI writes.
case $revision in
'' | *[!0123456789abcdef]*)
	echo "bad revision from $BASE/REVISION: '$revision'" >&2
	exit 1
	;;
esac
if [ "$(cat "$ROOT/current/REVISION" 2>/dev/null || true)" = "$revision" ]; then
	exit 0
fi
echo "updating to $revision"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
trap 'exit 1' HUP INT TERM
archive="openleet-$revision.tar.zst"
curl -fsSL -o "$work/$archive" "$BASE/$archive"
curl -fsSL -o "$work/$archive.sha256" "$BASE/$archive.sha256"
(cd "$work" && sha256sum -c "$archive.sha256" >/dev/null)

release="$ROOT/releases/$revision"
rm -rf "$release"
mkdir -p "$release"
tar --zstd -xf "$work/$archive" -C "$release"
# Units and this script come with each release, so changes to them deploy themselves.
"$release/deploy/install.sh" --units-only
# mv -T renames over the old link in one step, so `current` always points at a whole release.
ln -sfn "$release" "$ROOT/current.next"
mv -T "$ROOT/current.next" "$ROOT/current"
# The judge first (a submission in flight fails once), then the server: systemd holds its
# sockets, so the restart refuses no connection.
systemctl restart openleet-judge.service
systemctl restart openleet.service

# Keep the newest releases for a quick rollback (point `current` back and restart), never the
# running one. Release names are hex revisions, so parsing ls is safe.
current=$(readlink -f "$ROOT/current")
# shellcheck disable=SC2012
ls -1dt "$ROOT"/releases/* | tail -n +$((KEEP + 1)) | while IFS= read -r old; do
	if [ "$old" != "$current" ]; then rm -rf "$old"; fi
done
