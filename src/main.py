import os

from apify import Actor

from src.fetch_content import fetch_content
from src.music_generation import get_song, generate_songs
from src.lyrics_generation import generate_lyrics
from src.open_ai import truncate_to_max_content_length
from src.suggest_music_genre import suggest_music_genre


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input()
        kvs = await Actor.open_key_value_store()
        dataset = await Actor.open_dataset()  # Alternative visualisation

        url = actor_input.get("url")
        if not url:
            raise ValueError('Missing "url" attribute in input!')

        # Fetch page content.
        try:
            await Actor.set_status_message("Fetching page content")
            Actor.log.info("Fetching page content", extra={"url": url})
            page_content = truncate_to_max_content_length(await fetch_content(url))
        except Exception as e:
            await Actor.fail(
                exception=e, status_message="Fetching page content failed."
            )

        # Generate song lyrics + determine genre.
        try:
            await Actor.set_status_message("Generating lyrics using AI")
            Actor.log.info(
                "Generating lyrics using AI", extra={"page_content": page_content}
            )
            lyrics = await generate_lyrics(page_content)
            song_genre = actor_input.get("song_genre") or await suggest_music_genre(
                page_content
            )
            await kvs.set_value(
                key="lyrics.txt", value=lyrics, content_type="text/plain"
            )
        except Exception as e:
            await Actor.fail(
                exception=e, status_message="Generating lyrics using AI failed."
            )

        # Generate song.
        try:
            await Actor.set_status_message(
                "Generating the song (this might take a few minutes)"
            )
            Actor.log.info(
                "Generating the song", extra={"lyrics": lyrics, "genre": song_genre}
            )
            topmediai_api_key = actor_input.get("topmediai_api_key") or os.environ.get(
                "TOPMEDIAI_API_KEY"
            )

            song_links = generate_songs(
                lyrics=lyrics,
                api_key=topmediai_api_key,
                genre=song_genre,
                logger=Actor.log,
            )
            for variant, song_link in enumerate(song_links, start=1):
                await kvs.set_value(
                    key=f"song_variant_{variant}",
                    value=get_song(song_link),
                    content_type="audio/mpeg",
                )
                await dataset.push_data({"url": song_link, "lyrics": lyrics})
        except Exception as e:
            await Actor.fail(
                exception=e, status_message="Generating song using TopMediaAI failed."
            )

        # Charge user based on the resources used
        if actor_input.get("topmediai_api_key"):
            await Actor.charge(event_name="song_with_user_api_key", count=1)
        else:
            await Actor.charge(event_name="song_with_actor_api_key", count=1)
