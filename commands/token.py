from discord.ext import commands
from main import OWNER_ID, check_config, update_config


class TokenCommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tokenadd(self, ctx, *tokens: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not tokens:
                await ctx.reply(
                    "`You Must Provide At Least One Token. Separate Multiple Tokens With Spaces.`"
                )
                return
            message = "```\n"

            loaded_tokens = check_config("TOKENS")
            print(loaded_tokens)

            for token in tokens:
                try:
                    if token in loaded_tokens:
                        message += f"Token : {token} Is Already Added\n"

                    else:
                        loaded_tokens.append(token)

                        update_config("TOKENS", loaded_tokens)

                        message += f"Token : {token} Is Added Successfully\n"

                except ValueError:
                    message += f"Token : {token} Is Invalid\n"

            message += "```"
            await ctx.send(message)

    @commands.command()
    async def tokenremove(self, ctx, *token: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not token:
                await ctx.reply(
                    "`You Must Provide At Least One Token. Separate Multiple Tokens With Spaces.`"
                )
                return
            message = "```\n"

            loaded_tokens = check_config("TOKENS")
            print(loaded_tokens)

            for token in token:
                try:
                    if token in loaded_tokens:
                        loaded_tokens.remove(token)

                        update_config("TOKENS", loaded_tokens)

                        message += f"Token : {token} Is Removed Successfully\n"

                    else:
                        message += f"Token : {token} Is Not Added\n"

                except ValueError:
                    message += f"Token : {token} Is Invalid\n"

            message += "```"
            await ctx.send(message)


async def setup(bot):
    await bot.add_cog(TokenCommandHandler(bot))
