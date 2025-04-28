import discord
from discord.ext import commands
from main import OWNER_ID, POKETWO_ID, check_config, update_config, logger


class PoketwoCommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blacklistadd(self, ctx, *pokemons: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not pokemons:
                await ctx.reply(
                    "`You Must Provide At Least One Pokemon. Separate Multiple Pokemons With Spaces.`"
                )
                return
            message = "```\n"

            laoded_blacklist = check_config("BLACKLISTED_POKEMONS")
            for pokemon in pokemons:
                try:
                    if pokemon.lower() in laoded_blacklist:
                        message += f"Pokemon : {pokemon} Is Already Blacklisted\n"
                    else:
                        laoded_blacklist.append(pokemon.lower())
                        update_config("BLACKLISTED_POKEMONS", laoded_blacklist)
                        message += f"Pokemon : {pokemon} Added To Blacklist\n"
                except ValueError:
                    await ctx.reply(
                        f"Invalid Pokemon : `{pokemon}`. Please Provide A Valid Pokemon Name."
                    )

            message += "```"
            await ctx.send(message)

    @commands.command()
    async def blacklistremove(self, ctx, *pokemons: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not pokemons:
                await ctx.reply(
                    "`You Must Provide At Least One Pokemon. Separate Multiple Pokemons With Spaces.`"
                )
                return
            message = "```\n"

            loaded_blacklist = check_config("BLACKLISTED_POKEMONS")
            for pokemon in pokemons:
                try:
                    if pokemon.lower() not in loaded_blacklist:
                        message += f"Pokemon : {pokemon} Is Not Blacklisted\n"
                    else:
                        loaded_blacklist.remove(pokemon.lower())
                        update_config("BLACKLISTED_POKEMONS", loaded_blacklist)
                        message += f"Pokemon : {pokemon} Removed From Blacklist\n"
                except ValueError:
                    await ctx.reply(
                        f"Invalid Pokemon : `{pokemon}`. Please Provide A Valid Pokemon Name."
                    )

            message += "```"
            await ctx.send(message)

    @commands.command()
    async def incense(self, ctx, time: str, inter: str) -> None:
        if ctx.author.id in OWNER_ID:
            if time in ["30m", "1h", "3h", "1d"] and inter in ["10s", "20s", "30s"]:
                await ctx.send(f"<@{POKETWO_ID}> incense buy {time} {inter} -y")
            else:
                await ctx.send(
                    f"Invalid Usage. Correct Usage: `{self.bot.command_prefix}incense <time> <interval>`"
                )
                await ctx.send("Time : 30m, 1h, 3h, 1d")
                await ctx.send("Interval : 10s, 20s, 30s")

    @commands.command()
    async def shardbuy(self, ctx, amt: int) -> None:
        if ctx.author.id in OWNER_ID:
            if amt > 0:
                await ctx.send(f"<@{POKETWO_ID}> buy shards {amt}")
            else:
                await ctx.send(
                    f"Invalid Usage. Correct Usage: `{self.bot.command_prefix}shardbuy <amount>`"
                )

    @commands.command()
    async def trade(self, ctx, user: str) -> None:
        if ctx.author.id in OWNER_ID:
            await ctx.send(f"<@{POKETWO_ID}> trade {user}")
            logger.info(f"Trade Request Sent To {user}")


async def setup(bot):
    await bot.add_cog(PoketwoCommandHandler(bot))
