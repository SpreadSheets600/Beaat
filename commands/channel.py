from discord.ext import commands
from main import OWNER_ID, check_config, update_config


class ChannelCommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def channeladd(self, ctx, *channel_ids: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not channel_ids:
                await ctx.reply(
                    "`You Must Provide At Least One Channel ID. Separate Multiple IDs With Spaces.`"
                )
                return
            message = "```\n"

            loaded_channel_ids = check_config("WHITELISTED_CHANNELS")
            print(channel_ids)

            for channel_id in channel_ids:
                try:
                    if channel_id in loaded_channel_ids:
                        message += f"Channel ID : {channel_id} Is Already Whitelisted\n"
                    else:
                        loaded_channel_ids.append(int(channel_id))

                        update_config("WHITELISTED_CHANNELS", loaded_channel_ids)

                        message += f"Channel ID : {channel_id} Added To Whitelist\n"

                except ValueError:
                    await ctx.reply(
                        f"Invalid Channel ID : `{channel_id}`. Please Provide A Valid Numeric Channel ID."
                    )

            message += "```"
            await ctx.send(message)

    @commands.command()
    async def channelremove(self, ctx, *channel_ids: str) -> None:
        if ctx.author.id in OWNER_ID:
            if not channel_ids:
                await ctx.reply(
                    "`You Must Provide At Least One Channel ID. Separate Multiple IDs With Spaces.`"
                )
                return
            message = "```\n"

            loaded_channel_ids = check_config("WHITELISTED_CHANNELS")
            print(channel_ids)

            for channel_id in channel_ids:
                try:
                    if channel_id in loaded_channel_ids:
                        message += f"Channel ID : {channel_id} Is Already Whitelisted\n"
                    else:
                        loaded_channel_ids.remove(int(channel_id))

                        update_config("WHITELISTED_CHANNELS", loaded_channel_ids)

                        message += f"Channel ID : {channel_id} Removed From Whitelist\n"

                except ValueError:
                    await ctx.reply(
                        f"Invalid Channel ID : `{channel_id}`. Please Provide A Valid Numeric Channel ID."
                    )

            message += "```"
            await ctx.send(message)


async def setup(bot):
    await bot.add_cog(ChannelCommandHandler(bot))
