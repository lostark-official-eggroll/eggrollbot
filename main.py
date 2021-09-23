import asyncio
import discord
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='!')

# 디스코드에서 생성된 토큰을 여기에 추가
token = os.environ["BOT_TOKEN"]

# 아래는 봇이 구동되었을 때 동작하는 부분
@client.event
async def on_ready():
    print("Logged in as ") #봇의 아이디, 닉네임이 출력
    print(client.user.name)
    print(client.user.id)

# 디스코드 id와 계정 연동
@bot.command(name='계정연동')
async def link(ctx, Id, user: discord.Member = None) -> None:
	#디스코드 서버의 관리자는 타인의 계정을 그 사람의 디스코드 계정에 연동해주는 기능도 있으면 편리할 것입니다. 
    #코드의 첫 if else 구문들은 이를 구분하기 위해 쓰였습니다.

    if user and ctx.message.author.guild_permissions.administrator:
        hash = user.id
    else:
        if user:
            await ctx.send(f"타인의 계정연동 기능은 관리자만 사용가능합니다.")
            raise PermissionsError('ctx.author does not have permission')
        hash = ctx.author.id
		
    #DB.call()은 hash와 Id를 받고, DB에 hash를 서치해보고 있다면 그 데이터 값을 리턴, 
    #없다면 크롤링하여 리턴한 뒤 크롤링 데이터를 DB에 저장해줍니다.
    call_data = DB.call(hash,Id)
    
    #이후 디스코드 계정에 데이터를 연동해줍니다. 
    #이미 크롤러에서 원정대 내 캐릭터 정보를 아이템 레벨순으로 정렬하였습니다. 
    #call_data의 첫 인덱스의 값을 받아 대표 캐릭터 정보로 사용합니다.
    name, cl, lv = call_data[0][1:]
    role_name = '길드원' #길드 규칙 및 디스코드 역할에 맡게 지정
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    
    
    # 다시 관리자가 타인의 계정을 연동해준 것이라면 그 멤버의 역할과 닉네임을 바꿔줍니다.
    # 아닌 경우 명령어를 콜한 멤버의 역할과 닉네임을 바꿔줍니다.
    # 대표 캐릭터의 레벨이나 직업에 따라 미리 설정된 role로 user의 디스코드 역할, 디스코드 닉네임을 바꿔줍니다.
    
    if user and ctx.message.author.guild_permissions.administrator:
        try:
            await user.add_roles(role)
            await user.add_roles(discord.utils.get(ctx.guild.roles, name=cl))
            await user.edit(nick=f'{name}')
        except Exception as e:
            print(e)
        nick_ = user.nick
    # 아니면 author꺼 바꿈
    else:
        try:
            await ctx.author.add_roles(role)
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=cl))
            await ctx.author.edit(nick=f'{name}')
        except Exception as e:
            print(e)
        nick_ = None
	
    #  마지막으로 call_data를 이쁘게 출력하여 계정정보를 보여줍니다.
    
    await ctx.send(f'{nick_ or ctx.author.nick} 님의 계정 연동 사항입니다.\n')
    await ctx.send(embed=embed_print(call_data))
client.run(token)
bot.run(token)
