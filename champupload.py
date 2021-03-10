import praw, re
from datetime import datetime

def update(subreddit, data = "", form = "", lastmatch = "", nextmatch = "", topscorers = ""):
#    data = "test"
    user_agent = "Sidebar updater by /u/coombeseh"
    r = praw.Reddit(client_id = "jTU9fuDigFxLyA",
                    client_secret = "kwjxGHuBhisqjMxEgD8zQ11VLL0",
                    user_agent = user_agent,
                    username = "coombeseh",
                    password = "C0omb3s")
    
    sub = r.subreddit(subreddit)
    settings = sub.mod.settings()
    desc = settings['description']
    a = desc

    if subreddit == "urz":
        if data != "":
            tablesplit = re.split(":---\|:--:\|:--:\|:--:\|---:", a)
            rest = tablesplit[1]
            end = re.split("\|\|\|\|\|", rest)
            postdata = tablesplit[0] + data + end[1]
            a = postdata
            
    elif subreddit == "championship":
        if data != "":
            tablesplit = re.split(":--:\|:--\|:--:\|:--:\|:--:", a)
            rest = tablesplit[1]
            end = re.split("\*\^Last \^Updated:", rest)
            postdata = tablesplit[0] + data + end[1]
            a = postdata

    if form != "":
        formsplit = re.split("Last 5", a)
        rest = formsplit[1]
        end = re.split("\_\_\_\_\_", rest)
        postform = formsplit[0] + form + end[1]
        a = postform

    if lastmatch != "":
        lastmatchsplit = re.split("Last Match", a)
        rest = lastmatchsplit[1]
        end = re.split("Next Match", rest)
        postlastmatch = lastmatchsplit[0] + lastmatch + end[1]
        a = postlastmatch

    if nextmatch != "":
        nextmatchsplit = re.split("Next Match", a)
        rest = nextmatchsplit[1]
        end = re.split("Championship Table", rest)
        postnextmatch = nextmatchsplit[0] + nextmatch + end[1]
        a = postnextmatch

    if topscorers != "":
        scorersplit = re.split("Top Scorers", a)
        rest = scorersplit[1]
        end = re.split("## Cup Competitions", rest)
        postscorers = scorersplit[0] + topscorers + end[1]
        a = postscorers

    complete = a
    
    if subreddit == "urz":
        updatereplace = re.split("autoupdate", a)
        b = str(datetime.now())
        c = re.split("\.", b)[0]
        d = "autoupdate was " + c
        complete = updatereplace[0] + d

    elif subreddit == "championship":
        updatereplace = re.split("\*\^Last \^Updated:", a)
        rest = updatereplace[1]
        end = re.split("See", rest)
        b = str(datetime.now())
        c = re.split("\.", b)[0]
        e = re.split("\ ", c)
        d = "*^Last ^Updated: ^" + e[0] + " ^" + e[1] + " ^- ^See"
        complete = updatereplace[0] + d + end[1]
    
    settings['description'] = complete
    sub.mod.update(description = complete)

def bold(x):
    if x == "W":
        x = "**W**"
    return x

def pm(uname, subject, content):
    user_agent = "Sidebar updater by /u/coombeseh"
    r = praw.Reddit(client_id = "jTU9fuDigFxLyA",
                    client_secret = "kwjxGHuBhisqjMxEgD8zQ11VLL0",
                    user_agent = user_agent,
                    username = "coombeseh",
                    password = "C0omb3s")
    r.redditor(uname).message(subject, content)

def post(subreddit, title, content):
    user_agent = "Sidebar updater by /u/coombeseh"
    r = praw.Reddit(client_id = "jTU9fuDigFxLyA",
                    client_secret = "kwjxGHuBhisqjMxEgD8zQ11VLL0",
                    user_agent = user_agent,
                    username = "coombeseh",
                    password = "C0omb3s")
    sub = r.subreddit(subreddit)
    a = sub.submit(title, selftext=content, send_replies=False)
    return(a)

def edit(permalink, content):
    user_agent = "Sidebar updater by /u/coombeseh"
    r = praw.Reddit(client_id = "jTU9fuDigFxLyA",
                    client_secret = "kwjxGHuBhisqjMxEgD8zQ11VLL0",
                    user_agent = user_agent,
                    username = "coombeseh",
                    password = "C0omb3s")
    a = r.submission(id=permalink)
    a.edit(content)
