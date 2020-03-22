import asyncio
import discord
import os
from discord.ext import commands
import inform
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
    username = worksheet.col_values(4)
    for var in range(len(score)) :
        score[var] = int(score[var])
    sortedscore = sorted(score)
    print(score)
    print(sortedscore)
    for i in range(1, 11) :
        i = i * -1
        for m in range(len(score)) :
            if sortedscore[i] == score[m] :
                ranking.append([pin[m], sortedscore[i], username[m]])
                score[m] = 0
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
async def sortedname (ctx) :
    pin = worksheet.col_values(1)
    for i in range(len(pin)) :
        user = client.get_user(int(pin[i]))
        temp = 'D{}'.format(i+1)
        if user == None :
            worksheet.update_acell(temp, 'Unknown')
        elif user != None :
            worksheet.update_acell(temp, user.name)      
    
@client.command(aliases =['유저정보'])
async def userinfo (ctx, *args) :
    if len(args) > 0 :
        name = args[0]
        if len(args) > 1 :
            for i in range (1, len(args)) :
                name += " " + args[i]
        for member in ctx.author.guild.members :
            if name == member.display_name :
                if member.bot == False :
                    user = client.get_user(member.id)
                    info = discord.Embed(colour = discord.Colour.blue())
                    info.set_author(name = '**{}님의 서버 정보**'.format(member.name), icon_url = 'https://cdn.iconscout.com/icon/free/png-512/discord-3-569463.png')
                    info.set_thumbnail (url = user.avatar_url)
                    info.add_field (name = '서버 이름', value = '**{}**'.format(member.name), inline = True)
                    info.add_field (name = '클라이언트 이름', value = '**{}**'.format(member.display_name), inline= True)
                    info.add_field (name = '현재 상태', value = '**{0}**'.format(inform.statuscheck(member.status)), inline = True)
                    info.add_field (name = '{} 아이디'.format('<:id:689428440335777853>'), value = '{}'.format(member.id), inline = True)
                    info.add_field (name = '{}서버에 들어온 날짜'.format('<:inbox_tray:689057672297054210>'), value = '**{}**'.format(inform.datecheck(member.joined_at)), inline = False)
                    info.add_field (name = '{}계정을 만든 날짜'.format('<:inbox_tray:689057672297054210>'), value = '**{}**'.format(inform.datecheck(member.created_at)), inline = True)
                    await ctx.channel.send (embed = info)
        
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
        result = chatranking()
        info = discord.Embed()
        info.set_author (name = '장터방 채팅 순위', url = ctx.author.guild.banner_url)
        for i in range(len(result)) :
            info.add_field (name = '#{}'.format(i+1), value = '{}, {}회'.format(result[i][1], result[i][2]), inline = True)
        info.set_footer (text = '`20년 3월 12일부터 집계, 2:00 ~ 8:00 집계 X')
        await ctx.channel.send (embed = info)
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
def chatranking () :
    worksheet = doc.worksheet('JTB')
    uid = worksheet.col_values(1)
    name = worksheet.col_values(4)
    if len(uid) != len(worksheet.col_values(4)) :
        checks (uid)
    score = worksheet.col_values(2)
    lst = list()
    for i in range(len(score)) :
        score[i] = int(score[i])
    sortedscore = sorted(score)
    for i in range(1, 10) :
        temp = sortedscore [-1 * i] 
        for m in range(len(score)) :
            if score[m] == temp :
                lst.append([uid[m], name[m], temp])
    return lst
                
    
    
    


def checks (pin) :
    for i in range(len(pin)) :
        user = client.get_user(int(pin[i]))
        temp = 'D{}'.format(i+1)
        if user == None :
            worksheet.update_acell(temp, 'Unknown')
        elif user != None :
            worksheet.update_acell(temp, user.name)
            
client.run(token)
