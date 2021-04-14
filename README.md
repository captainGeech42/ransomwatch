# ransomwatch
Ransomware leak site monitoring

## Things to implement

- Scrape the full site
- See if there are new leaks
- See if any leaks were removed

need to set docker-compose volume for sqlite db, set in `RW_DB_PATH` env var

notify via slack/webhook whatever when a new leak is posted

Set `RW_CONFIG_PATH` env var for path to config (in container it's `/app/config.yaml`)