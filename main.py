import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction
from discord.ui import Button, View
import json

class ButtonView(View):
    def __init__(self, user,chapter):
        super().__init__(timeout=None)  
        self.user = user
        self.chapter = chapter
        self.click_counts = {"button_one": 0,"button_two": 0} 

    @discord.ui.button(label="Yeni Örnek Al (1/3)", style=ButtonStyle.green)
    async def button_one_callback(self, interaction: Interaction, button: Button):
        self.click_counts["button_one"] += 1
        new_label = f"Yeni Örnek Al ({self.click_counts['button_one']+1}/3)"
        button.label = new_label

        if self.click_counts["button_one"] >= 2:
            self.remove_item(button)
        
        await interaction.channel.send(file = discord.File(self.chapter[f"example_{self.click_counts['button_one']+1}"]),view=self)

    @discord.ui.button(label="Cevabı Gör", style=ButtonStyle.red)
    async def button_two_callback(self, interaction: Interaction, button: Button):
        self.click_counts["button_two"] += 1

        if self.click_counts["button_one"] >= 2:
            self.remove_item(button)
        
        await interaction.channel.send(file = discord.File(self.chapter[f"cevap_{self.click_counts['button_one']+1}"]))

with open('level.json', 'r') as f:
    chapter_list = json.load(f)

intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)

def has_role(member, role_id):
    return any(role.id == role_id for role in member.roles)

@client.command()
async def soruöner(ctx):
    user = ctx.author
    await ctx.message.delete()
    for chapter in chapter_list:
        if has_role(user, chapter["chapter_id"]):
            view = ButtonView(user,chapter)
            await user.send(file = discord.File(chapter["example_1"]),view=view)
            break
        else:
            await user.send(f"Sevgili {user.mention}, bu komutu kullanabilmek için CizUP'ta aktif olarak ilerliyor olman gerek.\nSeni de aramızda görmek isteriz. ➞ https://cizup.dev")
            break

client.run("MTE4NjAwNTk1NzM3ODA0ODExMQ.GtiyvT.8r2V9vHzNCOTvfT2ptGfPbOPXADh6XuWRNtK78")