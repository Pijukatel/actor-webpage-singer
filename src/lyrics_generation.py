import os

from openai import OpenAI

SYSTEM_PROMPT = """
You are a helpful, analytical assistant that can summarize text. You try to be non-biased and sticking to facts.
"""

USER_PROMPT = """
Summarize the following text into a song-like structure.

 - It should consist of several verses, each around 30 words, all of the roughly same length.
 - Don't rhyme it, unless the text is in English.
 - The text remains understandable, clear and factual.
 - Don't change the meaning, the story should stay as is.
 - Stick to the original order of information.
 - Stick to the original language.
 - Don't print headlines like "Verse 1".
"""

def generate_lyrics(content):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )

    result = chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{USER_PROMPT}\n\n```{content}```"}
        ],
        model="gpt-4o",
    )

    return result.choices[0].message.content
