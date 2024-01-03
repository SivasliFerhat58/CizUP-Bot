import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction
from discord.ui import Button, View
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


guild_id = 1183852227148918895


firefox_options = Options()
firefox_options.add_argument('--headless')
driver = webdriver.Firefox(options=firefox_options)

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

@client.event
async def on_ready():
    driver.get("https://chat.chatgptdemo.ai/")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("/"):
        await client.process_commands(message)
        return
    
            
    guild = client.get_guild(guild_id)
    member = guild.get_member(message.author.id)

    # if not isinstance(message.channel, discord.DMChannel):
    for chapter in chapter_list:
        if not has_role(member, chapter["chapter_id"]):
            await message.channel.send(f"Sevgili {message.author.mention}, bu botu kullanabilmek için aktif bir CizUP'ta olman gerekiyor.")
            return
            
    text_area = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="post-2"]/div[2]/div/div[2]/textarea')))
    text_area.click()

    text_area.send_keys(message.content)
    text_area.send_keys(Keys.ENTER)

    time.sleep(5)

    response = driver.find_elements(By.CLASS_NAME, 'wpaicg-ai-message')

    await message.channel.send(response[-1].text[4:])

@client.command()
async def soruöner(ctx):
    guild = client.get_guild(guild_id)
    user = guild.get_member(ctx.author.id)
    for chapter in chapter_list:
        if has_role(user, chapter["chapter_id"]):
            view = ButtonView(user,chapter)
            await user.send(file = discord.File(chapter["example_1"]),view=view)
            break
        else:
            await user.send(f"Sevgili {user.mention}, bu komutu kullanabilmek için aktif bir CizUP'ta olman gerekiyor.")
            break

client.run("MTE4NjAwNTk1NzM3ODA0ODExMQ.GtiyvT.8r2V9vHzNCOTvfT2ptGfPbOPXADh6XuWRNtK78")