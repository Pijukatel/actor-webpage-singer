import os

from apify import Actor

from src.fetch_content import fetch_content
from src.music_generation import generate_song, get_song
from src.lyrics_generation import generate_lyrics

async def main() -> None:
    async with Actor:
        # Read inputs
        actor_input = await Actor.get_input() or {'url': 'https://www.novinky.cz/clanek/krimi-ukradl-znamemu-igelitku-s-miliony-a-zmizel-na-opacny-konec-sveta-po-dvanacti-letech-pujde-do-vezeni-40509696'}
        url = actor_input.get('url')
        if not url:
            raise ValueError('Missing "url" attribute in input!')

        # Fetch content.
        content = await fetch_content(url)

        # Generate song lyrics.
        Actor.log.info("Generating the song lyrics")
        lyrics = generate_lyrics(content)
        print(lyrics)

        # Generate song.
        charge_result = await Actor.charge(
            event_name='foobar',
            count=4,
        )

        api_key = actor_input.get('topmediai_api_key') or os.environ.get("TOPMEDIAI_API_KEY")
        song_link = generate_song(lyrics=lyrics, api_key=api_key, genre=actor_input.get('song_genre'), logger=Actor.log)
        kvs = await Actor.open_key_value_store()
        await kvs.set_value(key="song", value=get_song(song_link), content_type="audio/mpeg")
