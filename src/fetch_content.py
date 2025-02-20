from apify import Actor


async def fetch_content(url):
    run = await Actor.call(
        actor_id="apify/website-content-crawler",
        run_input={
            "startUrls": [{"url": url}],
            "maxCrawlPages": 1,
            "crawlerType": "playwright:firefox",
        },
    )

    if run is None or run.status != "SUCCEEDED":
        raise RuntimeError("Website Content Crawler failed to scrape the page")

    page = await Actor.apify_client.dataset(run.default_dataset_id).list_items(limit=1)

    if not page.items:
        raise ValueError("No content scraped")

    return page.items[0].get("markdown")
