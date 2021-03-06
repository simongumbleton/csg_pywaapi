import csg_pywaapi
import sys

"""
This script demonstrates doing operations on multiple wwise objects passed in with sys.argv, 
or alternatively multiple currently selected wwise objects.
For each ID it gets some named properties and prints them
"""


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

## Do some opertation on each object that was passed in
for id in ids:
    # This is where you do your operations on each object
    # get some named properties from the given ID
    objectWithProperties = csg_pywaapi.getObjectProperties(id,["name","type"])
    print("Object {0} is a {1}".format(objectWithProperties["name"],objectWithProperties["type"]))


##### Pause the script to display results ###### 
input('Press <ENTER> to continue')

# Exit
csg_pywaapi.exit()