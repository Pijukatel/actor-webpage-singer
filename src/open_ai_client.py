import os

from openai import AsyncOpenAI


def get_open_api_client():
    return AsyncOpenAI(
        api_key=os.environ.get(
            "OPENAI_API_KEY"
        ),  # This is the default and can be omitted
    )
