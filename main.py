import asyncio
import discord
import os
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ  
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

ranking = list()
def chuchul() :
    pin = worksheet.col_values(1)
    score = worksheet.col_values(2)
    for var in range(len(score)) :
        score[var] = int(score[var])
    sortedscore = sorted(score)
    for i in range(1, 6) :
        i = i * -1
        for m in range(len(score)) :
            if sortedscore[i] == score[m] :
                ranking.append([pin[m], sortedscore[i]])
    for i in range(len(ranking)) :
        ranking[i][0] = int(ranking[i][0])
    return ranking
        
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
@client.event
async def on_ready () : # 항상
      print(client.user.name,"실행중")
      activity = discord.Game(name="!문의봇 으로 명령어를 확인하세요")
      await client.change_presence(status=discord.Status.online, activity=activity) # idle = 자리비움
        
@client.command()
async def ping (ctx) :
    await ctx.send ("Pong!")
    
@client.command(pass_context=True)
async def 문의봇 (ctx, *args) : 
    if len(args) == 0 :
        await ctx.send ("```css\n[!문의봇 업데이트] : 업데이트 내역을 확인할 수 있습니다.\n[#문의 <문의내용>] : (Only DM) 문의/건의를 보낼 수 있습니다.\n[!통계도움말] : 공사중..```")              
    elif args[0] == '업데이트' :
        await ctx.send ("```cs\n2020년 3월 11일 업데이트 내역 (0.1)\n#1 '통계도움말 추가'```")
        
@client.command()
async def 테스트 (ctx) :
    chuchul()
    for i in range(len(ranking)) :
        user = client.get_user(ranking[i][0])
        temp = user.name
        ranking[i][0] = temp
        print(ranking[i][0])     
        
@client.command()
async def 통계도움말 (ctx) :
    instro = '```cs\n!통계 출처 : #통계 출처를 확인합니다. \n!통계 채팅 : #채팅 통계를 출력합니다.```'
    embed = discord.Embed(title = '통계 도움말' , description = instro)
    await ctx.send(embed=embed)

@client.command()
async def 통계 (ctx, *args) :
    if len(args) == 0 :
        await ctx.send ("Unknown command")
    if args[0] == '출처' :
        await ctx.send ('자료 출처 : https://docs.google.com/spreadsheets/d/19lH3kuGI73vDO0jnfGWbCZLBNv9GlkMBtFEM5cOnmpk/edit?usp=sharing')
    if args[0] == '채팅' :
        chuchul()
        for i in range(len(ranking)) :
            user = client.get_user(ranking[i][0])
            temp = user.name
            ranking[i][0] = temp
        x = '2020년 3월 12일 오전 11시부터 집계, 새벽 2:00~8:00 집계X'
        embed = discord.Embed(description = x, colour = discord.Colour.gold())
        embed.set_author(name = '장터방 채팅 순위(통계)', icon_url = 'https://previews.123rf.com/images/robisklp/robisklp1504/robisklp150400041/38940859-%EA%B3%A8%EB%93%9C-%ED%8A%B8%EB%A1%9C%ED%94%BC.jpg')
        embed.add_field (name = '#1', value = '{0} : {1}회'.format(ranking[0][0], ranking[0][1]), inline = False)
        embed.add_field (name = '#2', value = '{0} : {1}회'.format(ranking[1][0], ranking[1][1]), inline = False)
        embed.add_field (name = '#3', value = '{0} : {1}회'.format(ranking[2][0], ranking[2][1]), inline = False)
        embed.add_field (name = '#4', value = '{0} : {1}회'.format(ranking[3][0], ranking[3][1]), inline = False)
        embed.add_field (name = '#5', value = '{0} : {1}회'.format(ranking[4][0], ranking[4][1]), inline = False)
        embed.set_footer(text = 'Kimdy#4847')
        await ctx.send(embed=embed)
contents = ""
@client.event
async def on_message(message) :
    gc.login()
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
