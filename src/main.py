import os

from apify import Actor

from src.fetch_content import fetch_content
from src.music_generation import generate_song, get_song
from src.lyrics_generation import generate_lyrics
from src.suggest_music_genre import suggest_music_genre


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input()
        kvs = await Actor.open_key_value_store()

        # Fetch page content.
        url = actor_input.get("url")
        if not url:
            raise ValueError('Missing "url" attribute in input!')
        await Actor.set_status_message("Fetching page content")
        Actor.log.info("Fetching page content", extra={"url": url})
        page_content = await fetch_content(url)

        # Generate song lyrics + determine genre.
        await Actor.set_status_message("Generating lyrics using AI")
        Actor.log.info(
            "Generating lyrics using AI", extra={"page_content": page_content}
        )
        lyrics = await generate_lyrics(page_content)
        song_genre = actor_input.get("song_genre") or await suggest_music_genre(page_content)
        await kvs.set_value(key="lyrics.txt", value=lyrics, content_type="text/plain")

        # Generate song.
        await Actor.set_status_message(
            "Generating the song (this might take a few minutes)"
        )
        Actor.log.info("Generating the song", extra={"lyrics": lyrics, "genre": song_genre})
        topmediai_api_key = actor_input.get("topmediai_api_key") or os.environ.get(
            "TOPMEDIAI_API_KEY"
        )

        song_link = generate_song(
            lyrics=lyrics,
            api_key=topmediai_api_key,
            genre=song_genre,
            logger=Actor.log,
        )
        await kvs.set_value(
            key="song", value=get_song(song_link), content_type="audio/mpeg"
        )

        # Charge user based on the resources used
        if actor_input.get("topmediai_api_key"):
            await Actor.charge(event_name="song_with_user_api_key", count=1)
        else:
            await Actor.charge(event_name="song_with_actor_api_key", count=1)

        # Alternative visualisation
        dataset = await Actor.open_dataset()
        await dataset.push_data({"url": song_link, "lyrics": lyrics})
