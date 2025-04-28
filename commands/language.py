from discord.ext import commands
from main import OWNER_ID, check_config, update_config


class LanguageCommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def languageadd(self, ctx, *languages: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not languages:
                await ctx.reply(
                    "`You Must Provide At Least One Language. Separate Multiple Languages With Spaces.`"
                )
                return
            message = "```\n"

            valid_languages = ["english", "french", "german", "japanese"]
            loaded_languages = check_config("LANGUAGES")

            for language in languages:
                try:
                    if language.lower() not in valid_languages:
                        await ctx.reply(
                            f"Invalid Language : `{language}`. Please Provide A Valid Language Used By Poketwo."
                        )
                        continue
                    if language.lower() in loaded_languages:
                        message += f"Language : {language} Is Already Added\n"
                    else:
                        loaded_languages.append(language.lower())
                        update_config("LANGUAGES", loaded_languages)
                        message += f"Language : {language} Added\n"

                except ValueError:
                    await ctx.reply(
                        f"Invalid Language : `{language}`. Please Provide A Valid Language Used By Poketwo."
                    )
            message += "```"
            await ctx.send(message)

    @commands.command()
    async def languageremove(self, ctx, *languages: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not languages:
                await ctx.reply(
                    "`You Must Provide At Least One Language. Separate Multiple Languages With Spaces.`"
                )
                return
            message = "```\n"

            valid_languages = ["english", "french", "german", "japanese"]
            loaded_languages = check_config("LANGUAGES")

            for language in languages:
                try:
                    if language.lower() not in valid_languages:
                        await ctx.reply(
                            f"Invalid Language : `{language}`. Please Provide A Valid Language Used By Poketwo."
                        )
                        continue
                    if language.lower() not in loaded_languages:
                        message += f"Language : {language} Is Not Added\n"
                    else:
                        loaded_languages.remove(language.lower())
                        update_config("LANGUAGES", loaded_languages)
                        message += f"Language : {language} Removed\n"

                except ValueError:
                    await ctx.reply(
                        f"Invalid Language : `{language}`. Please Provide A Valid Language Used By Poketwo."
                    )

            message += "```"
            await ctx.send(message)


async def setup(bot):
    await bot.add_cog(LanguageCommandHandler(bot))
