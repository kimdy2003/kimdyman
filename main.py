import asyncio
import discord
import os
import sheet
from discord.ext import commands

client = commands.Bot(command_prefix='-')
access_token = os.environ["BOT_TOKEN"]

@client.event
async def on_ready () : # 항상
      print(client.user.name,"실행중")
      activity = discord.Game(name="DM으로 문의주세요.")
      await client.change_presence(status=discord.Status.online, activity=activity) # idle = 자리비움

contents = ""
@client.event
async def on_message(message) :
    sheet.spread(int(message.author.id))
    if isinstance(message.channel,discord.DMChannel):
        if message.content.startswith("!문의") :
             contents = message.content[4:]
             username = str(message.author)
             user = client.get_user(337849294591885322)
             embed = discord.Embed(title="{} 님의 문의/건의내용".format(username), description = contents, colour= discord.Colour.gold())
             await user.send(embed=embed)
        else : 
            await message.author.send("메세지를 !문의 [내용] 으로 보내주세요.")
    else :
        if message.content.startswith("!문의") :
            await message.channel.send("문의는 저에게 해주세요^^")
      
client.run(access_token)
