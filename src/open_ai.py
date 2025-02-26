import os

from apify import Actor
from openai import AsyncOpenAI

OPENAI_MODEL = "gpt-4o"

# Max content length as supported by OpenAI API and the gpt-4o model
OPENAI_MAX_CONTENT_LENGTH_TOKENS = 128000


def get_open_api_client():
    return AsyncOpenAI(
        api_key=os.environ.get(
            "OPENAI_API_KEY"
        ),
    )


def truncate_to_max_content_length(content):
    # Simple heuristic: 1 word = 4 tokens. This is a pessimistic conversion, which should be safe for most languages.
    truncated_content = " ".join(content.split()[:OPENAI_MAX_CONTENT_LENGTH_TOKENS // 4])

    if len(truncated_content) < len(content):
        Actor.log.warning(
            "Fetched page was too long for OpenAI API and was truncated",
            extra={"original_length": len(content), "truncated_length": len(truncated_content)})

    return truncated_content
