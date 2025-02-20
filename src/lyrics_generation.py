from src.open_ai_client import get_open_api_client

SYSTEM_PROMPT = """
You are a helpful, analytical assistant that can summarize text. You try to be non-biased and sticking to facts.
"""

USER_PROMPT = """
Summarize the following text into a song-like structure.

 - It should consist of max 4 verses, each around 30 words, all of the roughly same length.
 - Don't rhyme it, unless the text is in English.
 - The text remains understandable, clear and factual.
 - Don't change the meaning, the story should stay as is.
 - Stick to the original order of information.
 - Stick to the original language.
 - Don't print headlines like "Verse 1".
"""


async def generate_lyrics(content):
    chat_completion = await get_open_api_client().chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{USER_PROMPT}\n\n```{content}```"},
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content
