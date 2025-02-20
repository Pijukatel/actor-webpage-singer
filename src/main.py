import os

from apify import Actor

from src.music_generation import generate_song, get_song
from src.lyrics_generation import generate_lyrics

async def main() -> None:
    async with Actor:
        # Read inputs
        actor_input = await Actor.get_input()
        url = actor_input.get('url')
        if not url:
            raise ValueError('Missing "url" attribute in input!')

        # Generate song lyrics.
        Actor.log.info("Generating the song lyrics")
        lyrics = await generate_lyrics(url, extract_top_stories=True) # TODO: get this from input
        Actor.log.info("Generated lyrics", extra={"lyrics": lyrics })

        # TODO: Enable
        # # Actor charge based on which key is used
        # user_api_key = actor_input.get('topmediai_api_key')
        # actor_api_key = os.environ.get("TOPMEDIAI_API_KEY")
        # if user_api_key:
        #     topmediai_api_key = user_api_key
        #
        #     #await Actor.charge(event_name='song_with_user_api_key',count=1)
        # else:
        #     topmediai_api_key = actor_api_key
        #     #await Actor.charge(event_name='song_with_actor_api_key', count=1)
        #
        # # Generate song.
        # song_link = generate_song(lyrics=lyrics, api_key=topmediai_api_key, genre=actor_input.get('song_genre'), logger=Actor.log)
        # kvs = await Actor.open_key_value_store()
        # await kvs.set_value(key="song", value=get_song(song_link), content_type="audio/mpeg")
