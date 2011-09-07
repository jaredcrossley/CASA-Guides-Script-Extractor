#!/usr/bin/env python
#
# python script intended to extract CASA code from the CASA Cookbook
# Wiki and collect it into a (CASA-executable) script. 
# Jack Gallimore 8/10/09
# Updated to accommodate new web host 10/30/09.
# Bug Fixes 12/17/09 -- jfg
# Bug fixes and added plotants to interactive command list 2/24/10 -- jfg


import urllib
import urllib2
import sys
import codecs
import re

# interactives
interactive=re.compile("(plotxy|plotcal|plotms|viewer|plotants)")

# globals

# define formatting junk that needs to be filtered
# If I were cleverer with regex the ensuing loop would probably not be necessary.
junkStr = ["<div dir=\"ltr\" style=\"text-align: left;\">"]
junkStr = junkStr + ["<div class=\"source-python\" style=\"font-family: monospace;\">"]
junkStr = junkStr + ["<pre>"]
junkStr = junkStr + ["</span>"]
junkStr = junkStr + ["</pre></div></div>"]
junkStr = junkStr + ["&nbsp;"]
paren1 = "&#40;"
paren2 = "&#41;"
brack2 = "&#93;"
brack1 = "&#91;"
sqirl1 = "&#123;"
sqirl2 = "&#125;"
quote1 = "&quot;"
lessthan = "&lt;"
greaterthan = "&gt;"
ampersand = "&amp;"
substr1 = r"<span class=[^>]*>"


# define casa code blocks
beginBlock = "class=\"source-python\""
endBlock = "</pre></div></div>"

def countParen(line):
    pcount = 0
    for char in line:
        if char == '(': pcount += 1
        if char == ')': pcount -= 1
    return pcount


# function to clean up html strings (convert html markup to executable python)
def loseTheJunk(line):
    outline = line # this should be function'd -- need to replace tgets etc as in first version of script
    outline = re.sub(substr1, r'', outline)
    for junk in junkStr:
        outline = outline.replace(junk, "")
    outline = outline.replace(quote1, "\"")
    outline = outline.replace(paren1, "(")
    outline = outline.replace(paren2, ")")
    outline = outline.replace(brack1, "[")
    outline = outline.replace(brack2, "]")
    outline = outline.replace(sqirl1, "{")
    outline = outline.replace(sqirl2, "}")
    outline = outline.replace(lessthan, "<")
    outline = outline.replace(greaterthan, ">")
    outline = outline.replace(ampersand, "&")

    #some additional parsing -- scripting has slightly different
    #syntax than interactive session for tget, default, and go
    #(presumably among others). 

    newline = outline
    newline = newline.replace(r'tget ', r'tget(')
    newline = newline.replace(r'default ', r'default(')
    if newline == 'go':
        newline = 'go('
    if newline != outline: newline = newline + ')'
    outline = newline
    return outline

# if there is an interactive command, add some pause lines after
#    intList = ["plotxy", "plotcal", "plotms","viewer","plotants"]

def addInteractivePause(outline):
    newoutline = outline
    newoutline += "\ninp()\nprint('When you are done with the graphics window,')\n"
    newoutline += "\nprint('quit that window, and')\n"
    newoutline += "\nuser_check=raw_input('press enter to continue script\\n')\n"
    return newoutline


#    mtch = interactive.match(outline)
#    if mtch:
#        # got an interactive command. Hoo boy here we go.
#        print mtch.group()

# start of main code

def main():
    try:
        baseURL = sys.argv[1]
    except:
        print 'No argument given.'
        print 'Syntax: extractCASAscript.py    \'http:blah.blah.edu/web_site/\''
        sys.exit(2)

    print "Rest assured. I'm trying to get " + baseURL + " for you now."
    outFile = baseURL.split('/')[-1] + '.py'
    outFile = outFile.replace("index.php?title=","")
    outFile = outFile.replace(":","")
    outFile = outFile.replace("_","") 
  
    req = urllib2.Request(baseURL)
    response = urllib2.urlopen(req)
    the_page = response.read().split("\n")
    
    iActive = 0
    print "Things are going well. Let me clean out some of that html markup."

    lineList = []
    for line in the_page:
        if (iActive == 0):
            # see if this line begins a python code block
            temp = line.find(beginBlock)
            if temp > -1:
                iActive = 1
                outline = loseTheJunk(line)
#                print outline
                lineList += [outline]
                temp = line.find(endBlock)
                if temp > -1:
                    iActive = 0
                line = "DontPrintMeBro" # avoid double printing if endBlock is on the same line
#                print >>f, outline
        if (iActive == 1):
            if (line != "DontPrintMeBro"):
                outline = loseTheJunk(line)
#                print outline
                lineList += [outline]
#                print >>f, outline
            temp = line.find(endBlock)
            if temp > -1:
                iActive = 0
    # OK, loaded the commands into a linelist. Now compress the lines into individual commands (allowing for commands to span multiple lines)
    # lines are grouped by closed parentheses
    compressedList = []
    iline = 0
    while iline < len(lineList):
        line = lineList[iline]
        pcount = countParen(line)
        while(pcount > 0):
            line += '\n'
            iline += 1
            line += lineList[iline]
            pcount = countParen(line)
        compressedList += [line]
        print line
        iline += 1
    print len(lineList)
    print len(compressedList)
            
    f = codecs.open(outFile, 'w','utf-8')
    for line in compressedList:
        mtch = interactive.match(line)
        if (mtch and line.find("showgui=F") == -1): line = addInteractivePause(line)
        print >>f, line
    f.close()
    print "Great. I think I just wrote the file " + outFile + " in the current directory. No promises.\n"
    print "In casapy, run the file using\n"
    print "execfile(\"" + outFile + "\")\n"
    
if __name__ == "__main__":
    main()
