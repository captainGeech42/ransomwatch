# RansomWatch

[![Build Image](https://github.com/captainGeech42/ransomwatch/workflows/Build%20Image/badge.svg)](https://github.com/captainGeech42/ransomwatch/actions?query=workflow%3A%22Build+Image%22) [![Docker Hub Publish](https://github.com/captainGeech42/ransomwatch/workflows/Docker%20Hub%20Publish/badge.svg)](https://github.com/captainGeech42/ransomwatch/actions?query=workflow%3A%22Docker+Hub+Publish%22) [![Docker Hub Image](https://img.shields.io/docker/v/captaingeech/ransomwatch?color=blue)](https://hub.docker.com/repository/docker/captaingeech/ransomwatch/general)

RansomWatch is a ransomware leak site monitoring tool. It will scrape all of the entries on various ransomware leak sites, store the data in a SQLite database, and send notifications via Slack or Discord when a new victim shows up, or when a victim is removed.

_Note: RansomWatch isn't being actively updated for the latest sites, and is mostly reliant on third-party contributions. Please open a pull request, and/or DM me on [Twitter](https://twitter.com/captainGeech42)._

## Configuration

In `config_vol/`, please copy `config.sample.yaml` to `config.yaml`, and add the following:

* Leak site URLs. I decided not to make this list public in order to prevent them from gaining even more noteriety, so if you have them, add them in. If not, this tool isn't for you.
  * To get the Hive API onion, load their main site and press F12 to use the developer tools. Look for XHR requests, you should see a few to a `hiveapi...` onion domain.
* Notification destinations. RansomWatch currently supports notifying via.the following:
  * Slack: Follow [these](https://api.slack.com/messaging/webhooks) instructions to add a new app to your Slack workspace and add the webhook URL to the config.
  * Discord: Follow [these](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) instructions to add a new app to your Discord server and add the webhook URL to the config.
  * Teams: Follow [these](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) instructions to add a new app to your Teams channel and add the webhook URL to the config.

Additionally, there are a few environment variables you may need to set:

* `RW_DB_PATH`: Path for the SQLite database to use
* `RW_CONFIG_PATH`: Path to the `config.yaml` file

These are both set in the provided `docker-compose.yml`.

## Usage

This is intended to be run in Docker via a cronjob on whatever increment you decide to use.

First, build the container: `docker-compose build app`

Then, add it to your crontab. Example crontab entry (running every 8 hours):

```
0 */8 * * * cd /path/to/ransomwatch && docker-compose up --abort-on-container-exit
```

If you'd prefer, you can use the image published on Docker Hub ([`captaingeech/ransomwatch`](https://hub.docker.com/repository/docker/captaingeech/ransomwatch/general)) instead, with a `docker-compose.yml` that looks something like this:

```yml
version: "3"

services:
  app:
    image: captaingeech/ransomwatch:latest
    depends_on:
      - proxy
    volumes:
      - ./db_vol:/db
      - ./config_vol:/config
    environment:
      PYTHONUNBUFFERED: 1
      RW_DB_PATH: /db/ransomwatch.db
      RW_CONFIG_PATH: /config/config.yaml

  proxy:
    image: captaingeech/tor-proxy:latest
```

This can also be run via the command line, but that requires you to have your own Tor proxy (with the control service) running. Example execution:

```
$ RW_DB_PATH=./db_vol/ransomwatch.db RW_CONFIG_PATH=./config_vol/config.yaml python3 src/ransomwatch.py
```

## Example Slack Messages

![Slack notification for new victim](/img/slack_example_new_victim.png)

![Slack notification for removed victim](/img/slack_example_removed_victim.png)

![Slack notification for site down](/img/slack_example_site_down.png)

![Slack notification for an error](/img/slack_example_error.png)

The messages sent to Discord and Teams are very similar in style, identical in content.

## Leak Site Implementations

The following leak sites are supported:

- [x] Conti
- [X] Sodinokibi/REvil
- [X] Pysa
- [X] Avaddon
- [X] DarkSide
- [X] CL0P
- [X] Nefilim
- [X] Mount Locker
- [X] Suncrypt
- [x] Everest
- [X] Ragnarok
- [X] Ragnar_Locker
- [X] BABUK LOCKER
- [X] Pay2Key
- [X] Cuba
- [X] RansomEXX
- [X] Pay2Key
- [X] Ranzy Locker
- [X] Astro Team
- [X] BlackMatter
- [X] Arvin
- [X] El_Cometa
- [X] Lorenz
- [X] Xing
- [X] Lockbit
- [X] AvosLocker
- [X] LV
- [X] Marketo
- [X] Lockdata
- [X] Rook

If there are other leak sites you want implemented, feel free to open a PR or DM me on Twitter, [@captainGeech42](https://twitter.com/captainGeech42)
