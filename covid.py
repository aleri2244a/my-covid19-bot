import discord
from bs4 import BeautifulSoup
import requests
import urllib

client = discord.Client()


@client.event
async def on_ready():
    print("봇이 성공적으로 실행되었습니다.")
    game = discord.Game('!코로나 로 코로나 정보 조회!')
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.content.startswith('!코로나'):
        url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        datecr = soup.find('span', {'class': 't_date'}) #기준날짜
        #print(f'기준일: {datecr.string}')

        totalcovid = soup.select('dd.ca_value')[0].text #누적 확진자수
        #print(f'누적 확진자: {totalcovid} 명')

        todaytotalcovid = soup.select('p.inner_value')[0].text #당일 확진자수 소계
        #print(f'확진자 소계: {todaytotalcovid} 명')

        todaydomecovid = soup.select('p.inner_value')[1].text #당일 국내발생 확진자수
        #print(f'국내발생: {todaydomecovid} 명')

        todayforecovid = soup.select('p.inner_value')[2].text #당일 해외유입 확진자수
        #print(f'해외유입: {todayforecovid} 명')

        totalca = soup.select('dd.ca_value')[2].text #누적 격리해제
        #print(f'누적 격리해제: {totalca} 명')

        todayca = soup.select('span.txt_ntc')[0].text #당일 격리해제
        #print(f'격리해제: {todayca} 명')

        totalcaing = soup.select('dd.ca_value')[4].text #누적 격리중
        #print(f'누적 격리중: {totalcaing}')

        todaycaing = soup.select('span.txt_ntc')[1].text #당일 격리중
        #print(f'격리중: {todaycaing} 명')

        totaldead = soup.select('dd.ca_value')[6].text #누적 사망자
        #print(f'누적 사망자: {totaldead} 명')

        todaydead = soup.select('span.txt_ntc')[2].text #당일 사망자
        #print(f'사망자: {todaydead} 명')

        covidembed = discord.Embed(title='코로나19 바이러스 국내 발생 현황 입니다!', description="", color=0x00D100, url='http://ncov.mohw.go.kr/')
        covidembed.add_field(name='확진 자 :', value=f'{totalcovid}({todaytotalcovid}) 명'
                                                f'\n\n국내 발생 확진자 : {todaydomecovid} 명\n해외 유입 확진자 : {todayforecovid} 명', inline=False)
        covidembed.add_field(name='격리 중 :', value=f'{totalcaing}({todaycaing}) 명', inline=False)
        covidembed.add_field(name='격리 해제 :', value=f'{totalca}({todayca}) 명', inline=False)
        covidembed.add_field(name='사망 자 :', value=f'{totaldead}({todaydead}) 명', inline=False)
        covidembed.set_footer(text=datecr.string)
        await message.channel.send(embed=covidembed)
        
client.run('ODU0ODk4MDI1OTA0OTk2NDAz.YMqn1A.UCRwZ9ACXyEz317OdmvbQtaH0_M')
