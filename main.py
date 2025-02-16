import time
import random
import asyncio
import logging
from discord.ext import commands
from discord_webhook import DiscordEmbed
from Source.PKIdentify import Pokefier
from Source.Utilities import (
    extract_pokemon_data,
    load_pokemon_data,
    remove_diacritics,
    read_config,
    send_log,
    solve,
)

pokefier = Pokefier()
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

config = read_config()
DELAY = config["DELAY"]
TOKENS = config["TOKENS"]
OWNER_ID = config["OWNER_ID"]
LANGUAGES = config["LANGUAGES"]
POKETWO_ID = config["POKETWO_ID"]
SPAM_ID = config["SPAM"]["SPAM_ID"]
INTERVAL = config["SPAM"]["TIMING"]
BLACKLISTED_POKEMONS = config["BLACKLISTED_POKEMONS"]
WHITELISTED_CHANNELS = config["WHITELISTED_CHANNELS"]

def spam():
    with open("Messages/Messages.txt", "r", encoding="utf-8", errors="ignore") as file:
        messages = file.readlines()
    return random.choice(messages).strip()

class Autocatcher(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None, self_bot=False)
        self.spam_id = SPAM_ID
        self.interval = INTERVAL
        self.languages = LANGUAGES
        self.pokemon_data = load_pokemon_data()
        self.whitelisted_channels = WHITELISTED_CHANNELS
        self.blacklisted_pokemons = BLACKLISTED_POKEMONS

    async def get_alternate_pokemon_name(self, name, languages=LANGUAGES):
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

async def run_autocatcher(token):
    bot = Autocatcher()

    @bot.event
    async def on_ready():
        bot.load_extension("handler.command")
        bot.started = time.time()
        bot.command_prefix = f"<@{bot.user.id}> "
        bot.verified = True
        bot.pokemons_caught = 0

    @bot.command()
    async def ping(ctx):
        await ctx.send("Pong!")
        await ctx.send(f"Latency : {round(bot.latency * 1000)}ms")

    @bot.command()
    async def incense(ctx, time: str, inter: str):
        if ctx.author.id != OWNER_ID:
            if time in ["30m", "1h", "3h", "1d"] and inter in ["10s", "20s", "30s"]:
                await ctx.send(f"<@{POKETWO_ID}> incense buy {time} {inter} -y")

    @bot.command()
    async def shardbuy(ctx, amt: int):
        if ctx.author.id == OWNER_ID and amt > 0:
            await ctx.send(f"<@{POKETWO_ID}> buy shards {amt}")

    @bot.command()
    async def channeladd(ctx, *channel_ids):
        if not channel_ids:
            await ctx.reply("`You Must Provide Atleast One Channel ID. Separate Multiple IDs With Spaces.`")
            return
        message = "```\n"
        for channel_id_str in channel_ids:
            try:
                channel_id = int(channel_id_str)
            except ValueError:
                await ctx.reply(f"Invalid Channel ID : `{channel_id_str}`. Please Provide A Valid Numeric Channel ID.")
                continue
            if channel_id in bot.whitelisted_channels:
                message += f"Channel ID : {channel_id} Is Already Whitelisted\n"
            else:
                bot.whitelisted_channels.append(channel_id)
                message += f"Channel ID : {channel_id} Whitelisted\n"
        message += "```"
        await ctx.send(message)

    @bot.command()
    async def channelremove(ctx, *channel_ids):
        if not channel_ids:
            await ctx.reply("`You Must Provide Atleast One Channel ID. Separate Multiple IDs With Spaces.`")
            return
        message = "```\n"
        for channel_id_str in channel_ids:
            try:
                channel_id = int(channel_id_str)
            except ValueError:
                await ctx.reply(f"Invalid Channel ID : `{channel_id_str}`. Please Provide A Valid Numeric Channel ID.")
                continue
            if channel_id in bot.whitelisted_channels:
                bot.whitelisted_channels = [
                    ch_id for ch_id in bot.whitelisted_channels if ch_id != channel_id
                ]
                message += f"Channel ID : {channel_id} Removed From Whitelist\n"
            else:
                message += f"Channel ID : {channel_id} Is Not Whitelisted\n"
        message += "```"
        await ctx.send(message)

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)
        if message.author.id == POKETWO_ID and message.channel.id in bot.whitelisted_channels:
            if "requesting a trade with" in message.content.lower():
                if message.components and message.components[0].children:
                    await time.sleep(random.choice(DELAY))
                    await message.components[0].children[0].click()
            if message.embeds:
                if "are you sure you want to confirm this trade?" in message.embeds[0].description.lower():
                    if message.components and message.components[0].children:
                        await time.sleep(random.choice(DELAY))
                        await message.components[0].children[0].click()

    await bot.start(token)

async def main(tokens):
    ac_tasks = [run_autocatcher(token) for token in tokens]
    await asyncio.gather(*ac_tasks)

if __name__ == "__main__":
    asyncio.run(main(TOKENS))
