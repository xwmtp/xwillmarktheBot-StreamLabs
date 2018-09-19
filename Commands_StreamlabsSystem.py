#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime
import time
import re
import json



# import Helpers

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "XWillCommands"
Website = "https://www.twitch.tv/xwillmarktheplace"
Description = "Extra commands for channel"
Creator = "XWillMarkThePlace"
Version = "1.0.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
#bingoPB = "01:21:33"
blackoutPB = "4:21:32"

bingoURL = "http://www.speedrunslive.com/tools/oot-bingo/"
noSariaURL = "http://www.buzzplugg.com/bryan/v9.2nosaria/example/"
raceURL = "#srl-"
bingoCard = "No bingo card has been set."
raceID = ""
skullCounter = 1
heartsCounter = 1
twoSmileys = False

# https://www.speedrun.com/api/v1/games/j1l9qz1g/categories
# https://www.speedrun.com/api/v1/games/76rkv4d8/categories

categories = {
    "glitchless tab" : "zd35jnkn", "glitchless any%" : "gq79gxpl", "glitchless bug limit" : "xqk98nd1", "glitchless 100%" : "p1259gk1",
    "glitchless variables" : "7890o58w",
    "mst" : "jdrwr0k6",
    "no im/ww" : "9d85yqdn",
    "all dungeons" : "zdnoz72q",
    "100%" : "q255jw2o",
    "no ww" : "xd1wj828",
    "any%" : "z275w5k0",
    "mweep%" : "vdoqyevk",
    "child_dungeons tab" : "9kvjpxjk", "child_dungeons" : "5q82gkkq", "child_dungeons rba" : "4qy5nz71", "child_dungeons glitchless" : "mlnd58d1",  "child_dungeons as adult" : "jq6y2571",  "child_dungeons variables" : "6nj99684",
    "dampe HP rta" : "7kjrx3x2",
    "dank%" : "q254ym8d",
    "jotwad" : "zd36j48d",
    "master sword rta" : "zdnq68qd",
    "reverse dungeon order" : "02qomy7k",
    "37_ water keys" : "xk9lqvyk",
    "all cows" : "z277n1g2",
    "all gold skulltulas" : "n2y1wo82",
    "all medallions" : "5dw56r5d",
    "go home and die%" : "w2014evk",
    "no major skips" : "mkezl3jk",
    "bingo" : "none"
}
# categories with subtabs
varCategories = {
    "glitchless",
    "child_dungeons"
}
# category extensions
extCategories = {
    "child_dungeons",
    "mweep",
    "dampe",
    "jotwad",
    "dank",
    "master sword rta",
    "reverse dungeon order",
    "37_ water keys",
    "all cows",
    "all gold skulltulas",
    "all medallions",
    "go home and die%",
    "no major skips"
}

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():

    global blacklist_dict
    blacklist_dict = {"scaramanga" : ["1:00:37"]}

    global bingoPlayer
    bingoPlayer = Player("xwillmarktheplace")

    global bingoPlayers
    bingoPlayers = {"xwillmarktheplace" : bingoPlayer}

    global alias_dict
    alias_dict = {"phoenixfeather1" : "phoenixfeather"}

    global clip_list
    clip_list = load_clips()

    global stopwords
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
                 "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot",
                 "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few",
                 "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
                 "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
                 "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
                 "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
                 "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
                 "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's",
                 "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
                 "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's",
                 "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
                 "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

    return

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    m = data.GetParam(0).lower()
    mess = data.Message.lower()

    if mess.startswith(bingoURL) or mess.startswith(noSariaURL):
        setBingo(data)
    if m == "!card" or m == "!seed" or m == "!board":
        card()
    if m.startswith(raceURL):
        setRace(data)
    elif m == "!race" or m == "!entrants":
        race()
    elif m == "!skulls":
        hundoSkulls(data)
    elif m == "!hearts":
        hundoHearts(data)
    elif m == "!wr":
        wr(data)
    elif m == "!pb":
        pb(data)
    elif m == "!userpb" or m == "!bingopb":
        userpb(data)
    elif m == "!average" or m == "!median" or m == "!results":
        bingoStats(data)
    elif mess == "!command" or m == "!commands" or m == "!comands" or m == "!comand":
        command(data)
    elif "zora tunic" in mess or "blue tunic" in mess or "blauwe tuniek" in mess or "zora tuniek" in mess or "tunique bleu" in mess or "tunique bleu" in mess:
        tunic(data)
    elif m == "!monkas" or m == "!monka":
        monka(data)
    elif "monkaStare" in mess:
        monkaStare(data)
    elif " owl" in mess or "owl " in mess or "parrot" in mess:
        owl(data)
    elif m == "!clip" or m == "!clips":
        clip_check(data)
    elif mess == ":)":
        smiley(data)
    else:
        global twoSmileys
        twoSmileys = False
    return


#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return


#Bingo
def setBingo(data):
    if Parent.HasPermission(data.User, "Caster", ""):
        global bingoCard
        bingoCard = data.Message
        seed = re.search(r'seed=\d+', data.Message).group(0)
        seed = str.replace(seed, "seed=", "")
        Parent.SendTwitchMessage("The !card command has been updated (seed " + seed +").")

def card():
    Parent.SendTwitchMessage(bingoCard)


def setRace(data):
    if Parent.HasPermission(data.User, "Caster", ""):
        global raceID
        id = data.Message.replace("#srl-", "")
        raceID = id

        entrants = get_entrants_string(id)

        message = "The !race command has been updated (#srl-" + id + ")." + entrants
        Parent.SendTwitchMessage(message)
def race():
    if raceID == "":
        Parent.SendTwitchMessage("No race has been set yet.")
        return
    entrants = get_entrants_string(raceID)
    message = "http://www.speedrunslive.com/race/?id="+raceID+entrants
    Parent.SendTwitchMessage(message)

def get_entrants_string(id):

    data = readjson_funct("http://api.speedrunslive.com/races/" + id + "?callback=renderEntrants")
    state = data['statetext']

    names = []
    for entrant in data['entrants'].values():
        name = entrant['displayname']
        rank = entrant['trueskill']
        names.append(name + " (" + str(rank) + ")")

    entrants = " Entrants: " + ", ".join(names)

    #entrant_info = {"entrants " : entrants}
    #entrant_info

    return entrants



#def get_entrants(   qa)

def hundoSkulls(data):
    if Parent.HasPermission(data.User, "Caster", ""):
        try:
            if data.GetParam(1) != "":
                n = int(str.replace(data.Message, "!skulls ", ""))
                if n > 100:
                    n = 100
                if n < 1:
                    n = 1
            else:
                n = skullCounter
        except ValueError:
            Parent.SendTwitchMessage("Please use an integer as argument for !skulls.")
            return
        n = printLines("HundoSkulls.txt", n, 100, 5)
        global skullCounter
        skullCounter = n

def hundoHearts(data):
    if Parent.HasPermission(data.User, "Caster", ""):
        try:
            if data.GetParam(1) != "":
                n = int(str.replace(data.Message, "!hearts ", ""))
                if n > 36:
                    n = 36
                if n < 1:
                    n = 1
            else:
                n = heartsCounter
        except ValueError:
            Parent.SendTwitchMessage("Please use an integer as argument for !hearts.")
            return
        n = printLines("HundoHearts.txt", n, 36, 5)
        global heartsCounter
        heartsCounter = n

def printLines(file, start, max, incr):
    n = start


    try:
        text = open(".\Services\Scripts\CommandScript\\" + file, "r")
    except IOError:

        Parent.SendTwitchMessage("Document could not be opened.")
        return
    lines = text.read().split('\n')


    for i in range(0, incr):
        if n > max:
            break
        Parent.SendTwitchMessage(lines[n - 1])
        n += 1
    if n > max:
        n = 1
    return n





def wr(data):
    title = readjson("https://decapi.me/twitch/title/" + Parent.GetChannelName(), jsonConv=False)

    if data.GetParam(1) == "":
        cat = checkCat(title.lower())
    else:
        cat = checkCat(data.Message.replace("!wr ","").lower())

    if cat == "error":
        if data.GetParam(1) == "":
            Parent.SendTwitchMessage("No WR found for current stream.")
        else:
            Parent.SendTwitchMessage("No WR found for given category.")
        return

    #Parent.SendTwitchMessage(cat)

    game = "j1l9qz1g"  # oot
    for extCat in extCategories:
        if extCat in cat:
            game = "76rkv4d8" #extensions
            break
    #Parent.SendTwitchMessage(game)


    url = "https://www.speedrun.com/api/v1/games/" + game + "/categories"
    wrData = readjson(url)['data']
    #Parent.SendTwitchMessage(url)
    #Parent.SendTwitchMessage(categories[cat])
    wrTime = None
    for i in range(len(wrData)):
        catData = wrData[i]
        for varCat in varCategories:
            if cat.split(" ")[0] == varCat and catData['id'] == categories[varCat + " tab"]:
                wrTime, name = getWrInfo(categories[varCat + " tab"], game, categories[varCat + " variables"], categories[cat])
                break
        if catData['id'] == categories[cat]:
            #Parent.SendTwitchMessage(catData['id'])
            wrTime, name = getWrInfo(categories[cat], game)
            break

    cat = cat.replace("_", " ")
    if cat == "bingo":
        Parent.SendTwitchMessage("There's no such thing as a bingo WR Kappa")
    elif wrTime == None:
        Parent.SendTwitchMessage("No WR found for OoT " + cat + ".")
    else:
        Parent.SendTwitchMessage("The current world record for OoT " + cat + " is " + wrTime + " by " + name + ".")



def pb(data):
    title = readjson("https://decapi.me/twitch/title/" + Parent.GetChannelName(), jsonConv=False)

    if data.GetParam(1) == "":
        cat = checkCat(title.lower())
    else:
        cat = checkCat(data.Message.replace("!pb ","").lower())

    if cat == "error":
        if data.GetParam(1) == "":
            Parent.SendTwitchMessage("No PB found for current stream.")
        else:
            Parent.SendTwitchMessage("No PB found for given category.")
        return

    url = "https://www.speedrun.com/api/v1/users/kjppz52j/personal-bests"
    pbData = readjson(url)['data']


    pbTime = None
    for i in range(len(pbData)):
        run = pbData[i]['run']
        if cat.split(" ")[0] == "glitchless":
            if run['category'] == categories["glitchless tab"] and run['values'][categories["glitchless variables"]] == categories[cat]:
                pbTime = getTime(run)
        elif run['category'] == categories[cat]:
            pbTime = getTime(run)
    if cat == "bingo":
        pbTime = str(bingoPB("xwillmarktheplace", "v92")) + " (v9.2), " + str(bingoPB("xwillmarktheplace", "v93")) + " v(9.2)" 
    elif cat == "blackout":
        pbTime = blackoutPB

    cat = cat.replace("_", " ")
    if pbTime == None:
        Parent.SendTwitchMessage("No PB found yet for OoT " + cat + ".")
    else:
        Parent.SendTwitchMessage("My current PB for OoT " + cat + " is " + pbTime + ".")





def userpb(data):
    title = readjson("https://decapi.me/twitch/title/" + Parent.GetChannelName(), jsonConv=False)

    if data.GetParam(0).lower() == "!bingopb":
        cat = "bingo"
    elif data.GetParam(1) == "":
        Parent.SendTwitchMessage("Provide a username please!")
        return
    elif data.GetParam(2) == "":
        cat = checkCat(title.lower())
    else:
        cat = checkCat(data.Message.replace("!pb " + data.GetParam(1) + " ", "").lower())
    username = data.GetParam(1)



    if cat == "error":
        if data.GetParam(2) == "":
            Parent.SendTwitchMessage("No PB found for current stream.")
        else:
            Parent.SendTwitchMessage("No PB found for given category.")
        return

    game = "j1l9qz1g"  # oot
    for extCat in extCategories:
        if extCat in cat:
            game = "76rkv4d8" #extensions
            break

    url = "https://www.speedrun.com/api/v1/games/" + game + "/categories"
    userData = readjson(url)['data']
    # Parent.SendTwitchMessage(url)
    # Parent.SendTwitchMessage(categories[cat])
    userTime = None
    for i in range(len(userData)):
        catData = userData[i]
        for varCat in varCategories:
            if cat.split(" ")[0] == varCat and catData['id'] == categories[varCat + " tab"]:
                userTime = getUserTime(username, categories[varCat + " tab"], game, categories[varCat + " variables"],
                                         categories[cat])
                break
        if catData['id'] == categories[cat]:
            # Parent.SendTwitchMessage(catData['id'])
            userTime = getUserTime(username, categories[cat], game)
            break
    cat = cat.replace("_", " ")
    if cat == "bingo":
        userTime = str(bingoPB(username))
    if userTime == None:
        return
    else:
        Parent.SendTwitchMessage(username + "'s PB for OoT " + cat + " is " + userTime + ".")






def getTime(run):
    seconds = run['times']['primary_t']
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def getWrInfo(catID, game = "j1l9qz1g", var = None, varID = None):
    baseURL ="https://www.speedrun.com/api/v1/leaderboards/" + game + "/category/" + catID + "?top=1"
    if var != None:
        baseURL += "&var-" + var + "=" + varID
    #Parent.SendTwitchMessage(baseURL)
    category = readjson(baseURL)

    run = category['data']['runs'][0]['run']

    wrTime = getTime(run)

    nameURL = run['players'][0]['uri']
    nameData = readjson(nameURL)
    name = nameData['data']['names']['international']
    return (wrTime, name)

def getUserTime(username, catID, game = "j1l9qz1g", var = None, varID = None):
    baseURL ="https://www.speedrun.com/api/v1/leaderboards/" + game + "/category/" + catID


    if var != None:
        baseURL += "?&var-" + var + "=" + varID
    category = readjson(baseURL)


    userURL = "https://www.speedrun.com/api/v1/users?lookup="+username
    userData = readjson(userURL)

    if userData['data'] == []:
        Parent.SendTwitchMessage("Username cannot be found.")
        return None
    else:
        userID = userData['data'][0]['id']


    runs = category['data']['runs']

    #Parent.SendTwitchMessage(str(len(runs))) get amount of runs!
    for i in range(len(runs)):
        run = runs[i]['run']
        if 'id' in run['players'][0] and run['players'][0]['id'] == userID:
            runTime = getTime(run)

            return runTime

    Parent.SendTwitchMessage("No record found for " + username + ".")
    return None


# Post random monka emote
def monka(data):
    if not Parent.IsOnCooldown(ScriptName, "!monkaS"):
        Parent.AddCooldown(ScriptName, "!monkaS", 5)
        url = "https://api.frankerfacez.com/v1/room/xwillmarktheplace"
        mData = readjson(url)
        emotes = mData['sets']['164185']['emoticons']

    monka = []
    for i in range(len(emotes)):
        name = emotes[i]['name']
        if "monka" in name:
            monka.append(name)
    int = Parent.GetRandom(0, len(monka)-1)
    Parent.SendTwitchMessage(monka[int])

# Post monkaStare with chance
def monkaStare(data):
    int = Parent.GetRandom(0, 100)
    if int < 40:
        Parent.SendTwitchMessage("monkaStare")

# Post badTunic
def tunic(data):
    int = Parent.GetRandom(0, 100)
    if int < 101:
        Parent.SendTwitchMessage("BadTunic")

def command(data):
    if not Parent.IsOnCooldown(ScriptName, "!commands"):
        Parent.AddCooldown(ScriptName, "!commands", 20)
        Parent.SendTwitchMessage("List of commands: https://pastebin.com/aQEG2T5D")

def smiley(data):
    if not Parent.IsOnCooldown(ScriptName, "!smiley"):
        global twoSmileys
        if twoSmileys:
            int = Parent.GetRandom(0, 100)
            if int < 45:
                Parent.SendTwitchMessage(":)")
            twoSmileys = False
            Parent.AddCooldown(ScriptName, "!smiley", 360)
        else:
            twoSmileys = True

def owl(data):
    if "parrot" in data.Message:
        Parent.SendTwitchMessage("DontYouNotWishForMeToNotRepeat")
        Parent.AddCooldown(ScriptName, "!owl", 120)
    else:
         int = Parent.GetRandom(0, 100)
         if not Parent.IsOnCooldown(ScriptName, "!owl") and int < 35 :
             Parent.SendTwitchMessage("DontYouNotWishForMeToNotRepeat")
             Parent.AddCooldown(ScriptName, "!owl", 360)






#### CLIPS


class Clip:

    def __init__(self, line):
        parts = line.split(";")
        self.name = parts[0]
        self.link = parts[1]
        try:
            self.keywords = parts[2].split(',')
        except:
            self.keywords = []

    def print_clip(self):
        Parent.SendTwitchMessage(self.name + " " + self.link)


def load_clips():
    try:
        text = open(".\Services\Scripts\CommandScript\clips.txt", "r")
    except IOError:
        Parent.SendTwitchMessage("CLips document could not be opened.")
        return
    lines = text.read().split('\n')

    clip_list = []
    for line in lines:
        clip = Clip(line)
        clip_list.append(clip)

    return clip_list

def clip_check(data):

    global clip_dict


    param = data.GetParam(1).lower()

    if param == "":
        int = Parent.GetRandom(0, len(clip_list))
        clip = clip_list[int]
        clip.print_clip()
        return

    i = 1
    params = []
    while param != "":
        params.append(param)
        i = i+1
        param = data.GetParam(i).lower()

    terms = [p for p in params if p not in stopwords]
    title = ' '.join(params)


    for clip in clip_list:
        if clip.name == title:
            clip.print_clip()
        else:
            terms
























def checkCat(title):
    if "bug limit" in title:
        return "glitchless bug limit"
    if "glitchless" in title:
        if "100%" in title or "hundo" in title:
            return "glitchless 100%"
        elif "child dungeons" in title:
            return "child_dungeons glitchless"
        else:
            return "glitchless any%"
    if "no im" in title:
        return "no im/ww"
    if "child dungeons" in title:
        if "adult" in title:
            return "child_dungeons as adult"
        elif "rba" in title:
            return "child_dungeons rba"
        else:
            return "child_dungeons"
    if "37" in title and "key" in title:
        return "37_ water keys"
    if "gold" and "skull" in title:
        return "all gold skulltulas"
    if "all" in title and "cows" in title:
        return "all cows"
    if "go home" in title and "die" in title:
        return "go home and die%"
    for name in {"mweep", "dank", "any"}:
        if name in title:
            return name + "%"
    for name in {"jotwad", "master sword rta", "all medallions"}:
        if name in title:
            return name
    for name, name2 in {("reverse dungeon order", "rdo"), ("all dungeons", "ad"), ("mst", "medallions, stones, trials"), ("no ww", "no wrong warp"), ("100%", "hundo"), ("no major skips", "nms")}:
        if name in title or name2 in title:
            return name
    if "bingo" in title or "snb" in title:
        return "bingo"
    if "blackout" in title:
        return "blackout"
    return "error"


def printList(list):
    for i in range(len(list)):
        Parent.SendTwitchMessage(list[i])

def readjson(url, jsonConv = True, printMessage = True, delete_function = False):
    response = Parent.GetRequest(url, {})

    if delete_function:

        #match = re.search(r"[^\(]+\(", response, re.IGNORECASE)
        #if match:
            #Parent.SendTwitchMessage(match.group())
        response = response.replace(r"\"\nrenderEntrants(", "") # replace first function (renderEntrants)
        response = response [:-4] # delete last )

    responseObj = json.loads(response)

    if responseObj["status"] == 200:
        result = responseObj["response"]
        if jsonConv:
            result = json.loads(result)
    else:
        if printMessage:
            Parent.SendTwitchMessage("Error in accessing api.")
        return None
    return result


def readjson_funct(url, jsonConv = True, printMessage = True):
    #Parent.SendTwitchMessage(url)
    response = Parent.GetRequest(url, {})

            #Parent.SendTwitchMessage(match.group())
    response = response[53:]
    response = response [:-5] # delete last )
    response = response.replace("\\\"", "\"")
    response = response.replace(r"\n", "")

    #Parent.SendTwitchMessage(response)
    responseObj = json.loads(response)
    return responseObj

    if responseObj["status"] == 200:
        result = responseObj["response"]
        if jsonConv:
            result = json.loads(result)
    else:
        #Parent.SendTwitchMessage(url)
        if printMessage:
            Parent.SendTwitchMessage("Error in accessing api.")
        return None
    return result



















############ READ BINGOS ===================


def bingoStats(data):
    command = data.GetParam(0).lower()
    player = bingoPlayer
    orig = bingoPlayer.name
    n = 15

    i = 1
    while(True):
        param = data.GetParam(i)

        if param == "":
            break

        if param.isdigit():
            n = int(data.GetParam(i))
        else:
            orig = param
            name = param.lower()
            if name in alias_dict.keys():
                name = alias_dict[name]
            player = getPlayer(name)
        i = i + 1

    if command == "!average" or command == "!median":
        #Parent.SendTwitchMessage(player.name)

        avg = player.get_average(n = n, avg=command[1:])
        value = str(avg)

    if command == "!results":
        races = bingoPlayer.get_races(n=n, type="v92", sort = "latest")
        times = [str(race.time) for race in races]
        value = ", ".join(times)


    Parent.SendTwitchMessage(orig + "'s " + command[1:] + " for the last " + str(n) + " bingos: " + value)

def bingoPB(user, type):
    player = getPlayer(user)
    return player.get_pb(type = type)


def getPlayer(user):
    global bingoPlayers
    if user in bingoPlayers.keys():
        player = bingoPlayers[user]
    else:
        player = Player(user)
        if not hasattr(player, 'races'):  # user doesn't exist
            return
        else:
            bingoPlayers[user] = player
    return player





V92 = 'http://www.speedrunslive.com/tools/oot-bingo?mode=normal'
NoSaria = 'http://www.buzzplugg.com/bryan/v9.2NoSaria/example/bingo.html'


class Race:

    def __init__(self, date, time, url, comment, player):
        self.date = date
        self.time = time
        self.url = url
        self.seed = extract_seed(url)
        self.type = extract_type(url, date)
        self.player = player
        self.comment = comment
        self.row = regex_to_row(extract_row(comment))

    def isBingo(self):
        return "bingo" in self.url


    def print_race(self, url = False):
        print_list = [str(self.date), str(self.time), self.type, self.seed, self.row, self.comment,]
        if url:
            print_list.append(self.url)
        print("\t".join(print_list))


def retrieve_race_info(race, player, v92 = True, noSaria=True, rest = False):
    for entrant in race["results"]:
        if entrant["player"].lower() == player.lower():

            time = entrant["time"]

            goal = race["goal"]

            # date = pd.to_datetime(race["date"], unit="s").date()
            date = int(race["date"])
            comment = ""

            if time == -1 or "bingo" not in goal: # ((not v92) and goal.startswith(V92)) or ((not noSaria) and goal.startswith(NoSaria)):
                continue
            elif not rest:
                continue
            if player.lower() != "xwillmarktheplace":
                Parent.SendTwitchMessage(goal)
            time = datetime.timedelta(seconds=time)

            comment = entrant["message"]

            return (date, time, goal, comment)

def extract_row(comment):
    s = "((((r(ow)?)|(c(ol)?))( )?(\d))|(tl(-| )?br)|(bl(-| )?tr))"

    m = re.search(s, comment, re.IGNORECASE)
    if m:
        return m.group().lower()
    else:
        return "BLANK"

def extract_type(url, date):
    if 'http://www.speedrunslive.com/tools/oot-bingo?mode=normal' in url:
        return "v92"
    elif url.startswith('http://www.buzzplugg.com/bryan/v9.2NoSaria/'):
        return "NoSaria"
    elif "blackout" in url:
        return "blackout"
    for name in {"v4", "v5", "v6", "v7", "v8", "v9.1"}:
        if name in url.lower():
            return name
    if "series" or "championship" in url:
        return "ocs "
    if not url.startswith('http://'):
        return 'other'

    else:
        cat = checkCat(url)
        if cat == "error":
            return "UNKNOWN"
        else:
            return cat

def extract_seed(url):
    seed = re.search(r"seed=(\d)+", url)
    if seed:
        seed = seed.group()
    else:
        seed = "-----"
    digit = seed.replace("seed=","")
    return digit



def regex_to_row(reg):
    if reg == "blank":
        return reg
    digit = re.search(r"\d", reg)
    if digit:

        if reg.startswith("r"):
            return "row" + digit.group()
        else:
            return "col" + digit.group()

    else:
        row = reg.replace("-", "")
        row = row.replace(" ", "")
        return row








class Player:

    def __init__(self, name, from_file=False):
        self.name = name

        #try:
        self.json = readjson("http://api.speedrunslive.com/pastraces?player=" + name + "&pageSize=1000", jsonConv=True, printMessage=False)
        if not self.json:
            userURL = "https://www.speedrun.com/api/v1/users?lookup=" + name
            userData = readjson(userURL)
            if userData["data"] == []:
                Parent.SendTwitchMessage("User not found.")
            else:
                name = userData['data'][0]['names']['international']
                self.__init__(name, from_file)
                return
        results = []
        for race in self.json["pastraces"]:
            tuple = retrieve_race_info(race, name, rest=True)
            if tuple != None:
                (date, time, goal, comment) = tuple
                results.append(Race(date, time, goal, comment, name))
        self.races = results
        self.bingos = [race for race in self.races if race.type == "v92"]
        if (self.bingos == []) or (self.bingos is None):
            Parent.SendTwitchMessage("No recorded bingo races found for user {}.".format(self.name))
        #Parent.SendTwitchMessage(str(len(self.bingos)))

        if self.name.lower() in blacklist_dict.keys():
            self.blacklist = blacklist_dict[self.name]

    def get_races(self, n=-1, type = "v92", sort = "best"):

        races = self.select_races(type)

        if n==-1:
            n = len(races)

        if sort == "best":
            sorted_bingos = sorted(races, key=lambda r: r.time)
        elif sort == "latest":
            sorted_bingos = sorted(races, key=lambda r: r.date, reverse=True)
        else:
            sorted_bingos = races
        return sorted_bingos[:n]

    def get_average(self, n=15, type = "v92", avg="average"):
        races = self.select_races(type, sort="latest")[:n]

        times = extract_times(races, seconds=True)
        if times == []:
            return

        if avg == "average" or avg == "mean":
            res = int(mean(times))
        else:
            res = int(median(times))
        return datetime.timedelta(seconds=res)#.replace(microseconds = 0)

    def get_pb(self, type = "v92"):
        race = self.select_races(type)[0]
        return race.time


    def select_races(self, type="v92", sort="best", remove_blacklisted=True):
        if type == "bingo":
            races = self.bingos
        elif type == "v92":
            races = [race for race in self.races if race.type == "v92"]
        elif type == "v93":
            races = [race for race in self.races if race.type == "v93"]
        elif type == "v92+":
            races = [race for race in self.races if ((race.type == "v92") | (race.type == "v93"))]
        else:
            races = self.races

        if sort == "best":
            races = sorted(races, key=lambda r: r.time)
        elif sort == "latest":
            races = sorted(races, key=lambda r: r.date, reverse=True)

        if remove_blacklisted and self.name in blacklist_dict.keys():
            races = [race for race in races if str(race.time) not in self.blacklist]

        return races





def extract_times(races, seconds = True):
    if seconds:
        return [race.time.total_seconds() for race in races]
    else:
        return [race.time for race in races]

def mean(times):
    times = sorted(times)
    return sum(times)/len(times)

def median(times):
    times = sorted(times)

    mid = int(len(times) / 2)

    if len(times) % 2 == 0:
        median = (times[mid-1] + times[mid])/2
    else:
        median = times[mid]

    return median









