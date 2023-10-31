import asyncio
import requests
import json
import datetime

import discord
from discord.ext import commands

import os
import random
import bs4
import openai
import urllib.request
from bs4 import BeautifulSoup as bs
import re

app = commands.Bot(command_prefix='!',intents=discord.Intents.all())
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@app.event
async def on_ready():
    print('Done')
    await app.change_presence(activity=discord.Game(name='!도움 [봇 사용법]'))
    #await app.change_presence(status=discord.Status.online, activity=None)


@app.command()
async def 안녕(ctx):
    await ctx.send('안녕하세요! 저는 디스코드 챗봇입니다!')

@app.command()
async def 따라해(ctx, *, text):
    await ctx.send(text)
    print(type(text))

@app.command()
async def 도움(ctx):
    await ctx.send(embed = discord.Embed(title="봇 사용법", description='설명 입력', color=0x00aaaa))


@app.command()
async def 한강물(ctx):
    url = "https://api.qwer.pw/request/hangang_temp"
    res = requests.get(url, "apikey=guest")
    res_json = json.loads(res.content)
    respond = res_json[1]
    await ctx.send('현재 한강물 온도: ' + str(respond['respond']['temp']) + '°C')

@app.command()
async def 명언(ctx):
    url = "https://api.qwer.pw/request/helpful_text"
    res = requests.get(url, "apikey=guest")
    res_json = json.loads(res.content)
    respond = res_json[1]
    await ctx.send(respond['respond'])

#대기, 무한 대기 예제
@app.command()
async def 대기(ctx):
    channel = ctx.channel
    await ctx.send("안녕이라고 해줘")
    def check(m):
        return m.content == '안녕' and m.channel == channel
    msg = await app.wait_for('message', check=check)
    await channel.send('안녕 {.author}'.format(msg))

@app.command()
async def 무한거절(ctx):
    channel = ctx.channel
    await ctx.send("'끝'이라고 말하면 종료")
    while(True):
        msg = await app.wait_for('message')
        await ctx.send('거절!')
        if (msg.content == '끝'):
            await ctx.send('종료합ㄴ디ㅏ')
            break

#@app.command()
#async def 영화끝말잇기(ctx):
#    channel = ctx.channel
#    author = ctx.author
#    indexList = [0]
#    start = 0
#    f = open('anime.txt', 'r', encoding='UTF8')
#    lines = f.readlines()
#    lines = list(map(lambda s: s.strip(), lines))
#    await ctx.send("영화 끝말잇기를 시작합니다. 선/후 중 하나를 말해주세요")
#    def check(m):
#        return m.channel == channel and m.author == author
#    while(True):
#        msg = await app.wait_for('message', check=check)
#        if msg.content == '선':
#            await ctx.send("선공을 선택하셨습니다. 먼저 제시해주세요.")
#            start = 1
#            checkInput = "뷁"
#            break
#        elif msg.content == '후':
#            await ctx.send("후를 선택하셨습니다. 먼저 공격하겠습니다.")
#            Rtxt = random.randrange(0, len(lines)-1)
#            await ctx.send(lines[Rtxt])
#            checkInput = lines[Rtxt][-1]
#            break
#        else:
#            await ctx.send("'선'이나 '후'만 입력해주세요.")
#    while(True):
#        msg = await app.wait_for('message', check=check)
#        Acheck = 0
#        if msg.content[0] != checkInput and start == 0:
#            await ctx.send("끝말잇기 실패로 제 승리로 취급, 게임을 종료합니다^^")
#            break
#        for i in range(0,len(lines)):
#            if not i in indexList:
#                if (msg.content[-1] == lines[i][0]):
#                    await ctx.send(lines[i])
#                    await ctx.send(lines[i][-1] + "로 시작하는 영화을 입력해주세요.")
#                    checkInput = lines[i][-1]
#                    Acheck += 1
#                    indexList.append(i)
#                    break
#        if (Acheck == 0):
#            await ctx.send(msg.content[-1] + "로 시작하는 영화 이름을 찾지 못했으므로 종료합니다 8ㅁ8")
#            Acheck = 0
#            break
#        start = 0

@app.command()
async def 요리레시피(ctx, *, text):
    # 'by 만개의 레시피'로 작성된 레시피 주소 크롤링(page 1~165)
    # /recipe/xxxxxxx
    food = text
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://www.10000recipe.com/recipe/list.html?q=' + food, headers=header)  ## 만개의레시피 음식검색창
    html = req.text
    parse = bs(html, 'html.parser')
    urls = parse.find_all("div", {"class": "common_sp_thumb"})
    url = []
    for u in urls:
        url.append(u.find('a')["href"])
    url = ('https://www.10000recipe.com/' + url[0])
    req = urllib.request.Request(url)
    code = urllib.request.urlopen(url).read()
    soup = bs(code, "html.parser")
    num_id = 0
    food_dicts = []
    ingre_set = set()  # 재료 목록들을 담기 위한 set
    info_dict = {}
    ingre_list = []
    ingre_dict = {}
    recipe_list = []
    recipe_dict = {}
    food_dict = {}
    # 변수목록
    # menu_name : 메뉴 이름
    # menu_img : 메뉴 이미지
    # menu_summary : 메뉴 설명
    # menu_info_1 : n인분
    # menu_info_2 : 요리 시간
    # menu_info_3 : 난이도
    # ingredient_name : 재료 이름
    # ingredient_count : 계랑 숫자
    # ingredient_unit : 계량 단위
    # ingredient_main : 조미료 판단
    # recipe_step_txt : 레시피 순서 txt
    # recipe_step_img : 레시피 순서 img

    # menu_name
    res = soup.find('div', 'view2_summary')
    res = res.find('h3')
    menu_name = res.get_text()

    # menu_img
    res = soup.find('div', 'centeredcrop')
    res = res.find('img')
    menu_img = res.get('src')

    # menu_summary
    res = soup.find('div', 'view2_summary_in')
    menu_summary = res.get_text().replace('\n', '').strip()

    # menu_info
    res = soup.find('span', 'view2_summary_info1')  # menu_info_1
    menu_info_1 = res.get_text()
    res = soup.find('span', 'view2_summary_info2')  # menu_info_2
    menu_info_2 = res.get_text()
    res = soup.find('span', 'view2_summary_info3')  # menu_info_3
    menu_info_3 = res.get_text()

    # info dict
    info_dict = {"info1": menu_info_1,
                 "info2": menu_info_2,
                 "info3": menu_info_3}

    # ingredient
    res = soup.find('div', 'ready_ingre3')
    try:
        for n in res.find_all('ul'):
            for tmp in n.find_all('li'):
                ingredient_name = tmp.get_text().replace('\n', '').replace(' ', '')
                count = tmp.find('span')
                ingredient_tmp = count.get_text()
                ingredient_name = re.sub(ingredient_tmp, '', ingredient_name)  # ingredient_name
                ingredient_unit = ingredient_tmp.replace('/', '').replace('+', '')
                ingredient_unit = ''.join([i for i in ingredient_unit if not i.isdigit()])  # ingredient_unit
                ingredient_count = re.sub(ingredient_unit, '', ingredient_tmp)  # ingredient_count
                # ingre_list
                ingre_dict = {"ingre_name": ingredient_name,
                              "ingre_count": ingredient_count,
                              "ingre_unit": ingredient_unit, }
                ingre_list.append(ingre_dict)

                # set에 업데이트
                ingre_set.add(ingredient_name)
    except(AttributeError):
        pass

    await ctx.send('메뉴 이름: ' + menu_name + '\n정보: ' + menu_info_1 + ', 시간: ' + menu_info_2 + ', 난이도: ' + menu_info_3)
    await ctx.send('////////////////////////////////////////////////////////')
    await ctx.send("<재료>")
    for i in ingre_list:
        if i['ingre_count'] == '':
            await ctx.send(i['ingre_name'].replace('구매', '') + i['ingre_unit'])
        else:
            await ctx.send(i['ingre_name'].replace('구매', '') + i['ingre_count'] + i['ingre_unit'])
    await ctx.send('////////////////////////////////////////////////////////')
    # recipe
    res = soup.find_all("div", {"class": "view_step_cont"})
    i = 1
    for n in res:
        recipe_step_txt = n.get_text().replace('\n', ' ')
        await ctx.send('조리순서' + str(i))
        i += 1
        await ctx.send(recipe_step_txt)
        tmp = n.find('img')
        recipe_step_img = tmp.get('src')
        await ctx.send(recipe_step_img)

    # 변수목록
    # menu_name : 메뉴 이름
    # menu_img : 메뉴 이미지
    # menu_summary : 메뉴 설명
    # menu_info_1 : n인분
    # menu_info_2 : 요리 시간
    # menu_info_3 : 난이도
    # ingredient_name : 재료 이름
    # ingredient_count : 계랑 숫자
    # ingredient_unit : 계량 단위
    # ingredient_main : 조미료 판단
    # recipe_step_txt : 레시피 순서 txt
    # recipe_step_img : 레시피 순서 img


@app.command()
async def 영한번역(ctx, *, text):
    client_id = "apiId"
    client_secret = "apiPw"

    data = {'text': text,
            'source': 'en',
            'target': 'ko'}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id": client_id,
              "X-Naver-Client-Secret": client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if (rescode == 200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        await ctx.send(trans_data)
    else:
        print("Error Code:", rescode)
        await ctx.send("번역 오류!")

@app.command()
async def 한영번역(ctx, *, text):
    client_id = "apiId"
    client_secret = "apiPw"

    data = {'text': text,
            'source': 'ko',
            'target': 'en'}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id": client_id,
              "X-Naver-Client-Secret": client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if (rescode == 200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        await ctx.send(trans_data)
    else:
        print("Error Code:", rescode)
        await ctx.send("번역 오류!")

@app.command()
async def 메시지(ctx, *, text):
    openai.api_key = 'apikey'
    messages = []
    content = text
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    chat_response = completion.choices[0].message.content
    await ctx.send(chat_response)
    messages.append({"role": "디스코드 챗봇", "content": chat_response})

@app.command()
async def 날씨(ctx, *, text):
    if text == '석관동':
        nx = 61
        ny = 128
    elif text == '강남':
        nx = 61
        ny = 126
    elif text == '홍대':
        nx = 59
        ny = 126
    elif text == '합정':
        nx = 59
        ny = 126
    elif text == '제주':
        nx = 52
        ny = 38
    elif text == '서울':
        nx = 60
        ny = 127
    elif text == '부산':
        nx = 98
        ny = 76
    elif text == '대구':
        nx = 89
        ny = 90
    elif text == '대전':
        nx = 67
        ny = 100
    elif text == '세종':
        nx = 66
        ny = 103
    elif text == '안양':
        nx = 59
        ny = 123
    elif text == '경기도':
        nx = 60
        ny = 120
    elif text == '김포':
        nx = 55
        ny = 128
    elif text == '전라남도':
        nx = 51
        ny = 67
    elif text == '인천':
        nx = 55
        ny = 124
    elif text == '전라북도':
        nx = 63
        ny = 89
    elif text == '광주':
        nx = 58
        ny = 74
    else:
        nx = 'error'
        ny = 'kkk'
        await ctx.send('등록되지 않은 지역입니다.')

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    key = '날씨apikey'

    now = datetime.datetime.now()
    today = datetime.datetime.today().strftime("%Y%m%d")
    y = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")
    if now.minute < 45:  # base_time와 base_date 구하는 함수
        if now.hour == 0:
            base_time = "2330"
            w_time = "0000"
            base_date = yesterday
        else:
            pre_hour = now.hour - 1
            if pre_hour < 10:
                base_time = "0" + str(pre_hour) + "30"
                w_time = "0" + str(now.hour) + "00"
                if(pre_hour == 9):
                    w_time = str(now.hour) + "00"
            else:
                base_time = str(pre_hour) + "30"
                w_time = str(now.hour) + "00"
            base_date = today
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
            w_time = "0" + str(now.hour + 1) + "00"
            if (now.hour == 9):
                w_time = str(now.hour + 1) + "00"
        else:
            base_time = str(now.hour) + "30"
            w_time = str(now.hour + 1) + "00"
        base_date = today
    params = {'serviceKey': key, 'pageNo': '1', 'numOfRows': '1000', 'dataType': 'JSON', 'base_date': base_date,
              'base_time': base_time, 'nx': nx, 'ny': ny}

    res = requests.get(url, params=params)
    res_json = json.loads(res.content)
    items = res_json["response"]['body']['items']['item']
    weather_data = dict()
    print(items)
    for item in items:
        # 기온
        if item['category'] == 'T1H' and item['fcstTime'] == w_time:
            weather_data['tmp'] = item['fcstValue']
        # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
        if item['category'] == 'SKY' and item['fcstTime'] == w_time:
            weather_data['sky'] = item['fcstValue']
        # 강수형태 없음(0) 비(1) 비/눈(2), 눈(3), 소나기(4)
        if item['category'] == 'PTY' and item['fcstTime'] == w_time:
            weather_data['rain'] = item['fcstValue']
        # 풍속
        if item['category'] == 'WSD' and item['fcstTime'] == w_time:
            weather_data['wind'] = item['fcstValue']

    if weather_data['sky'] == '1':
        await ctx.send('날씨: 맑음')
    if weather_data['sky'] == '3':
        await ctx.send('날씨: 구름 많음')
    if weather_data['sky'] == '4':
        await ctx.send('날씨: 흐림')
    await ctx.send('온도: ' + weather_data['tmp'] + '도')
    if int(weather_data['wind']) < 4:
        await ctx.send('바람: 약함')
    if int(weather_data['wind']) >= 4:
        await ctx.send('바람: 약간 강함')
    if int(weather_data['wind']) >= 9:
        await ctx.send('바람: 강함')
    if weather_data['rain'] == '0':
        await ctx.send('현재는 비가 내리지 않습니다')
    if weather_data['rain'] == '1':
        await ctx.send('그리고 비가 내립니다')
    if weather_data['rain'] == '2':
        await ctx.send('그리고 비나 눈이 옵니다')
    if weather_data['rain'] == '3':
        await ctx.send('그리고 눈이 옵니다')
    if weather_data['rain'] == '5':
        await ctx.send('그리고 빗방울이 내립니다')
    if weather_data['rain'] == '6':
        await ctx.send('그리고 빗방울눈이 날립니다')
    if weather_data['rain'] == '7':
        await ctx.send('그리고 하늘에 눈이 날립니다')



@app.command()
async def 야식추천(ctx):
    f = open('food.txt', 'r', encoding='UTF8')
    lines = f.readlines()
    lines = list(map(lambda s: s.strip(), lines))
    txtNum = (len(lines) - 1)
    Rtxt = random.randrange(0, txtNum)
    await ctx.send(lines[Rtxt] + '(을)를 추천해요!')


@app.command()
async def 멜론차트(ctx):
    RANK = 10
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    req = requests.get('https://www.melon.com/chart/week/index.htm', headers=header)  ## 주간 차트를 크롤링 할 것임
    html = req.text
    parse = bs4.BeautifulSoup(html, 'html.parser')

    titles = parse.find_all("div", {"class": "ellipsis rank01"})
    singers = parse.find_all("div", {"class": "ellipsis rank02"})

    title = []
    singer = []

    for t in titles:
        title.append(t.find('a').text)

    for s in singers:
        singer.append(s.find('span', {"class": "checkEllipsis"}).text)

    for i in range(RANK):
        await ctx.send('%3d위: %s - %s' % (i + 1, title[i], singer[i]))


app.run('apikey')