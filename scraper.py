import requests
import sys
import time
from bs4 import BeautifulSoup
import processdata

def processmodactions(modactionslist):
    rawmodactions = modactionslist.find("table", {"class": "modlog"}).contents[1:]
    modactions = []
    for line in rawmodactions:
        linedict = {}
        timestamp = line.contents[2].find("span").attrs.get("title")
        description = line.contents[4].text
        linedict["timestamp"] = timestamp
        linedict["description"] = description
        modactions.append(linedict)
    return modactions

def listoflinks(soup):
    result = []
    otherlinks = soup.find("p", {"class": "unimportant"})
    for link in list(filter(lambda x: x.name == 'a', otherlinks.contents)):
        test = 'https://8ch.net/log.php' + link.attrs.get('href')
        result.append(test)
    return result

def appendtofile(buffer, filename):
    with open(filename, "a") as outputfile:
        outputfile.write(buffer)

def processlinks(linkstoprocess, pagelist):
    for page in otherpages:
        url = page
        print(url)
        loopresponse = requests.get(url)
        loopsoup = BeautifulSoup(loopresponse.text, "html.parser")
        pagedata = processmodactions(loopsoup)
        buffer = ""
        for line in pagedata:
            buffline = line.get("timestamp") + ": " + line.get("description") + "\n"
            buffer += buffline
        appendtofile(buffer, filename)
        pagelist += pagedata

if len(sys.argv) is not 2:
    print("Usage: \"scraper.py <boardname>\"")
    sys.exit("No valid board name")
else:
    board = sys.argv[1]
    url = 'https://8ch.net/log.php?board=' + board
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pagelist = processmodactions(soup)
    otherpages = listoflinks(soup)
    timestring = time.strftime("%Y:%m:%d-%H:%M:%S")
    filename = "scrapefile" + "-" + board + "-" + timestring + ".txt"
    processlinks(otherpages, pagelist)

    print("mod actions: " + str(len(pagelist)) + ", first timestamp: " + pagelist[0].get("timestamp") + " last timestamp: " + pagelist[-1].get("timestamp"))
    print("Processing data from output file " + filename)
    liststringdict = processdata.readfile(filename)
    processdata.writecsv(liststringdict, board)


