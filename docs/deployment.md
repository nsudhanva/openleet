# Deployment

```mermaid
flowchart LR
    P[push to main] --> CI["GitHub Actions<br/>lint, test, build x86-64-v3"]
    CI --> R["edge release<br/>openleet-REV.tar.zst"]
    CI -- "signed POST /api/deploy" --> S[openleet]
    S -- writes deploy-request --> PU[openleet-update.path]
    T[openleet-update.timer<br/>every 5 min, fallback] --> U
    PU --> U["update.sh (root)<br/>verify sha256, unpack,<br/>switch current, restart"]
    R --> U
    U --> V["CI polls /api/version<br/>until REV is live"]
```

A push to `main` runs the checks, builds a release archive and asks the server to deploy it. The
server only records the request. `update.sh` runs as root, verifies the archive, switches
`/opt/openleet/current` to it and restarts the services.

## On the server

Every part is a systemd unit that starts at boot, so a reboot needs no manual step.

- `openleet-http.socket` and `openleet-https.socket` hold ports 80 and 443, so a restart drops no
  connections.
- systemd restarts the server if it exits or does not answer its watchdog.
  `openleet-health.timer` restarts the server after three failed health checks. It restarts the
  judge when the judge is down.
- The server renews its TLS certificate 30 days before the certificate expires.
- The server copies the database to `/var/lib/openleet/backups/` every day and keeps the last 14
  copies.

When the server starts, it runs any pending migrations. If it cannot open the database file, it
moves the file to `/var/lib/openleet/quarantine/` and restores the newest backup. If the file
opens but a migration fails, the server stops and leaves the file as it is.

## Restore a backup

`/var/lib/openleet/backups/` holds a copy of the database for each of the last 14 days
(`DATE.duckdb`) and for each of the last three migrations, taken right before the migration ran
(`pre-migration-STAMP.duckdb`). A restore loses every change that you made after the backup was
taken. To restore a backup, stop the server, move the database aside and put the backup in its
place:

```bash
sudo systemctl stop openleet
sudo sh -c 'cd /var/lib/openleet && mkdir -p replaced && mv openleet.duckdb* replaced/'
sudo install -o openleet -g openleet -m 0600 BACKUP.duckdb /var/lib/openleet/openleet.duckdb
sudo systemctl start openleet
```

The server migrates a backup with an older schema when it starts.

## Roll back

`update.sh` keeps the newest three releases in `/opt/openleet/releases/`. To run an older
release, install its units and scripts, point `current` at it and restart the services:

```bash
old=/opt/openleet/releases/REV
sudo "$old/deploy/install.sh" --units-only
sudo ln -sfn "$old" /opt/openleet/current
sudo systemctl restart openleet-judge openleet
```

`update.sh` never installs a revision that it installed before. Thus neither the deploy request
of CI nor the 5-minute timer undoes the rollback. The next push to `main` does.

A build cannot open a database that a newer release migrated. The server stops with "newer
than this build's" in its log (`journalctl -u openleet`). To roll back past a migration, also
restore the copy that the server took right before that migration, or the newest daily backup
older than that migration (see above).

## New server

You need an Ubuntu 24.04 machine with 1 GB of memory or more (a free e2-micro on Google Cloud
works), ports 80 and 443 open to the internet, and a DNS A record that points a domain at the
machine.

```bash
git clone https://github.com/nsudhanva/openleet && cd openleet
sudo SITE_ADDRESS=openleet.example.com deploy/install.sh
```

The installer takes about two minutes. It creates the `openleet` user and installs Python for the
judge. It adds 1 GB of swap when the machine has none. It lets security updates reboot the
machine at 10:00 and writes `/etc/openleet.env`.

Then the installer downloads the newest release (server, web app, problems and test corpus) and
starts it. The server gets its TLS certificate from Let's Encrypt within a minute. To check it,
run `curl https://openleet.example.com/api/health`.

The installer also takes `TZ` (the day boundary for streaks, such as `America/Los_Angeles`; UTC
by default) and `DEPLOY_SECRET` (see below). Run the installer again to change them. It keeps the
values that you leave out. Set `SITE_ADDRESS=http://HOST` to serve plain HTTP without a
certificate.

The server installs each new release within 5 minutes. To move progress from another server,
restore a backup of that server (see above).

## Deploy from your own fork

A server installs releases from the GitHub repository that you cloned on it (`OPENLEET_REPO` in
`/etc/openleet.env`), so clone your fork on the server. Then, in the settings of the fork:

1. Enable GitHub Actions. Each push to `main` publishes a release, and your server installs it
   within 5 minutes.
2. For deploys within seconds of a push, add the repository variable `SITE_URL`
   (`https://openleet.example.com`) and the secret `DEPLOY_SECRET` (any long random string,
   such as the output of `openssl rand -hex 32`). Give the server the same secret:
   `sudo DEPLOY_SECRET=... deploy/install.sh`.

The test corpus is not in git: `data/judge/corpus.json` names the repository and release asset
that hold it. Thus a fork uses the corpus of its upstream until it rebuilds and publishes its own
(`uv run openleet judge publish`). The `images` workflow of the fork publishes Docker images to
`ghcr.io/OWNER`. Run them with `IMAGES=ghcr.io/OWNER docker compose up -d`.
