#updates the match thread, checks if all games are ended - if more in matchweek, reschedules self, if no more schedules checker
#if matches still running, reschedules self in 5 mins

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

with open("content.txt", "w") as file:
    file.write(page.text)

playing = [] #output lists
fixtures = []

#initiate counting variables
i = 1
j = 1
k = 3
z = 0
gameweekroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[1]' #check current gameweek
thisweek = str(tree.xpath(gameweekroute + '/text()')[0])
k -= 1
gameweekroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[1]' #check last gameweek
k += 1
lastweek = str(tree.xpath(gameweekroute + '/text()')[0])
checkweek = int(lastweek[9:-6]) #create check integer
check = int(thisweek[9:-6]) - checkweek #see if gameweeks are sequential (original fixture list)
if check == 1: #if sequential, only collect this gameweek
    multiweek = False
    titleweek = thisweek
else: #if not sequential, collect multiple gameweeks of fixtures
    multiweek = True
    titleweek = "Rescheduled Matches"
print(titleweek)
#collect live scores from any games in progress or completed
timesroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[2]/div/table/tbody/tr[' #base xpath for fixture information
running = True
checking = True
allended = False
while running:
    try:
        timings = timesroute + str(i) + ']/td[' + str(j) + ']/div/div/div/table' #iterate extended xpath base through table of fixtures
        hometeam = str(tree.xpath(timings + '/tr[5]/td[2]/div[2]/span[1]' + '/text()')[0]) #collect fixture and score values
        awayteam = str(tree.xpath(timings + '/tr[6]/td[2]/div[2]/span[1]' + '/text()')[0])
        homescore = str(tree.xpath(timings + '/tr[5]/td[2]/div[1]/div' + '/text()')[0])
        awayscore = str(tree.xpath(timings + '/tr[6]/td[2]/div[1]/div' + '/text()')[0])
        try:
            completed = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div[2]/span' + '/text()')[0]) #see if game has finished
            currenttime = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div[1]' + '/text()')[0]) #if it has, get value FT
            if checking == True:
                allended = True #confirm that last collected match has finished (only checks if there are NO matches currently running)
        except Exception as e: #only entered if game not finished
            #print(e)
            try:
                currenttime = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div[2]/span/span/span[1]' + '/text()')[0]) #see if current time is half time
            except:
                currenttime = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/span' + '/text()')[0]) #collect current minute
            checking = False
            allended = False
        if currenttime == "Halfâtime": #correctly format HT
            currenttime = "Half Time"
        a = hometeam + " " + homescore + "-" + awayscore + " " + awayteam + ", " + currenttime #format all collected values
        playing.append(a)
        z += 1 #increment game counter
        if j == 1: #counting variables update to move through table
            j = 2
        elif j == 2:
            i += 1
            j = 1
    except Exception as e: #entered if completed or in progress game not found
        ##print(e)
        z += 1 #increment game counter
        if z > 12: #stop checking if game counter exceeds max number of games in a gameweek
            k += 1
            gameweekroute = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[' + str(k) + ']/div[1]' #check next gameweek
            thisweek = str(tree.xpath(gameweekroute + '/text()')[0])
            check = int(thisweek[9:-6]) - checkweek #compare next gameweek to check gameweek
            if check == 1: #if next gameweek is one more than check gameweek, stop iterating
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

runtomorrow = False

#collect information for games yet to start
# if multiweek == False:
#     running = True
#     i = 1 #reset counting variables
#     j = 1
#     z = 0
#     while running:
#         try:
#             timings = timesroute + str(i) + ']/td[' + str(j) + ']/div/div/div/table' #iterate extended xpath base through table of fixtures
#             hometeam = str(tree.xpath(timings + '/tr[5]/td[2]/div/span[1]' + '/text()')[0]) #collect fixture information
#             awayteam = str(tree.xpath(timings + '/tr[6]/td[2]/div/span[1]' + '/text()')[0])
#             day = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[1]' + '/text()')[0])
#             if day == "Today":
#                 allended = False
#             if day == "Tomorrow":
#                 runtomorrow = True
#             kickoff = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[2]' + '/text()')[0])
#             a = hometeam + " vs " + awayteam + ", " + day + " " + kickoff #format fixture information
#             fixtures.append(a)
#             z += 1 #increment game counter
#             if j == 1: #counting variables update to move through table
#                 j = 2
#             elif j == 2:
#                 i += 1
#                 j = 1
#         except Exception as e: #entered if future game not found
#             ##print(e)
#             z += 1 #increment game counter
#             if z > 12: #stop checking if game counter exceeds max number of games in a gameweek
#                 running = False
#             elif j == 1: #counting variables update to move through table
#                 j = 2
#             elif j == 2:
#                 j = 1
#                 i += 1
#             else: #stop checking in any other scenario
#                 running = False

# elif multiweek == True:
running = True
i = 1 #reset counting variables
j = 1
z = 0
k = 3
while running:
    try:
        timings = timesroute + str(i) + ']/td[' + str(j) + ']/div/div/div/table' #iterate extended xpath base through table of fixtures
        hometeam = str(tree.xpath(timings + '/tr[5]/td[2]/div/span[1]' + '/text()')[0]) #collect fixture information
        awayteam = str(tree.xpath(timings + '/tr[6]/td[2]/div/span[1]' + '/text()')[0])
        day = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[1]' + '/text()')[0])
        if day == "Today":
            allended = False
        if day == "Tomorrow":
            runtomorrow = True
        kickoff = str(tree.xpath(timings + '/tr[3]/td[3]/div/div/div/div[2]' + '/text()')[0])
        a = hometeam + " vs " + awayteam + ", " + day + " " + kickoff #format fixture information
        print(a, k)
        fixtures.append(a)
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
            if check == 1: #if next gameweek is one more than check gameweek, stop iterating
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
for i in playing: #fill content variable with formatted text
    content = content + i + "  \n"
starthour = 23 #initatiate time check variable
startmin = 59
matchtime = "23:59"
for i in fixtures:
    content = content + i + "  \n"
    if "Tomorrow" in i:
        start = int(i[-5:-3])
        if start < starthour: #find earliest game start time
            starthour = start
            startmin = i[-2:]
        if start == starthour:
            start = int(i[-2:])
            if start < int(startmin):
                startmin = start
        matchtime = str(starthour) + ":" + str(startmin)
content = content + "\n\nThis thread was posted automatically, if there are any issues please contact the mods"
print(content)
print("All ended?: " + str(allended))
print("Games tomorrow?: " + str(runtomorrow))
postid = ""
with open("starttime.txt", "r") as file:
    postid = file.read()
u.edit(postid, content)
if allended == False:
    #cron schedule in 5 mins
    timenow = datetime.datetime.now()
    mins = datetime.date.strftime(timenow, "%M")
    hrs = datetime.date.strftime(timenow, "%H")
    mins = int(mins) + 5
    if mins >= 60:
        mins -= 60
        hrs = int(hrs) + 1
    cron = CronTab(user='andrew')
    cron.remove_all(comment='update')
    cron.write()
    schedule = str(mins) + " " + str(hrs) + " * * *"
    job = cron.new(command='/usr/bin/python3 /home/andrew/code/updater.py > /home/andrew/code/updatelog 2>&1', comment = "update")
    job.setall(schedule)
    cron.write()
elif runtomorrow == True:
    #cron schedule tomorrow at matchtime
    cron = CronTab(user='andrew')
    cron.remove_all(comment='update')
    cron.write()
    schedule = str(startmin) + " " + str(starthour) + " * * *"
    job = cron.new(command='/usr/bin/python3 /home/andrew/code/updater.py > /home/andrew/code/updatelog 2>&1', comment = "update")
    job.setall(schedule)
    cron.write()
else:
    #cron schedule checker tomorrow
    cron = CronTab(user='andrew')
    cron.remove_all(comment='update')
    cron.write()
    schedule = "00 02 * * *"
    job = cron.new(command='/usr/bin/python3 /home/andrew/code/gamechecker.py > /home/andrew/code/checkerlog 2>&1', comment = "checker")
    job.setall(schedule)
    cron.write()