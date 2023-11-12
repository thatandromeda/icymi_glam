Based on [Mau Foronda's fork](https://github.com/mauforonda/mastodon_digest) of [Matt Hodges' mastodon_digest](https://github.com/hodgesmr/mastodon_digest).

Rather than rendering a digest page, this powers a bot based on [@icymi_law](https://icymilaw.org/), but for the GLAM community. The bot lives at [@icymi_glam@glammr.us](https://https://glammr.us/@icymi_glam).

---

## Development

Prerequisites:
* set up a mastodon bot
* create a mastodon token which can read and write your timeline
* copy `.env.example` to `.env` and fill in the credentials with your own

Install dependencies: `poetry install`

Run tests: `poetry run python -m unittest tests`

Run the bot from CLI: `poetry run python run.py -n 12 -s SimpleWeighted -t lax`

## To run your own

1. Fork this repository
2. Create repository secrets (`Settings` → `Secrets/Actions` → `New repository secrets`) for:
  - `MASTODON_BASE_URL`: the url of your instance, like `https://mastodon.social`
  - `MASTODON_USERNAME`: your user name, like `Gargron`
  - `MASTODON_TOKEN`: a token you request in your instance settings under `Preferences` → `Development`
3. Adjust the [github workflow](.github/workflows/update.yml) however you want
  - edit `cron` to define how often you want the digest to run
  - edit the command `python run.py -n 12 -s SimpleWeighted -t lax` with your own preferences for:
```
  -n {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24}
                        The number of hours to consider (default: 12)
  -s {ExtendedSimple,ExtendedSimpleWeighted,Simple,SimpleWeighted}
                        Which post scoring criteria to use. Simple scorers take a geometric
                        mean of boosts and favs. Extended scorers include reply counts in
                        the geometric mean. Weighted scorers multiply the score by an
                        inverse sqaure root of the author's followers, to reduce the
                        influence of large accounts. (default: SimpleWeighted)
  -t {lax,normal,strict}
                        Which post threshold criteria to use. lax = 90th percentile, normal
                        = 95th percentile, strict = 98th percentile (default: normal)
```
4. Enable github actions under `Settings` → `Actions/General`,  run the action from the `Actions` tab and when it succeeds publish your digest by going to `Settings` → `Pages` and selecting to deploy from the `root` of the `gh-pages` branch.
