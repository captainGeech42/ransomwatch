# RansomWatch

_(NOTE: RansomWatch is actively being developed, and isn't suitable for prod, **yet**)_

RansomWatch is a ransomware leak site monitoring tool. It will scrap all of the entries on various ransomware leak sites, store the data in a SQLite database, and send notifications via Slack when a new victim shows up, or when a victim is removed.

## Configuration

Please copy `config.sample.yaml` to `config.yaml`, and add the following:

* Leak site URLs. I decided not to make this list public in order to prevent them from gaining even more noteriety, so if you have them, add them in. If not, this tool isn't for you.
* Slack webhook URLs. Follow [these](https://api.slack.com/messaging/webhooks) instructions to add a new app to your Slack workspace and add the webhook URL to the config.

Additionally, there are a few environment variables you may need to set:

* `RW_DB_PATH`: Path for the SQLite database to use
* `RW_CONFIG_PATH`: Path to the `config.yaml` file

These are both set in the provided `docker-compose.yaml`. If you prefer, you can modify the `Dockerfile` and use a volume to provide the `config.yaml` if you don't want to bake it in.

## Usage

This is intended to be run via a cronjob on whatever increment you decide to use.

Example crontab entry (running every 8 hours):

```
0 */8 * * * cd /path/to/ransomwatch && docker-compose up --abort-on-container-exit
```

(make sure to build it first, `docker-compose build`)

## Example Slack Messages

New victim:

![Slack notification for new victim](/img/slack_example_new_victim.png)

Removed victim:

![Slack notification for removed victim](/img/slack_example_removed_victim.png)

Site down:

![Slack notification for site down](/img/slack_example_site_down.png)

Error:

![Slack notification for an error](/img/slack_example_error.png)


## Leak Site Implementations

The following leak sites are (planned to be) supported:

- [x] Conti
- [ ] MAZE
- [ ] Egregor
- [X] Sodinokibi/REvil
- [ ] DoppelPaymer (captcha, prob won't be supported for a while)
- [ ] NetWalker
- [ ] Pysa
- [X] Avaddon
- [ ] DarkSide
- [ ] CL0P
- [ ] Nefilim
- [ ] Everest
- [ ] Suncrypt
- [ ] Ragnar_Locker
- [ ] Ragnarok
- [ ] Mount Locker
- [ ] BABUK LOCKER
- [ ] RansomEXX
- [ ] Cuba
- [ ] Pay2Key
- [ ] Astro Team
- [ ] Ranzy Locker
- [ ] LV

If there are other leak sites you want implemented, feel free to open a PR or DM me on Twitter, [@captainGeech42](https://twitter.com/captainGeech42)