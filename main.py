import sys
from tabnanny import check
import time
import json
import random
import asyncio
import logging
import concurrent.futures
from typing import List, Optional

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from discord.ext import commands
from discord_webhook import DiscordEmbed

from source.identify import Pokefier
from source.utilities import (
    extract_pokemon_data,
    load_pokemon_data,
    remove_diacritics,
    read_config,
    send_log,
    solve,
)
from source.messages import *

# ========================================== LOGGING ========================================= #

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def log_message(level: str, message: str) -> None:
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
    else:
        logger.info(message)


logger.info("+ Initialized Logging")

# ========================================== CONFIG ========================================== #

config = read_config()
logger.info("+ Initialized Config")

DELAY = config["DELAY"]
TOKENS = config["TOKENS"]
LOGGING = config["LOGGING"]
OWNER_ID = config["OWNER_ID"]
LANGUAGES = config["LANGUAGES"]
POKETWO_ID = config["POKETWO_ID"]
SPAM = config["SPAM"]["ENABLED"]
INTERVAL = config["SPAM"]["TIMING"]
SPAM_ID = config["SPAM"]["SPAM_ID"]
WEBHOOK_URL = config["WEBHOOK_URL"]
BLACKLISTED_POKEMONS = config["BLACKLISTED_POKEMONS"]
WHITELISTED_CHANNELS = config["WHITELISTED_CHANNELS"]

pokefier = Pokefier(num_interpreters=max(8, len(config["TOKENS"]) * 2))

BOT_THREAD_POOL = concurrent.futures.ThreadPoolExecutor(
    max_workers=max(10, len(config["TOKENS"]) * 3)
)


def load_config():
    try:
        with open("source/config.json", "r") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        logger.error("Config File Not Found")
        return {}
    except json.JSONDecodeError:
        logger.error("Error Decoding JSON COnfig File")
        return {}
    except Exception as e:
        logger.error(f"Unexpected Error : {e}")
        return {}


def check_config(key: str):
    try:
        with open("source\config.json", "r") as file:
            config = json.load(file)

        if key in config:
            return config[key]
        else:
            logger.warning(f"Key {key} Not Found In Config.")
            return None

    except Exception as e:
        logger.error(f"Error Reading Config: {e}")
        return None


def update_config(key: str, value: str):
    try:
        with open("source\config.json", "r") as file:
            config = json.load(file)

        config[key] = value

        with open("source\config.json", "w") as file:
            json.dump(config, file, indent=4)

        logger.info(f"Updated config: {key} = {value}")

    except Exception as e:
        logger.error(f"Error Updating Config: {e}")


# ========================================== SPAM ========================================== #


def spam() -> str:
    with open("messages/messages.txt", "r", encoding="utf-8", errors="ignore") as file:
        messages = file.readlines()
    return random.choice(messages).strip()


# ========================================== AUTOCATCHER CLASS ========================================== #


class Autocatcher(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=None, self_bot=False)
        self.spam_id = SPAM_ID
        self.interval = INTERVAL
        self.languages: List[str] = LANGUAGES
        self.pokemon_data = load_pokemon_data()
        self.whitelisted_channels: List[int] = WHITELISTED_CHANNELS
        self.blacklisted_pokemons: List[str] = BLACKLISTED_POKEMONS

    async def get_alternate_pokemon_name(
        self, name: str, languages: List[str] = LANGUAGES
    ) -> str:
        pokemon = next(
            (p for p in self.pokemon_data if p["name"].lower() == name.lower()), None
        )
        if pokemon:
            alternate_names = [
                alt_name
                for alt_name in pokemon.get("altnames", [])
                if alt_name.get("language").lower() in languages
            ]
            if alternate_names:
                return random.choice(alternate_names)["name"].lower()
        return name.lower()


# ========================================== MAIN FUNCTIONS ========================================== #


async def run_autocatcher(token: str) -> None:
    bot = Autocatcher()
    bot.remove_command("help")

    @bot.event
    async def on_ready() -> None:
        logger.info("+ ============== Pokefier ============== +")
        logger.info(f"+ Logged In : {bot.user} (ID: {bot.user.id})")
        logger.info("+ ============== Config ================ +")
        logger.info(f"+ Languages: {bot.languages}")
        logger.info(f"+ Whitelisted Channels: {bot.whitelisted_channels}")
        logger.info(f"+ Blacklisted Pokemons: {bot.blacklisted_pokemons}")
        logger.info("+ ====================================== +")
        bot.started = time.time()
        bot.command_prefix = f"<@{bot.user.id}> "
        logger.info(f"+ Bot Prefix: {bot.command_prefix}")

        await bot.load_extension("commands.poketwo")
        logger.info("+ Loaded Poketwo Commands")

        await bot.load_extension("commands.utilities")
        logger.info("+ Loaded Utilities Commands")

        await bot.load_extension("commands.channel")
        logger.info("+ Loaded Channel Commands")

        await bot.load_extension("commands.language")
        logger.info("+ Loaded Language Commands")

        bot.verified = True
        bot.pokemons_caught = 0

    @bot.event
    async def on_message(message) -> None:
        await bot.process_commands(message)

        if (
            message.author.id == POKETWO_ID
            and message.channel.id in bot.whitelisted_channels
        ):
            logger.info("Message Received From POKETWO")
            logger.info("Attempting To Process Message")

            if "requesting a trade with" in message.content.lower():
                logger.info("Trade Request Received")
                try:
                    if message.components[0].children[0].label.lower() == "accept":
                        time.sleep(random.choice(DELAY))
                        await message.components[0].children[0].click()
                    logger.info("Trade Accepted")
                except Exception as e:
                    logger.error(f"Error in trade acceptance: {e}")

            if message.embeds:
                embed = message.embeds[0]
                if (
                    embed.author
                    and "are you sure you want to confirm this trade? please make sure that you are trading what you intended to."
                    in embed.author.name.lower()
                ):
                    logger.info("Trade Confirmation Received")
                    if message.components[0].children[0].label.lower() == "confirm":
                        time.sleep(random.choice(DELAY))
                        await message.components[0].children[0].click()
                    logger.info("Trade Completed")

            if "are you sure you want to exchange" in message.content.lower():
                logger.info("A Shard Buy Message Received")
                try:
                    if message.components[0].children[0].label.lower() == "confirm":
                        time.sleep(random.choice(DELAY))
                        await message.components[0].children[0].click()
                    logger.info("Shard Bought")
                except Exception as e:
                    logger.error(f"Error in shard buying: {e}")

            if "you don't have enough shards" in message.content.lower():
                logger.info("Not Enough Shards To Buy Incense")
                await message.channel.send("Not Enough Shards To Buy Incense")
                await message.channel.send(
                    f"To Buy Shards Use `{bot.command_prefix}shardbuy <amount>`"
                )

            # ========================================== SPAWN HANDLING ========================================== #
            incense = ""
            remaining_spawns = ""
            spawn_interval = ""
            time_left = ""

            if message.embeds:
                if (
                    message.channel.id in bot.whitelisted_channels
                    and message.embeds[0].title
                    and "wild" in message.embeds[0].title.lower()
                    and bot.verified
                ):
                    logger.info("A Pokémon Spawned - Attempting To Predict")
                    if message.embeds[0].footer.text:
                        footer = message.embeds[0].footer.text.split("\n")
                        incense = footer[0]
                        remaining_spawns = footer[1]
                        spawn_interval = footer[2]
                        time_left = footer[3].split("at")[0]

                    pokemon_image = message.embeds[0].image.url
                    predicted_pokemons = await pokefier.predict_pokemon_from_url(
                        pokemon_image
                    )
                    predicted_pokemon = max(predicted_pokemons, key=lambda x: x[1])
                    name = predicted_pokemon[0]
                    score = predicted_pokemon[1]

                    bot.blacklisted_pokemons = [
                        pokemon_name.lower()
                        for pokemon_name in bot.blacklisted_pokemons
                    ]
                    if name.lower() in bot.blacklisted_pokemons:
                        logger.info(
                            f"Pokémon : {name} Was Not Caught Because It Is Blacklisted"
                        )
                        return

                    if score > 30.0:
                        alt_name = await bot.get_alternate_pokemon_name(
                            name, languages=bot.languages
                        )
                        alt_name = remove_diacritics(alt_name)
                        time.sleep(random.choice(DELAY))
                        await message.channel.send(
                            f"<@716390085896962058> c {alt_name}"
                        )
                        logger.info(f"Predicted Pokémon : {name} With Score : {score}")
                    else:
                        logger.info(f"Predicted Pokémon : {name} With Score : {score}")
                        await message.channel.send("<@716390085896962058> h")

            if (
                "that is the wrong pokémon" in message.content.lower()
                and bot.verified
                and message.channel.id in bot.whitelisted_channels
            ):
                logger.info("Wrong Pokémon Detected")
                await message.channel.send("<@716390085896962058> h")
                logger.info("Requested Hint For Wrong Pokémon")

            if (
                "the pokémon is" in message.content.lower()
                and bot.verified
                and message.channel.id in bot.whitelisted_channels
            ):
                logger.info("Solving The Hint")
                hint = solve(message.content)
                time.sleep(random.choice(DELAY))
                await message.channel.send(f"<@716390085896962058> c {hint[0]}")
                logger.info("Hint Solved")

            if (
                "congratulations" in message.content.lower()
                and bot.verified
                and message.channel.id in bot.whitelisted_channels
            ):
                bot.pokemons_caught += 1
                is_shiny = "these colors" in message.content.lower()

                pokemon_data = extract_pokemon_data(message.content)
                pokemon = next(
                    (
                        p
                        for p in bot.pokemon_data
                        if p["name"].lower() == pokemon_data["name"].lower()
                    ),
                    None,
                )

                embed1 = DiscordEmbed(title="A Pokemon Was Caught!", color="03b2f8")
                embed1.set_description(
                    f"Account Name : {bot.user.name}\n\nPokémon Name : {pokemon_data['name']}\n\nPokémon Level : {pokemon_data['level']}\nPokémon IV : {pokemon_data['IV']}%\n\nShiny : {is_shiny}\nRarity : {pokemon['rarity']}\n\nPokémons Caught : {bot.pokemons_caught}"
                )
                embed1.set_author(
                    name="Pokefier",
                    url="https://github.com/sayaarcodes/pokefier",
                    icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
                )
                embed1.set_thumbnail(url=pokemon["image"]["url"])
                embed1.set_timestamp()

                if incense == "Incense: Active.":
                    embed2 = DiscordEmbed(title="Incense Details", color="03b2f8")
                    embed2.set_description(
                        f"Remaining Spawns : {remaining_spawns}\nSpawn Interval : {spawn_interval}\nTime Left : {time_left}"
                    )
                    embed2.set_author(
                        name="Pokefier",
                        url="https://github.com/sayaarcodes/pokefier",
                        icon_url="https://raw.githubusercontent.com/sayaarcodes/pokefier/main/pokefier.png",
                    )
                    embed2.set_thumbnail(url=pokemon["image"]["url"])
                    embed2.set_timestamp()

                    send_log(embed=embed2, WEBHOOK_URL=WEBHOOK_URL)

                send_log(embed=embed1, WEBHOOK_URL=WEBHOOK_URL)

            if (
                f"https://verify.poketwo.net/captcha/{bot.user.id}" in message.content
                and bot.verified
            ):
                logger.info("A Captcha Challenge Was Received")
                bot.verified = False
                await message.channel.send("<@716390085896962058> incense pause")
                logger.info("Incense Paused")
                owner_dm = await bot.fetch_user(OWNER_ID)
                await owner_dm.send(
                    f"Captcha Challenge Received. Please Solve It.\n\n{message.content}"
                )
                logger.info("Captcha Challenge Sent To Owner")

    await bot.start(token)


async def main(tokens: List[str]) -> None:
    ac_tasks = [run_autocatcher(token) for token in tokens]
    await asyncio.gather(*ac_tasks)


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main(TOKENS))
    finally:
        loop.close()
