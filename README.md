# Turn a page into a song! 🎶🎸

[![Webpage Singer](https://apify.com/actor-badge?actor=josef.prochazka/webpage-singer)](https://apify.com/josef.prochazka/webpage-singer)

This Actor scrapes content of a URL your provide, uses LLM to turn it into lyrics, and then generates a song from it.

## How does it work?

- Apify's [Website Content Crawler](https://apify.com/apify/website-content-crawler/input-schema) is used to scrape the URL.
- OpenAI API is used to generate lyrics from the page content.
- [TopMediai](https://www.topmediai.com/) is used to generate a song from the lyrics.

## Costs

You are charged per song generated. You can provide your own TopMedia AI API token to reduce the costs.

Note: We're currently running on a limited TopMediai plan, so having the Actor cover the costs of song generation is not guaranteed.

There is also a small additional cost for scraping the URL using the Website Content Crawler, which depends on the page complexity (roughly $0.01-0.05).

## Example results

Actor respects the language of the webpage and uses the same language for the song generation:

- [_Dynamic klezmer_ song](https://api.apify.com/v2/key-value-stores/KNPDwiHWpbV8fv5od/records/song) generated from a [news article](https://www.irozhlas.cz/zpravy-svet/neni-mozne-porad-preslapovat-na-miste-valka-trva-tri-roky-rika-prezident_2502201611_kvr). (Czech)
- [Auto-genre song](https://api.apify.com/v2/key-value-stores/aXqrrXXCZT3yYUGdR/records/song) generated from the [Apify About page](https://apify.com/about). (English)

## Open Source

This Actor is open source, hosted on [GitHub](https://github.com/Pijukatel/actor-text-summary-song).
