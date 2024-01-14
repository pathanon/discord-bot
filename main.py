import discord
from discord.ext import commands
from discord import app_commands
import random
from myserver import server_on
import os

from PIL import Image
from bs4 import BeautifulSoup
import requests
from io import BytesIO

menu_page = "https://www.unileverfoodsolutions.co.th"
# url = "https://www.unileverfoodsolutions.co.th/th/recipes/%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%A0%E0%B8%97%E0%B9%80%E0%B8%A1%E0%B8%99%E0%B8%B9_%E0%B8%AD%E0%B8%B2%E0%B8%AB%E0%B8%B2%E0%B8%A3%E0%B9%84%E0%B8%97%E0%B8%A2.html"
menu_url = "https://www.unileverfoodsolutions.co.th/th/recipes/%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%A0%E0%B8%97%E0%B9%80%E0%B8%A1%E0%B8%99%E0%B8%B9_%E0%B8%AD%E0%B8%B2%E0%B8%AB%E0%B8%B2%E0%B8%A3%E0%B9%84%E0%B8%97%E0%B8%A2.html?start=13"
menu_response = requests.get(menu_url)
menu_page_html = BeautifulSoup(menu_response.text,'html.parser')
menu_name_all = menu_page_html.find_all('span',class_='item-list__title')
menu_url_all = menu_page_html.find_all('div',class_="item-list__body span-3")

def get_menu_info(idx):
    name_ = menu_name_all[idx]
    url_ = menu_url_all[idx]
    inst_url = menu_page+url_.a["href"]
    # print(f"ชื่อเมนู : {name_}\n เว็บสูตรอาหาร {inst_url} \n")
    response_inst = requests.get(inst_url)
    inst_html = BeautifulSoup(response_inst.text,'html.parser')
    img_name = inst_html.find('figure',class_="recipe-image-v2 js-recipe-image-v2")
    if img_name==None:
        img_name = inst_html.find('picture')
        img_name = menu_page+img_name.img["src"]
    else:
        img_name = img_name.img["src"]
    instructions_ = inst_html.find('ol',class_="instructions")
    inst_list = [inst.text for inst in instructions_.li.ul.find_all('li')]
    # print("\nเว็บรุปภาพ\n",img_name)
    # print("\nสูตรอาหาร\n")
    # print(inst_list)
    finale = {"name":name_.text,
              "inst_url":inst_url,
              "img_url":img_name,
              "inst_list":inst_list}
    return finale

def generate_text_bot(info_):
    name = info_["name"]
    # inst_url = info_["inst_url"]
    img_url = info_["img_url"]
    inst = info_["inst_list"]
    name_format = f"ชื่อเมนู : {name}\n" 
    # name_format = f"เว็บสูตรอาหาร : {inst_url}"
    # name_format = f"เว็บรุปภาพ : {img_url}"
    inst_format = "สูตรอาหาร"
    for idx,cont in enumerate(inst):
        inst_format+=f"\n{idx+1}. {cont}"
    # print(inst_format)
    return name_format+inst_format

def get_menu_all():
    return [menu_name.text for menu_name in menu_name_all]

def get_info_byname(name_):
    all_listed = get_menu_all()
    if name_ in all_listed:
        test_index = all_listed.index(name_)
        output_string = generate_text_bot(get_menu_info(test_index))
    else:
        output_string = "เมนูนี้ไม่อยู่ในคลังขอโทษด้วยครับผม"
    return output_string

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
# TOKEN='<TOKEN>'
TOKEN = os.getenv('token')
food_list = get_menu_all()

@bot.event
async def on_ready():
    print("Bot Online!")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1195666668156883005) # ID Channel
    text = f"Welcome {member.mention} to server test-bot-channel!"
    embedding = discord.Embed(title='Welcome to the server',
                              description= text,
                              color = 0x66FFFF)

    await channel.send(text) # sending text messege "welcome"
    await channel.send(embed=embedding)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1195666668156883005) # ID Channel
    text = f"{member.mention} has left server test-bot-channel!"
    await channel.send(text) # sending text messege "welcome"

@bot.event
async def on_message(message):
    mes = message.content # pull message
    if mes.lower() == 'hello':
        await message.channel.send("Hey! How are you?")
    elif mes.lower() == 'hi bot':
        await message.channel.send(f"Hi {message.author.name}! How are you?")
    await bot.process_commands(message)

# @bot.command()
# async def hello(ctx):
#     await ctx.send(f"Hi {ctx.author.name}!")

# @bot.command()
# async def test(ctx,arg):
#     await ctx.send(arg)
@bot.tree.command(name='help',description='Bot Commands')
async def helpcommand(interaction):
    embeds = discord.Embed(title="Help Me! - Bot Commands",
                           description="Bot Commands",
                           color=0x66FFFF,
                           timestamp=discord.utils.utcnow())
    embeds.add_field(name="/help",   value="Showing all command(s)",   inline=False)
    embeds.add_field(name="/hello", value="Greetings with bots",    inline=False)
    embeds.add_field(name="/random-food",   value="Bot will randomly pick 1 food for you or may be not!",   inline=False)
    embeds.add_field(name="/how-to-cook", value="typing the menu and return instructions",    inline=False)
    embeds.add_field(name="/dog-cat", value="add an image of anything and it will return dog or cat",    inline=False)
    embeds.add_field(name="/classify", value="add an image of plant and return classified diseases and treatments",    inline=False)
    embeds.add_field(name="/regconize", value="add an image of plant and return name of plant",    inline=False)
    

    # embeds.set_author(name='Author',url="",icon_url="")
    # embeds.set_thumbnail(url='')
    # embeds.set_image(url='')
    # embeds.set_footer(url='')
    await interaction.response.send_message(embed=embeds)

@bot.tree.command(name='hello',description='Replies with Hello')
async def hello(interaction):
    await interaction.response.send_message('Hello World!')

@bot.tree.command(name='random-food',description='Randomly pick me some food menu!')
async def randfood(interaction):
    random_menu = random.choice(get_menu_all())
    # await interaction.response.send_message(f'ทำอะไรกินดี...งั้นลอง {random_menu} ไหมครับ\n')
    await interaction.response.send_message(get_info_byname(random_menu))


@bot.tree.command(name='how-to-cook',description='typing the menu and return instructions')
@app_commands.describe(name='typing the menu')
async def listingred(interaction, name:str):
    await interaction.response.send_message(get_info_byname(name))

# @bot.tree.command(name='dog-cat',description='add an image of anything and it will return dog or cat')
# @app_commands.describe(img='add file path of the image')
# async def dogcatimage(interaction, img:str):
#     with open(my_filename,"rb") as fh:
#         f = discord.File(fh,filename=my_filename)
    
#     # embeds = discord.Embed(title="Dog or Cat! - Let Me Guess",
#     #                        description="It's Dog",
#     #                        color=0x66FFFF,
#     #                        timestamp=discord.utils.utcnow(),
#     #                        set_image=img)
#     await interaction.send(file=f)

server_on()
bot.run(TOKEN)