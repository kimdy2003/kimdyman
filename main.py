import asyncio
import discord
import os
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

client = commands.Bot(command_prefix='-')
access_token = 'NjgyNDMzNzI0NDk0Nzc0Mjkz.XleKrQ.AcfWIee5DpHbVsi7LNoBc5JUB-8'

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/user/Desktop/heroic-venture-270306-6b725eb305d4.json', scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/19lH3kuGI73vDO0jnfGWbCZLBNv9GlkMBtFEM5cOnmpk/edit#gid=0'

doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('JTB')
userID = worksheet.col_values(1)

def spread(id) :
    if "{}".format(id) in userID :
        for i in range(len(userID)) : 
            if userID[i] == "{}".format(id) : 
                temp = "B{}".format(i+1)
                data = int(worksheet.acell(temp).value)
                data += 1
                date = str(data)
                worksheet.update_acell(temp, date)
    else : 
        worksheet.update_acell("A{}".format(len(userID)+1), "{}".format(id))
        worksheet.update_acell("B{}".format(len(userID)+1), "1")

@client.event
async def on_ready () : # 항상
      print(client.user.name,"실행중")
      activity = discord.Game(name="문의는 DM")
      await client.change_presence(status=discord.Status.online, activity=activity) # idle = 자리비움

@client.event
async def on_message(message) :
    spread(message.author.id)
      
client.run(access_token)
