from apify import Actor


async def main() -> None:
    async with Actor:
        # Read inputs
        actor_input = await Actor.get_input() or {'url': 'https://apify.com/'}
        url = actor_input.get('url')
        if not url:
            raise ValueError('Missing "url" attribute in input!')

        # Get text summary

        # Generate song.

        # Push song to kvs
