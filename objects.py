import requests, datetime
from lxml import html

#set up GET request
now = str(datetime.date.today()) #today's date
#now = "2021-03-11" #for testing
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'} #correct HTML formatting
champ =  "https://www.google.co.uk/async/lr_lg_fp?yv=3&q=lg|/g/11j74c9ljn|mt|fp&async=sp:2,lmid:%2Fm%2F0355pl,tab:mt,emid:%2Fg%2F11j74c9ljn,rbpt:undefined,ct:GB,hl:en,tz:Europe%2FLondon,dtoint:" + now + "T12%3A30%3A00Z,dtointmid:%2Fg%2F11j74c9ljn,_id:liveresults-sports-immersive__league-fullpage,_pms:s,_fmt:pc"
#GET requests for either prem or champ fixtures, with minimum information (prem k = 5, champ k = 3)
page = requests.get(url=champ, headers=headers) #load HTML
tree = html.fromstring(page.content) #create tree for xpaths

with open("test2.html", "w") as file:
    file.write(str(page.content))

