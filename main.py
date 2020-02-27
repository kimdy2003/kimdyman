import asyncio
import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='-')
access_token = os.environ["BOT_TOKEN"]

@client.event
async def on_ready () : # 항상
      print(client.user.name,"실행중")
      activity = discord.Game(name="-문의 (문의 내용) 으로 문의/건의사항 을 보내주세요~!")
      await client.change_presence(status=discord.Status.online, activity=activity) # idle = 자리비움

@client.event
async def on_message(message) :
    if message.content.startswith("-문의") : 
        msg = message.content[4:]
        author = message.guild.get_member(337849294591885322)
        await author.send(msg)
        await message.channel.send("해당 사항이 전달되었습니다.")
      
client.run(access_token)
