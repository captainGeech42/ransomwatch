# ransomwatch
Ransomware leak site monitoring

## Configuration:

Please copy `config.sample.yaml` to `config.yaml`, and add the following:

* Leak site URLs. I decided not to make this list public in order to prevent them from gaining even more noteriety, so if you have them, add them in. If not, this tool isn't for you.
* Slack webhook URLs. Follow [these](https://api.slack.com/messaging/webhooks) instructions to add a new app to your Slack workspace and add the webhook URL to the config.

Additionally, there are a few environment variables you may need to set:

* `RW_DB_PATH`: Path for the SQLite database to use
* `RW_CONFIG_PATH`: Path to the `config.yaml` file

These are both set in the provided `docker-compose.yaml`. If you prefer, you can modify the `Dockerfile` and use a volume to provide the `config.yaml` if you don't want to bake it in.

## Usage:

This is intended to be run via a cronjob on whatever increment you decide to use.

Example crontab entry (running every 8 hours):

```
0 */8 * * * cd /path/to/ransomwatch && docker-compose up --abort-on-container-exit
```

(make sure to build it first, `docker-compose build`)

## Leak Site Implementations:

The following leak sites are (planned to be) supported:

- [x] Conti
- [ ] MAZE
- [ ] Egregor
- [ ] Sodinokibi/REvil
- [ ] DoppelPaymer
- [ ] NetWalker
- [ ] Pysa
- [ ] Avaddon
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