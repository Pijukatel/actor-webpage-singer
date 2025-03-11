from apify import Actor


async def fetch_content(url):
    run = await Actor.call(
        actor_id="apify/website-content-crawler",
        run_input={
            "startUrls": [{"url": url}],
            "maxCrawlPages": 1,
            "crawlerType": "playwright:adaptive",
            "proxyConfiguration": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
        },
        memory_mbytes=4096,  # Reduce memory so that it can run on free accounts.
    )

    if run is None or run.status != "SUCCEEDED":
        raise RuntimeError("Website Content Crawler failed to scrape the page")

    page = await Actor.apify_client.dataset(run.default_dataset_id).list_items(limit=1)

    if not page.items:
        raise ValueError("No content scraped")

    return page.items[0].get("markdown")
