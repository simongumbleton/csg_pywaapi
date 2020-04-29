import csg_pywaapi
import sys
from pprint import pprint



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

## Do some opertation on each object that was passed in
for id in ids:
    print("This is where you do your operations on each object")




# Close the undo groupr
csg_pywaapi.endUndoGroup("MyUndoGroup")

##### Pause the script to display results ###### 
input('Press <ENTER> to continue')

# Exit
csg_pywaapi.exit()