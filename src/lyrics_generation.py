import json

from apify import Actor
from pydantic import BaseModel

from src.fetch_content import fetch_single_page, fetch_pages
from src.open_ai_client import get_open_api_client

NUMBER_OF_TOP_STORIES = 4

SYSTEM_PROMPT_FOR_LYRICS_GENERATION = """
You are a helpful, analytical assistant that can summarize text to song-like structures.

Stick to the following rules:
- All verses should be around 30 words, all of them roughly the same length.
- Don't rhyme the output, unless the original text is in English.
- Don't print headlines like "Verse 1".
- Whatever you produce should not change the meaning from the original input.
- Stick to the original order of information.
- Stick to the original language.
- The text remains understandable, clear and factual.
"""

USER_PROMPT_TO_GENERATE_SINGLE_PAGE_LYRICS = f"""
Summarize the following text into song-like lyrics. Generate max 4 verses
"""

USER_PROMPT_TO_EXTRACT_TOP_STORIES = f"""
The following text should be a scraped content of a news website main page.

Extract the top {NUMBER_OF_TOP_STORIES} stories with the biggest impact on the world.

Print URLs of the stories as a valid JSON array and nothing else, so that it can be parsed in the next step.

Example output:

```
["https://url1.com", "https://url2.com", "https://url3.com", "https://url4.com"]
```
"""

USER_PROMPT_TO_GENERATE_TOP_STORIES_LYRICS = f"""
Summarize each of the following articles into a single song verse.
"""

async def generate_lyrics(url, extract_top_stories = False):
    if extract_top_stories:
        return await generate_lyrics_from_top_stories(url)
    else:
        return await generate_lyrics_from_single_page(url)

async def generate_lyrics_from_single_page(url):
    content = await fetch_single_page(url)

    chat_completion = await get_open_api_client().chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_FOR_LYRICS_GENERATION},
            {"role": "user", "content": f"{USER_PROMPT_TO_GENERATE_SINGLE_PAGE_LYRICS}```{content}```"}
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content

async def generate_lyrics_from_top_stories(url):
    # Get the top stories form the main page
    top_stories_urls = await get_top_stories_urls(url)

    # Fetch content for all the pages
    stories = await fetch_pages(top_stories_urls)

    # Generate lyrics
    annotated_stories = [f"Article ${i+1}: \n\n{story}" for i, story in enumerate(stories)]
    print(annotated_stories)
    chat_completion = await get_open_api_client().chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_FOR_LYRICS_GENERATION},
            {"role": "user", "content": f"{USER_PROMPT_TO_GENERATE_TOP_STORIES_LYRICS}```{annotated_stories}```"}
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content

class TopStoriesUrlsResponse(BaseModel):
    urls: list[str]

async def get_top_stories_urls(main_page_url):
    main_page_content = await fetch_single_page(main_page_url)

    print(main_page_content)

    # Let LLM pick the top stories
    chat_completion = await get_open_api_client().beta.chat.completions.parse(
        messages=[
            {"role": "system", "content": "Produce valid JSON"},
            {"role": "user", "content": f"{USER_PROMPT_TO_EXTRACT_TOP_STORIES} \n\n```{main_page_content}```"}
        ],
        model="gpt-4o",
        response_format=TopStoriesUrlsResponse
    )

    response = chat_completion.choices[0].message.parsed
    Actor.log.info("Extracted top stories URLs", extra={"response": response})

    return response.urls
