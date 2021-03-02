import sys
import csg_pywaapi
from pprint import pprint
from datetime import datetime


#Connect to Wwise
result = csg_pywaapi.connect()
if not result:
    exit()

csg_pywaapi.beginUndoGroup()

queryName = "Notes - ToDos"
qID = 0
extracted = "TASKED"

now = datetime.now()
date = now.strftime("%d%m%y")

query = csg_pywaapi.getObjectProperties(queryName, [], "search")
if len(query) == 0:
    print("Query not found, exiting.")
    csg_pywaapi.cancelUndoGroup()
    csg_pywaapi.exit()
    sys.exit()

qID = query[0]["id"]

query = csg_pywaapi.getObjectProperties(qID, ["notes"], "query")



ids = []
if (len(sys.argv) > 1):
    sysargs = set(sys.argv[1:])
    for arg in sysargs:
        ids.append(arg)

if not ids:
    # no arg given, use selected object instead
    res = csg_pywaapi.getSelectedObjects()
    #print(res)
    for obj in res:
        ids.append(obj["id"])


targetID = ids[0]
#print(targetID)
TargetWwiseObject = csg_pywaapi.getObjectProperties(targetID, [])
SelectedPath = TargetWwiseObject["path"]
SelectedName = TargetWwiseObject["name"]
#print(SelectedName)
#print(SelectedPath)

filename = "../temp_WwiseNotes_{}_{}.csv".format(SelectedName, date)

try:
    file = open(filename,'w')
except IOError as x:
    print("Error accessing file")
    csg_pywaapi.endUndoGroup("Extract Wwise notes to CSV")
    csg_pywaapi.exit()
    sys.exit()
else:
    count = 0
    for result in query:
        #print(result["path"])
        if SelectedPath in result["path"]:
            name = result["name"]
            notesraw = result["notes"]
            notes = notesraw.replace('\n','')
            notes = notes.replace('"',"'")
            #if the notes havent been extracted
            if not extracted in notes:
                #save the name and notes out to some format
                data = name + "," + '"{}"'.format(notes)
                lineEnd = "\n"
                #   write a new line to the file
                file.write(data+lineEnd)
                #   add the extracted text to the notes
                csg_pywaapi.setNotes(result["id"], notesraw + "\n --" + extracted)
                count +=1

    file.close()

    csg_pywaapi.endUndoGroup("Extract Wwise notes to CSV")

    print("Done")
    print("Extracted {0} notes from {1}".format(count,SelectedName))

    ##### Pause the script to display results ######
    input('Press <ENTER> to continue')

    csg_pywaapi.exit()