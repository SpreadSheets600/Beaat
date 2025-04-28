import discord
from discord.ext import commands
from main import OWNER_ID, POKETWO_ID, check_config, update_config, load_config, logger


class UtilitiesCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        if ctx.author.id in OWNER_ID:
            message = (
                "```diff\n"
                "Available Commands:\n"
                "\n"
                " shard           -> Buy Shards\n"
                " help            -> View This Help Message\n"
                " say             -> Make The Bot Say Something\n"
                " ping            -> Check If The Bot Is Online\n"
                "\n"
                " trade           -> Request A Trade With A User\n"
                " config          -> View The Current Configuration\n"
                " solved          -> Confirm That The Captcha Was Solved\n"
                "\n"
                " incense         -> Start The Incense\n"
                " resume          -> Resume The Incense\n"
                " pause           -> Pause The Incense\n"
                "\n"
                " channeladd      -> Add A Channel To The Whitelist\n"
                " channelremove   -> Remove A Channel From The Whitelist\n"
                "\n"
                " blacklistadd    -> Add A Pokémon To The Blacklist\n"
                " blacklistremove -> Remove A Pokémon From The Blacklist\n"
                "\n"
                " languageadd     -> Add A Language To The Language List\n"
                " languageremove  -> Remove A Language From The Language List\n"
                "```"
            )
            await ctx.send(message)

    @commands.command()
    async def ping(self, ctx) -> None:
        if ctx.author.id in OWNER_ID:
            await ctx.send(f"Latency: {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def solved(self, ctx) -> None:
        if ctx.author.id in OWNER_ID:
            self.bot.verified = True
            await ctx.send("Thanks Dude! I Will Continue The Grind")
            await ctx.send(f"<@{POKETWO_ID}> incense resume")
            logger.info("Captcha Solved - Self Bot Booted")

    @commands.command()
    async def pause(self, ctx) -> None:
        if ctx.author.id in OWNER_ID:
            self.bot.verified = False
            await ctx.send("Thanks Dude! I Will Pause The Grind")
            await ctx.send(f"<@{POKETWO_ID}> incense pause")
            logger.info("Captcha Solved - Self Bot Paused")

    @commands.command()
    async def resume(self, ctx) -> None:
        if ctx.author.id in OWNER_ID:
            self.bot.verified = True
            await ctx.send("Thanks Dude! I Will Continue The Grind")
            await ctx.send(f"<@{POKETWO_ID}> incense resume")
            logger.info("Captcha Solved - Self Bot Booted")

    @commands.command()
    async def config(self, ctx) -> None:
        if ctx.author.id in OWNER_ID:

            loaded_config = load_config()
            self.bot.whitelisted_channels = loaded_config["WHITELISTED_CHANNELS"]
            self.bot.blacklisted_pokemons = loaded_config["BLACKLISTED_POKEMONS"]
            self.bot.languages = loaded_config["LANGUAGES"]

            message = f"```PREFIX: {self.bot.command_prefix}\nOWNER_ID: {OWNER_ID}\n\nWHITELISTED_CHANNELS = {self.bot.whitelisted_channels}\nBLACKLISTED_POKEMONS={self.bot.blacklisted_pokemons}\n\nLANGUAGES = {self.bot.languages}```"
            await ctx.reply(message)

    @commands.command()
    async def say(self, ctx, *, message: str) -> None:
        if ctx.message.author.id in OWNER_ID:
            if "p2" in message.lower():
                message = message.replace("p2", f"<@{POKETWO_ID}>")
                await ctx.send(message)
            else:
                await ctx.send(message)


async def setup(bot):
    await bot.add_cog(UtilitiesCommandCog(bot))
