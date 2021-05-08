# Contributing Info

Thank you for contributing code to RansomWatch! Please read this document for info on how to make a successful PR to the project

## New Leak Site

This is probably the main source of external contributions to the project. When adding a new site, the easiest way to start is by referencing one of the existing leak site implementations, and tweaking it to properly support your site. You'll also need to add it to the list of sites in `src/ransomwatch.py`.

To test it, make a `config.yaml` and configure a notification provider and the leak site URL, and use the provided `docker-compose.yml`. This command is the easiest one-liner for repetitive testing:

```
$ docker-compose build app && docker-compose up --abort-on-container-exit
```

## Other Features

If you have cool ideas for ways to make RansomWatch better, that'd be awesome! Please open an issue first with your idea so you don't waste anytime if it conflicts with other plans for the project, and then it can be connected to a pull request when you have the code ready to add.