import asyncio
import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '$')

def datecheck (pme) :
    pme = str(pme) 
    result = str()
    result = "{0}년 {1}월 {2}일 {3}시 {4}분".format(pme[0:4], pme[5:7], pme[8:10], pme[11:13], pme[14:16])
    return result

def statuscheck(status) :
    status = str(status)
    if status == 'online' :
        status = '{} 온라인'.format('<:green_circle:689426408564719626>')
        return status
    if status == 'offline' :
        status = '{} 오프라인'.format('<:grey_circle:689428995065905162>')
        return status
    if status == 'idle' :
        status = '{} 자리비움'.format('<:yellow_circle:689428995065905162>')
        return status
    if status == 'dnd' :
        status = '{} 다른 용무중'.format('<:red_circle:689428995065905162>')
        return status
