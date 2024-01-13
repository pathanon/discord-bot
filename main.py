import discord
from discord.ext import commands
from discord import app_commands
import random
from myserver import server_on
import os

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
# TOKEN='<TOKEN>'
TOKEN = os.getenv('token')
food_list = ["ข้าวหมูแดง",
             "ข้าวหมูกรอบ",
             "ข้าวผัดทะเลต้มยำ",
             "ห่อหมก",
             "ข้าวกระเพราหมูสับไข่ดาว",
             "ก๋วยเตี๋ยวหมูตุ๋น",
             "หอยทอด",
             "อะไรก็ได้โตแล้ว",
             "ไม่ต้องแดกสิ...ไอ่สัสแค่นี้ยังต้องให้กูคิด",
             "ผัดไท"]
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
    embeds.add_field(name="/list-ingredients", value="typing the menu and return list of ingredients",    inline=False)
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
async def hello(interaction):
    random_menu = random.choice(food_list)
    await interaction.response.send_message(f'กินอะไรดีอ่ะนะ...งั้นลอง {random_menu}')
    # await interaction.response.send_message(a)


@bot.tree.command(name='list-ingredients')
@app_commands.describe(name='typing the menu and return list of ingredients')
async def listingred(interaction, name:str):
    ingred_list = {
            "ข้าวหมูแดง":"หมูแดง กับ ข้าวเปล่า",
             "ข้าวหมูกรอบ":"มีแต่น้ำมัน",
             "ข้าวผัดทะเลต้มยำ":"ข้าว กับ ทะเล",
             "ห่อหมก":"ใบตอง กับ ปลา",
             "ข้าวกระเพราหมูสับไข่ดาว":"มีแต่ถัวฝักยาวหมูไม่เห็นมีเลย",
             "ก๋วยเตี๋ยวหมูตุ๋น":"แป้ง และ วิญญาณหมู",
             "หอยทอด":"หอย และ น้ำมัน",
             "ผัดไท":"อร่อยไม่ซ้ำจำสูตรไม่ได้",
             "unknown":"สั่งยากชิบหาย...ลองไป Google มั้ย"
    }
    if name in list(ingred_list.keys()):
        name_ = ingred_list[name]
    else: name_ = ingred_list["unknown"]
    await interaction.response.send_message(f'ถามว่ามีอะไรบ้าง.... {name_}')

server_on()
bot.run(TOKEN)