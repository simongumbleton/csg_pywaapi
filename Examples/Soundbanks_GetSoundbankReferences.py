import csg_pywaapi
import sys
import csg_helpers.gui as gui
from pprint import pprint


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
    #gui.showMessageforXseconds(message,5)


#Connect to Wwise
result = csg_pywaapi.connect()
if not result:
    exit()

#Setup an undo group
csg_pywaapi.beginUndoGroup()

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
    SelectedObjectBanks = csg_pywaapi.getSoundbanks("id", SelectedObject["id"])
    if SelectedObjectBanks:
        BankObjectRefs[SelectedObject["name"]] = SelectedObjectBanks
    else:
        BankObjectRefs[SelectedObject["name"]] = False



showSoundbankRefResults(BankObjectRefs)
#pprint(BankObjectRefs)

# Close the undo groupr
csg_pywaapi.endUndoGroup("MyUndoGroup")

##### Pause the script to display results ###### 
#input('Press <ENTER> to continue')

# Exit
csg_pywaapi.exit()