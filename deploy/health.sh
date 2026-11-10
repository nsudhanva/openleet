#!/bin/sh
# Checks OpenLeet once (openleet-health.timer runs it every minute, as root) and heals it:
# restarts the server after three failed health checks in a row, restarts the judge when the
# server reports it down, and logs an error when the certificate is close to expiry.
set -eu

ENV_FILE=/etc/openleet.env
FAILS=/run/openleet-health.fails
CERT_WARN_DAYS=14

site=$(sed -n 's/^SITE_ADDRESS=//p' "$ENV_FILE" | cut -d, -f1)
case "$site" in
	http://*) url="${site%/}/api/health"; resolve="" ;;
	*) url="https://$site/api/health"; resolve="--resolve $site:443:127.0.0.1" ;;
esac

# shellcheck disable=SC2086 # $resolve is empty or two words on purpose.
if body=$(curl -fsS --max-time 10 $resolve "$url"); then
	rm -f "$FAILS"
else
	count=$(($(cat "$FAILS" 2>/dev/null || echo 0) + 1))
	echo "$count" >"$FAILS"
	echo "health check failed ($count in a row)"
	if [ "$count" -ge 3 ]; then
		echo "restarting openleet.service"
		systemctl restart openleet.service
		rm -f "$FAILS"
	fi
	exit 0
fi

if [ "$(printf '%s' "$body" | jq -r .judge)" != "ok" ]; then
	echo "judge reported down: restarting openleet-judge.service"
	systemctl restart openleet-judge.service
fi

expires=$(printf '%s' "$body" | jq -r '.certificate.expires_at // empty')
if [ -n "$expires" ]; then
	days=$(((expires / 1000 - $(date +%s)) / 86400))
	if [ "$days" -lt "$CERT_WARN_DAYS" ]; then
		echo "certificate expires in $days days; automatic renewal is not working" >&2
	fi
fi
