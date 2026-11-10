#!/bin/sh
# Installs the newest release CI published (github.com/nsudhanva/google, release "edge"), if it
# is not the one running: unpack next to the others, switch the `current` link, restart.
# Run by google-cards-update.timer as root; safe to run by hand.
set -eu
ROOT=/opt/google-cards
BASE=https://github.com/nsudhanva/google/releases/download/edge

revision=$(curl -fsSL "$BASE/REVISION")
if [ "$(cat "$ROOT/current/REVISION" 2>/dev/null || true)" = "$revision" ]; then
	exit 0
fi
echo "updating to $revision"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
archive="google-cards-$revision.tar.zst"
curl -fsSL -o "$work/$archive" "$BASE/$archive"
curl -fsSL -o "$work/$archive.sha256" "$BASE/$archive.sha256"
(cd "$work" && sha256sum -c "$archive.sha256" >/dev/null)

release="$ROOT/releases/$revision"
rm -rf "$release"
mkdir -p "$release"
tar --zstd -xf "$work/$archive" -C "$release"
# Units and this script come with each release, so changes to them deploy themselves.
"$release/deploy/install.sh" --units-only "$release"
ln -sfn "$release" "$ROOT/current.next"
mv -T "$ROOT/current.next" "$ROOT/current"
systemctl restart google-judge.service google-cards.service

# Keep the last three releases for a quick rollback (point `current` back and restart).
ls -1dt "$ROOT"/releases/* | tail -n +4 | xargs -r rm -rf
