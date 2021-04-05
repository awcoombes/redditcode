#posts the pre-matchweek thread at 1200 day of first game
#schedules match thread for kickoff of first game

import requests, datetime
from lxml import html
import champupload as u
from crontab import CronTab

#set up GET request
now = str(datetime.date.today()) #today's date
#now = "2021-03-09"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'} #correct HTML formatting
prem = "https://www.google.com/async/lr_lg_fp?yv=3&q=lg|/g/11j4y8fvpd|mt|fp&async=sp:2,lmid:%2Fm%2F02_tc,tab:mt,emid:%2Fg%2F11j4y8fvpd,rbpt:undefined,ct:GB,hl:en,tz:Europe%2FLondon,dtoint:" + now + "T00%3A00%3A00Z,dtointmid:%2Fg%2F11j4y8fvpd,_id:liveresults-sports-immersive__league-fullpage,_pms:s,_fmt:pc"
champ =  "https://www.google.co.uk/async/lr_lg_fp?yv=3&q=lg|/g/11j74c9ljn|mt|fp&async=sp:2,lmid:%2Fm%2F0355pl,tab:mt,emid:%2Fg%2F11j74c9ljn,rbpt:undefined,ct:GB,hl:en,tz:Europe%2FLondon,dtoint:" + now + "T12%3A30%3A00Z,dtointmid:%2Fg%2F11j74c9ljn,_id:liveresults-sports-immersive__league-fullpage,_pms:s,_fmt:pc"
#GET requests for either prem or champ fixtures, with minimum information (prem k = 5, champ k = 3)
page = requests.get(url=champ, headers=headers) #load HTML
tree = html.fromstring(page.content) #create tree for xpaths

#clubs formatting dict
clubsdict = {'Bournemouth': '[BOU](https://reddit.com/r/AFCBournemouth)', 'Barnsley': '[BAR](https://reddit.com/r/BarnsleyFC)', 'Birmingham': '[BIR](https://reddit.com/r/BCFC)', 'Blackburn Rovers': '[BBR](https://reddit.com/r/BRFC)', 'Brentford': '[BRE](https://reddit.com/r/Brentford)', 'Bristol City': '[BRC](https://reddit.com/r/BristolCity)', 'Cardiff City': '[CDF](https://reddit.com/r/Bluebirds)', 'Coventry': '[CVC](https://reddit.com/r/ccfc)', 'Derby County': '[DER](https://reddit.com/r/DerbyCounty)', 'Huddersfield': '[HUD](https://reddit.com/r/HuddersfieldTownFC)', 'Luton Town': '[LUT](https://reddit.com/r/COYH)', 'Middlesbrough': '[MID](https://reddit.com/r/Boro)', 'Millwall': '[MIL](https://reddit.com/r/Millwall)', 'Norwich City': '[NOR](https://reddit.com/r/NorwichCity)', 'Nottm Forest': '[NTF](https://reddit.com/r/NFFC)', 'Preston': '[PNE](https://reddit.com/r/PNE)', 'QPR': '[QPR](https://reddit.com/r/SuperHoops)', 'Reading': '[RDG](https://reddit.com/r/URz)', 'Rotherham': '[RTU](https://www.reddit.com/subreddits/create)', 'Sheffield Wednesday': '[SHW](https://reddit.com/r/SheffieldWednesday)', 'Stoke City': '[STK](https://reddit.com/r/StokeCityFC)', 'Swansea': '[SWA](https://reddit.com/r/SwanseaCity)', 'Watford': '[WAT](https://reddit.com/r/Watford_FC)', 'Wycombe': '[WYC](https://reddit.com/r/WycombeWanderers)'}
data = [] #output list

#initiate counting variables
i = 1
j = 1
with open ("k.txt", "r") as file:
    k = int(file.read())
z = 0
gameweekroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[1]' #check current gameweek
print(gameweekroute)
thisweek = str(tree.xpath(gameweekroute + '/text()')[0])
k -= 1
gameweekroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[1]' #check last gameweek
k += 1
lastweek = str(tree.xpath(gameweekroute + '/text()')[0])
checkweek = int(lastweek[9:-6]) #create check integer
check = int(thisweek[9:-6]) - checkweek #see if gameweeks are sequential (original fixture list)
if check > 0: #if sequential, only collect this gameweek
    multiweek = False
    titleweek = thisweek
else: #if not sequential, collect multiple gameweeks of fixtures
    multiweek = True
    titleweek = "Rescheduled Matches"
print(titleweek)
timesroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[2]/div/table/tbody/tr[' #base xpath for fixture information

#collect information for games yet to start
if multiweek == False:
    running = True
    i = 1 #reset counting variables
    j = 1
    z = 0
    runtoday = False
    while running:
        try:
            timings = timesroute + str(i) + ']/td[' + str(j) + ']/div/div/div/table' #iterate extended xpath base through table of fixtures
            hometeam = str(tree.xpath(timings + '/tr[5]/td[2]/div/span[1]' + '/text()')[0]) #collect fixture information
            awayteam = str(tree.xpath(timings + '/tr[6]/td[2]/div/span[1]' + '/text()')[0])
            day = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[1]' + '/text()')[0])
            if day == "Today":
                runtoday = True
            kickoff = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[2]' + '/text()')[0])
            a = clubsdict[hometeam] + " vs " + clubsdict[awayteam] + ", " + day + " " + kickoff #format fixture information
            data.append(a)
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
                running = False
            elif j == 1: #counting variables update to move through table
                j = 2
            elif j == 2:
                j = 1
                i += 1
            else: #stop checking in any other scenario
                running = False

elif multiweek == True:
    running = True
    i = 1 #reset counting variables
    j = 1
    z = 0
    runtoday = False
    while running:
        try:
            timings = timesroute + str(i) + ']/td[' + str(j) + ']/div/div/div/table' #iterate extended xpath base through table of fixtures
            hometeam = str(tree.xpath(timings + '/tr[5]/td[2]/div/span[1]' + '/text()')[0]) #collect fixture information
            awayteam = str(tree.xpath(timings + '/tr[6]/td[2]/div/span[1]' + '/text()')[0])
            day = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[1]' + '/text()')[0])
            kickoff = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[2]' + '/text()')[0])
            a = clubsdict[hometeam] + " vs " + clubsdict[awayteam] + ", " + day + " " + kickoff #format fixture information
            data.append(a)
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
                gameweekroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[1]' #check next gameweek
                thisweek = str(tree.xpath(gameweekroute + '/text()')[0])
                check = int(thisweek[9:-6]) - checkweek #compare next gameweek to check gameweek
                if check >= 1: #if next gameweek is one more than check gameweek, stop iterating
                    running = False
                else: #if next gameweek is NOT one more than check gameweek, load fixtures from it
                    i = 1
                    j = 1
                    z = 0
                    timesroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[2]/div/table/tbody/tr['
            elif j == 1: #counting variables update to move through table
                j = 2
            elif j == 2:
                j = 1
                i += 1
            else: #stop checking in any other scenario
                running = False

content = "" #initiate content variable
starthour = 23 #initatiate time check variable
startmin = 59
matchtime = "23:59"
for i in data: #fill content variable with formatted text
    content = content + i + "  \n"
    start = int(i[-5:-3])
    day = i[-7]
    if start < starthour and day == "y": #find earliest game start time
        starthour = start
        startmin = i[-2:]
    matchtime = str(starthour) + ":" + str(startmin)
content = content + "\n\nThis thread was posted automatically, if there are any issues please contact the mods"
sub = "coombeseh" #set up variables for reddit post
title = "Pre-Match thread: " + titleweek
link = u.post(sub, title, content) #post to reddit
#print(content)

#cron code to schedule match thread at matchtime
cron = CronTab(user='andrew')
cron.remove_all(comment='prematch')
cron.write()
schedule = str(startmin) + " " + str(starthour) + " * * *"
job = cron.new(command='/usr/bin/python3 /home/andrew/code/matchthread.py > /home/andrew/code/matchlog 2>&1', comment = "match")
job.setall(schedule)
cron.write()