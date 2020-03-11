import asyncio
import discord
import os
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands

client = commands.Bot(command_prefix='-')
token = os.environ['BOT_TOKEN']
scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('heroic-venture-270306-6b725eb305d4.json', scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/19lH3kuGI73vDO0jnfGWbCZLBNv9GlkMBtFEM5cOnmpk/edit#gid=0'

doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('JTB')
userID = list()
    
def spread(id) :
    userID = worksheet.col_values(1)
    for i in range(len(userID)) : 
            if userID[i] == "{}".format(id) : 
                temp = "B{}".format(i+1)
                data = int(worksheet.acell(temp).value)
                data += 1
                date = str(data)
                worksheet.update_acell(temp, date)
    if str(id) not in userID :
        worksheet.insert_row(['{}'.format(id), '1'], len(userID)+1)
      
@client.event
async def on_ready () : # 항상
      print(client.user.name,"실행중")
      activity = discord.Game(name="문의는 DM")
      await client.change_presence(status=discord.Status.online, activity=activity) # idle = 자리비움

contents = ""
@client.event
async def on_message(message) :
    spread(message.author.id)
    if message.content.startswith ("!문의") :
        user = client.get_user(message.author.id)
        await user.send ("현재 사용할 수 없는 기능입니다.")
client.run(token)
