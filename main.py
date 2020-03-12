import asyncio
import discord
import os
import gspread
import time
import json
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands

client = commands.Bot(command_prefix='!')
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
    gc.login()
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
      activity = discord.Game(name="!문의봇 으로 명령어를 확인하세요")
      await client.change_presence(status=discord.Status.online, activity=activity) # idle = 자리비움

@client.command(pass_context=True)
async def 문의봇 (ctx, *args) : 
    if len(args) == 0 :
        await ctx.send ("```css\n[!문의봇 업데이트] : 업데이트 내역을 확인할 수 있습니다.\n[#문의 <문의내용>] : (Only DM) 문의/건의를 보낼 수 있습니다.\n[!통계자료확인] : 공사중..```")              
    elif args[0] == '업데이트' :
        await ctx.send ("```cs\n2020년 3월 11일 업데이트 내역 (0.1)\n#1 '이번이 첫 릴리즈라서 업데이트가 아님'```")
        
contents = ""
@client.event
async def on_message(message) :
    spread(int(message.author.id))
    if message.content.startswith("#문의") :
        contents = message.content[4:]
        username = str(message.author)
        user = client.get_user(337849294591885322)
        embed = discord.Embed(title = '{} 해당 내용이 전달되었습니다!'.format(':eyes:') ,description = '전달 내용 : {}'.format(contents))
        await message.author.send(embed=embed)
        embed2 = discord.Embed(title = '{}님으로부터의 문의/건의 내용'.format(username), description = '{}'.format(contents))
        await user.send(embed=embed2)
    await client.process_commands(message)
client.run(token)
