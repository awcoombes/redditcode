#Code checks if there are any games to be played today
#if there are, it schedules the match thread at 1200 sameday

import requests, datetime
from lxml import html
from crontab import CronTab

#set up GET request
now = str(datetime.date.today()) #today's date
#now = "2021-03-11" #for testing
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'} #correct HTML formatting
prem = "https://www.google.com/async/lr_lg_fp?yv=3&q=lg|/g/11j4y8fvpd|mt|fp&async=sp:2,lmid:%2Fm%2F02_tc,tab:mt,emid:%2Fg%2F11j4y8fvpd,rbpt:undefined,ct:GB,hl:en,tz:Europe%2FLondon,dtoint:" + now + "T00%3A00%3A00Z,dtointmid:%2Fg%2F11j4y8fvpd,_id:liveresults-sports-immersive__league-fullpage,_pms:s,_fmt:pc"
champ =  "https://www.google.co.uk/async/lr_lg_fp?yv=3&q=lg|/g/11j74c9ljn|mt|fp&async=sp:2,lmid:%2Fm%2F0355pl,tab:mt,emid:%2Fg%2F11j74c9ljn,rbpt:undefined,ct:GB,hl:en,tz:Europe%2FLondon,dtoint:" + now + "T12%3A30%3A00Z,dtointmid:%2Fg%2F11j74c9ljn,_id:liveresults-sports-immersive__league-fullpage,_pms:s,_fmt:pc"
#GET requests for either prem or champ fixtures, with minimum information (prem k = 5, champ k = 3)
page = requests.get(url=champ, headers=headers) #load HTML
tree = html.fromstring(page.content) #create tree for xpaths

##with open("test.txt", "w") as file:
##    file.write(page.text)

#initiate counting variables
i = 1
j = 1
k = 1
z = 0
running = True
runtoday = False
while running:
    #print(z)
    try:
        timesroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[2]/div/table/tbody/tr[' #base xpath for fixture information
        timings = timesroute + str(i) + ']/td[' + str(j) + ']/div/div/div/table' #iterate extended xpath base through table of fixtures
        #hometeam = str(tree.xpath(timings + '/tr[5]/td[2]/div/span[1]' + '/text()')[0]) #collect fixture information
        #awayteam = str(tree.xpath(timings + '/tr[6]/td[2]/div/span[1]' + '/text()')[0])
        day = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[1]' + '/text()')[0])
        print(day)
        if day == "Today": #check if game is today, if any found stop iterating and move to scheduler
            runtoday = True
            running = False
        else:
            print("other day found")
            running = False
        #kickoff = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[2]' + '/text()')[0])
        #a = hometeam + " vs " + awayteam + ", " + day + " " + kickoff #format fixture information
        #print(a)
        z += 1 #increment game counter
        if j == 1: #counting variables update to move through table
            j = 2
        elif j == 2:
            i += 1
            j = 1
    except Exception as e: #entered if future game not found
        ##print(e)
        z += 1 #increment game counter
        if z > 12: #stop checking if game counter exceeds max number of games in a gameweek
            k += 1
            i = 1
            j = 1
            z = 0
        elif j == 1: #counting variables update to move through table
            j = 2
        elif j == 2:
            j = 1
            i += 1
        else: #stop checking in any other scenario
            running = False

print(k)
with open ("k.txt", "w") as file:
    file.write(str(k))

cron = CronTab(user='andrew')
cron.remove_all(comment='checker')
cron.write()

print(runtoday)
if runtoday == True:
    #cron code to schedule prematch at 1200
    schedule = "00 12 * * *"
    cron = CronTab(user='andrew')
    job = cron.new(command='/usr/bin/python3 /home/andrew/code/prematch.py > /home/andrew/code/prematchlog 2>&1', comment = "prematch")
    job.setall(schedule)
    cron.write()
else:
    #cron code to schedule self at 0200 tomorrow
    schedule = "00 02 * * *"
    cron = CronTab(user='andrew')
    job = cron.new(command='/usr/bin/python3 /home/andrew/code/gamechecker.py > /home/andrew/code/checkerlog 2>&1', comment = "checker")
    job.setall(schedule)
    cron.write()