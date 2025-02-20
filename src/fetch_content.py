from apify import Actor

async def fetch_pages(urls):
    Actor.log.info("Fetching pages", extra={"urls": urls})

    start_urls = [{"url": url} for url in urls]

    run = await Actor.call(
        actor_id="apify/website-content-crawler",
        run_input={
            "startUrls": start_urls,
            "maxCrawlPages": len(start_urls),
            "crawlerType": "playwright:adaptive",
        })

    if run is None or run.status != 'SUCCEEDED':
        raise RuntimeError('Website Content Crawler failed to scrape the page')

    page = await Actor.apify_client.dataset(run.default_dataset_id).list_items(limit=1)

    if not page.items:
        raise ValueError('No content scraped')

    markdowns = [item.get('markdown') for item in page.items]
    return markdowns

async def fetch_single_page(url):
    return (await fetch_pages(urls=[url]))[0]

