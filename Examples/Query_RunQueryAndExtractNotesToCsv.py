import sys
import csg_pywaapi
from pprint import pprint
from datetime import datetime

"""
This script runs a query for a selected structure to find any wwise objects marked with "TODO" in the notes.
For any found, it extracts the TODO notes to a CSV file for tracking, and appends the string "-TASKED", which is used 
to filter subsequent searches.
To use this, specify a value for  queryName  which matches an existing query in wwise. 
In our example this query lists all items with TODO in the notes.
Select one or more objects in wwise as the structures you wish to operate on
(we do this so the mix notes can be extracted for specific areas e.g. ambience/foley/weapons etc)
for each selected object it will extract the TODO notes to a time-stamped CSV and update the notes with -TASKED

This script demonstrates use of Queries as well as filtering and operating on the results of queries
"""

#Connect to Wwise
result = csg_pywaapi.connect(8080)
if not result:
    exit()

csg_pywaapi.beginUndoGroup()

#Name of the wwise query to use
queryName = "Notes - ToDos"

#Text to append to the notes once extracted
extractedText = "TASKED"

#Optional path to specify for the CSV file, if blank will use the wwise project root folder
pathToSaveCSV = ""

now = datetime.now()
date = now.strftime("%d%m%y")

#Find the query in Wwise and get the ID of it if it exists
query = csg_pywaapi.getObjectProperties(queryName, [], "search")
if len(query) == 0 or query==False:
    print("Query not found, exiting.")
    csg_pywaapi.cancelUndoGroup()
    csg_pywaapi.exit()
    sys.exit()

if type(query) is list:
    qID = query[0]["id"]
else:
    qID = query["id"]

#Run the query and get the notes property for each result object found
query = csg_pywaapi.getObjectProperties(qID, ["notes"], "query")

#Get the list of IDs to operate on
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

for id in ids:
    TargetWwiseObject = csg_pywaapi.getObjectProperties(id, [])
    SelectedPath = TargetWwiseObject["path"]
    SelectedName = TargetWwiseObject["name"]

    if pathToSaveCSV == "":
        pathToSaveCSV = csg_pywaapi.getPathToWwiseProjectFolder()

    filename = pathToSaveCSV + "/temp_WwiseNotes_{}_{}.csv".format(SelectedName, date)

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
                if not extractedText in notes:
                    #save the name and notes out to some format
                    data = name + "," + '"{}"'.format(notes)
                    lineEnd = "\n"
                    #   write a new line to the file
                    file.write(data+lineEnd)
                    #   add the extracted text to the notes
                    csg_pywaapi.setNotes(result["id"], notesraw + "\n --" + extractedText)
                    count +=1

        file.close()
        print("Extracted {0} notes from {1}".format(count, SelectedName))

csg_pywaapi.endUndoGroup("Extract Wwise notes to CSV")

print("Done")

##### Pause the script to display results ######
input('Press <ENTER> to continue')

csg_pywaapi.exit()