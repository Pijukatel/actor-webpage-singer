import os
from apify import Actor
from openai import OpenAI

from src.music_generation import generate_song, get_song


from src.lyrics_generation import generate_lyrics

SYSTEM_PROMPT = """
You are a helpful, analytical assistant that can summarize text. You try to be non-biased and sticking to facts.
"""

USER_PROMPT = """
Summarize the following text into a song-like structure.

 - It should consist of several verses, each around 30 words.
 - They don't have to rhyme but should be of the same length.
 - Stay factual, keeping the original content.
 - Stick to the original language.
"""

async def main() -> None:
    async with Actor:
        # Read inputs
        actor_input = await Actor.get_input() or {'url': 'https://apify.com/'}
        url = actor_input.get('url')
        if not url:
            raise ValueError('Missing "url" attribute in input!')

        # Hard-code a multi-line string to a variable:
        content = """
Čtyřletý trest vězení potvrdil ve středu Vrchní soud v Olomouci Lukáši Ondráčkovi (41) z Uherského Hradiště za to, že na začátku roku 2012 ukradl igelitku s 210 tisíci eury (přes 5,2 milionu korun) svému tehdy devětatřicetiletému známému. Po více než dvanácti letech tak soud uzavřel kauzu, kterou se česká justice zabývala několikrát.

Foto: Petr Marek
Lukáš Ondráček u Vrchního soudu v Olomouci

Článek
Muž, který po krádeži narychlo odletěl na Nový Zéland, od počátku tvrdil, že je nevinný. Hájil se tím, že šlo o mstu ze strany jeho známého.

Poprvé ho odsoudil senát zlínské pobočky Krajského soudu v Brně 4. září 2012 na sedm let za mříže. Olomoucký vrchní soud pak tento verdikt potvrdil, když odvolání obžalovaného zamítl jako nedůvodné. Řízení tehdy soudy vedly jako proti uprchlému.

Zatčen v Austrálii
Ondráček po činu za ukradené peníze cestoval po světě, mj. byl na Fidži, v Japonsku a také v Austrálii, kde byl 22.listopadu 2013 na základě mezinárodního zatykače zadržen a pak nepřetržitě držen v předběžné vazbě až do 19. září 2020, kdy byl propuštěn na svobodu.

„Pak se vrátil domů a požádal o zrušení odsuzujících rozsudků,“ řekl Novinkám mluvčí Vrchního soudu v Olomouci Stanislav Cik s tím, že v opakovaném hlavním líčení byl předloni 17. července odsouzen na čtyři roky za mříže. „Tento rozsudek jsme zrušili a případ vrátili krajskému soudu, aby se vypořádal řádně s obhajobou obžalovaného. Ten to udělal loni 8. dubna a my jsme dnes (ve středu) tento trest potvrdili,“ popsal mluvčí.

Svědci ho s taškou viděli
Důkazy, především výpovědi svědků, kteří uvedli, že Ondráčka viděli s igelitkou s penězi, ho podle soudu jednoznačně usvědčily. „O vině obžalovaného svědčilo i jeho chování bezprostředně po činu, tedy rychlý úprk z České republiky na protilehlý konec zeměkoule,“ podotkl Cik.

Ondráček 5. ledna 2012 využil toho, že jeho známý nedával chvíli pozor, a igelitovou tašku s bankovkami o hodnotě převážně 500 eur ukradl ze stolu v bytě v Uherském Hradišti. Odjel do Brna a odtud pokračoval letecky do Prahy.

Tam přemluvil kamarádku ke společné dovolené na Novém Zélandu a druhý den skutečně odletěli. Dívka se pak vrátila sama poté, co jí rodiče napsali, že Ondráčka hledá policie. Jeho advokátka pak u prvního soudního jednání tvrdila, že rychle zmizel z Česka nikoliv ze strachu z policie, ale ze známého, jenž ho údajně zatahoval do mafiánských praktik.
"""

        # Generate song lyrics
        Actor.log.info("Generating the song lyrics")
        lyrics = generate_lyrics(content)
        print(lyrics)

        # Generate song.
        api_key = actor_input.get('topmediai_api_key')
        Actor.log.info(f"Generating song using: {api_key}")
        song_link = generate_song(lyrics=content, api_key = api_key, genre= "Hip Hop")
        kvs = await Actor.open_key_value_store()
        kvs.set_value(key="generated_song", value=song_link)
