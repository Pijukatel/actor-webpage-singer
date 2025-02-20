from src.open_ai_client import get_open_api_client

SYSTEM_PROMPT = """
You are a helpful, sensitive and empathetic assistant that understands nuances and emotions in text.
"""

USER_PROMPT = """
The following text will be turned into a song. Please suggest a music genre that fits the text.

Take into account the mood, tone, severity, topic etc.

Return just the genre and nothing else.

Sample outputs: "indie britpop", "experimental rock", "opera".
"""


async def suggest_music_genre(content):
    chat_completion = await get_open_api_client().chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{USER_PROMPT}\n\n```{content}```"},
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content
