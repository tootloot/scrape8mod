import sys
import re
import time
import csv

def parsetimestring(timestring):
    timeobj = time.strptime(timestring, "%m/%d/%y (%a) %H:%M:%S")
    return timeobj

def parseaction(actionstring):
    def makeregex(string):
        return re.search(re.compile(string), actionstring)

    result = {}
    delete = makeregex(r"[Dd]ele")
    post = makeregex(r"[Pp]ost")
    postno = makeregex(r"#\d{4,8}")
    ban = makeregex(r"[Bb]an")
    locked = makeregex(r"[Ll]ock")
    clear = makeregex(r"[Cc]lear")
    report = makeregex(r"[Rr]eport")
    file = makeregex(r"[Ff]ile")
    bumplock = makeregex(r"[Bb]umplock")
    dismiss = makeregex(r"[Dd]ismiss")
    spoiler = makeregex(r"[Ss]poiler")
    edit = makeregex(r"[Ee]dit")
    cycle = makeregex(r"([Cc]ycle)|([Cc]yclical)")
    demote = makeregex(r"[Dd]emote")
    settings = makeregex(r"[Ss]ettings")
    board = makeregex(r"[Bb]oard")
    thread = makeregex(r"[Tt]hread")
    promote = makeregex(r"[Pp]romote")
    unstickie = makeregex(r"[Uu]nstickie")
    stickie = makeregex(r"[Ss]tickie")
    volunteer = makeregex(r"[Vv]olunteer")
    created = makeregex(r"[Cc]reated")
    reopened = makeregex(r"[Rr]e-open")

    if postno:
        if thread:
            result["ThreadNumber"] = actionstring[postno.regs[0][0]:postno.regs[0][1]]
        else:
            result["PostNumber"] = actionstring[postno.regs[0][0]:postno.regs[0][1]]
    if delete:
        if post:
            if file:
                result["Type"] = "File deletion"
            else:
                result["Type"] = "Post deletion"
        elif thread and file:
            result["Type"] = "Delete all posts in thread"
    elif spoiler and file:
        result["Type"] = "File spoiler"
    elif edit and post:
        result["Type"] = "Post edit"
    elif edit and board and settings:
        result["Type"] = "Edited board settings"
    elif cycle:
        result["Type"] = "Post cycled"
    elif ban:
        result["Type"] = "Ban"
        reason = re.search(re.compile(r"reason:"), actionstring)
        if reason:
            result["Reason"] = actionstring[reason.regs[0][0]:]
        length = re.search(re.compile(r"\d{1,4}.(([Dd]ay)|([Mn]onth)|([Hh]our)|([Yy]ear)|([Ww]eek))"), actionstring)
        if length:
            result["Length"] = actionstring[length.regs[0][0]:length.regs[0][1]]
    elif bumplock:
        result["Type"] = "Bumplock"
    elif locked:
        result["Type"] = "Lock thread"
    elif dismiss and report:
        result["Type"] = "Dismiss report"
    elif demote and report:
        result["Type"] = "Demoted report"
    elif promote and report:
        result["Type"] = "Promoted report"
    elif reopened and report:
        result["Type"] = "Re-opened report"
    elif clear and report:
        result["Type"] = "Clear reports"
    elif unstickie:
        result["Type"] = "Unstickied thread"
    elif stickie:
        result["Type"] = "Stickied thread"
    elif created and volunteer:
        result["Type"] = "Created volunteer"
    else:
        result["Type"] = "Unknown"
    return result


def parseline(inputline):
    result = {}
    repattern = re.compile(": ")
    splitindex = repattern.search(inputline)
    timestring = inputline[0:splitindex.regs[0][0]]
    timeobj = parsetimestring(timestring)
    result["time"] = timeobj
    actionstring = inputline[splitindex.regs[0][1]:].rstrip()
    result["actiondict"] = parseaction(actionstring)
    result["actionstring"] = inputline[splitindex.regs[0][1]:].rstrip()
    return result


def readfile(filename):
    try:
        with open(filename, "r+") as inputfile:
            lines = inputfile.readlines()
            result = []
            for line in lines:
                parsed = parseline(line)
                result.append(parsed)
            return result
    except:
        sys.exit("input file error")

def writecsv(timeactionlist, board):
    filename = "resultfile-" + board + "-" + time.strftime("%Y:%m:%d-%H:%M:%S") + ".csv"
    print("Writing processed data to output CSV file " + filename)
    with open(filename, "w") as outputfile:
        writer = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        keys = ["Type", "PostNumber", "ThreadNumber", "Reason", "Length"]
        writer.writerow(keys + ["Timestamp"] + ["RawString"])
        for line in timeactionlist:
            linedict = line.get("actiondict")
            row = []
            for key in keys:
                row.append(linedict.get(key, ""))
            timeval = line.get("time")
            timestamp = time.strftime("%m/%d/%Y, %H:%M:%S", timeval)
            writer.writerow(row + [timestamp] + [line.get("actionstring")])


def main():
    if len(sys.argv) is not 3:
        print("Usage: \"processdata.py <datafile> <board>\"")
        sys.exit("No valid filename")
    else:
        liststringdict = readfile(sys.argv[1])
        writecsv(liststringdict, sys.argv[2])

