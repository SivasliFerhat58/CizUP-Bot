from discord.ext import commands

class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="merhaba", description="Merhaba der.")
    async def merhaba(self, ctx):
        await ctx.send("Merhaba!")

bot = commands.Bot("token")
bot.add_cog(MyCommands(bot))

bot.run("MTE4NjAwNTk1NzM3ODA0ODExMQ.GtiyvT.8r2V9vHzNCOTvfT2ptGfPbOPXADh6XuWRNtK78")