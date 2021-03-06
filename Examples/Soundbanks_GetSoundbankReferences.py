import csg_pywaapi
import sys
import csg_helpers.gui as gui
from pprint import pprint

"""
This script finds and displays any soundbanks that directly reference a given wwise object(s).
It will find direct references for the object and any ancestors in any soundbank
It does this by looking at direct inclusions as well as event action references
It demonstrates using the getSoundbanks() method and the gui helper to display results
"""

def showSoundbankRefResults(itembankrefs):
    message = ""
    for key in itembankrefs:
        if itembankrefs[key]:
            banks = ""
            for bank in itembankrefs[key]:
                banks += "{0}, ".format(bank)
            message += "{0} is referenced in {1}".format(key,banks) + "\n"
        else:
            message += "{0} is not directly referenced in any soundbank".format(key) + "\n"
    gui.messageBox(message,"Soundbank References")


#Connect to Wwise
result = csg_pywaapi.connect(8080)
if not result:
    exit()


#If run from cmd/bat/wwise then usually IDs will be passed into the args
ids = []
if (len(sys.argv) > 1):
    sysargs = set(sys.argv[1:])
    for arg in sysargs:
        ids.append(arg)

#if no args are given, then get the currently selected objects instead
if not ids:
    res = csg_pywaapi.getSelectedObjects()
    for obj in res:
        ids.append(obj["id"])

BankObjectRefs = {}
## Do some opertation on each object that was passed in
for id in ids:
    SelectedObject = csg_pywaapi.getObjectProperties(id)
    SelectedObjectBanks = csg_pywaapi.getSoundbanks(SelectedObject["id"])
    if SelectedObjectBanks:
        BankObjectRefs[SelectedObject["name"]] = SelectedObjectBanks
    else:
        BankObjectRefs[SelectedObject["name"]] = False



showSoundbankRefResults(BankObjectRefs)
#pprint(BankObjectRefs)


##### Pause the script to display results ###### 
input('Press <ENTER> to continue')

# Exit
csg_pywaapi.exit()