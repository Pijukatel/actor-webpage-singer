# Turn a page into a song! 🎶🎸

This Actor scrapes content of a URL your provide, uses LLM to turn it into lyrics, and then generates a song from it.

## How does it work?

- Apify's [Website Content Crawler](https://apify.com/apify/website-content-crawler/input-schema) is used to scrape the URL.
- OpenAI API is used to generate lyrics from the page content.
- [TopMediai](https://www.topmediai.com/) is used to generate a song from the lyrics.

## Costs

You are charged per song generated. You can provide your own TopMedia AI API token to reduce the costs.

Note: We're currently running on a limited TopMediai plan, so having the Actor cover the costs of song generation is not guaranteed.
