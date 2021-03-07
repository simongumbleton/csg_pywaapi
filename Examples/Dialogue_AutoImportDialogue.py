import csg_pywaapi
from csg_helpers import gui
from csg_helpers import Files
import sys
import os
from pprint import pprint

"""
This script imports audio files as voice in the default language and creates play events.
Given a directory (or multiple dirs passed via sys.argv) we find all the wav files under that root.
For each file we find, create some paths based on the folder structure for the actor mixer and event hierarchies.
Then import the wav file under the generated path and create a Play event for it.

This script demonstrates importing audio files, creating wwise objects from string paths, use of the Files helper
"""

#shorthands for object types for path creation
WU = "<WorkUnit>"
AM = "<ActorMixer>"
FD = "<Folder>"

#Funtions to generate a wwise object path from a relative directory path
def getObjectImportPath(relDir):
    dirSteps = str.split(relDir, os.sep)
    objectPath = WU + dirSteps[0] + "\\"
    for dir in dirSteps:
        if dir == '':
            continue
        objectPath += AM + dir + "\\"
    return  objectPath

def getEventImportPath(relDir):
    dirSteps = str.split(relDir, os.sep)
    objectPath = WU + dirSteps[0] + "\\"
    for dir in dirSteps:
        if dir == '':
            continue
        objectPath += FD + dir + "\\"
    return  objectPath

#Pause if errors to display log
def handleError():
    print("Error! Check log for details")
    ##### Pause the script to display results ######
    input('Press <ENTER> to continue')
    csg_pywaapi.exit()
    exit()


# Connect to Wwise
result = csg_pywaapi.connect(8080)
if not result:
    exit()

projectInfo = csg_pywaapi.getProjectInfo()
if not projectInfo:
    print("Could not get project info, is wwise project open?")
    csg_pywaapi.exit()
    exit()
#Get the default language and path to project
defaultLanguage = projectInfo["@DefaultLanguage"]
pathToWwiseDir = csg_pywaapi.getPathToWwiseProjectFolder()

# Setup an undo group
csg_pywaapi.beginUndoGroup()

# If run from cmd/bat/wwise then a list of directories can be passed in
dirs = []
if (len(sys.argv) > 1):
    sysargs = set(sys.argv[1:])
    for arg in sysargs:
        dirs.append(arg)

# if no args are given, then ask the user for a directory
if not dirs:
    res = gui.askUserForDirectory()
    if not res:
        print("No directly selected..Exiting")
        csg_pywaapi.exit()
        exit()
    dirs.append(res)


## Do some opertation on each object that was passed in
for dir in dirs:
    directory = os.path.abspath(dir)
    filesToImport = Files.setupSourceFileList(directory)
    dirName = os.path.basename(directory)
    print(filesToImport)

    importFilelist = []
    for audiofile in filesToImport:
        foo = audiofile.rsplit('.')  # remove extension from filename
        audiofilepath = foo[0]
        audiofilename = os.path.basename(audiofilepath)
        relativepath = os.path.relpath(audiofilepath, directory)
        relativeDir = os.path.dirname(relativepath)
        if relativeDir == '': #If the files were in the root then relative dir is empty, so use the root dir
            relativeDir = dirName

        AMpath = getObjectImportPath(relativeDir)
        AMobj = csg_pywaapi.createStructureFromPath(AMpath,"\\Actor-Mixer Hierarchy")
        if not AMobj:
            print("Failed to create object: {0}".format(AMpath))
            handleError()
        AMobj = csg_pywaapi.getObjectProperties(AMobj["id"],["path"])
        Evpath = getEventImportPath(relativeDir)
        EvObj = csg_pywaapi.createStructureFromPath(Evpath,"\\Events")
        if not EvObj:
            print("Failed to create object: {0}".format(Evpath))
            handleError()
        EvObj = csg_pywaapi.getObjectProperties(EvObj["id"], ["path"])

        importFilelist.append(
            {
                "audioFile": audiofile,
                "objectPath": AMobj["path"] +"\\" + "<Sound Voice>" + audiofilename,
                "originalsSubFolder": relativeDir,
                "event": EvObj["path"] +"\\" + audiofilename + "@Play"
            }
        )

    importArgs = {
        "importOperation": "useExisting",
        "autoAddToSourceControl": True,
        "default": {
            "importLanguage": defaultLanguage,
        },
        "imports": importFilelist
    }
    res = csg_pywaapi.importAudioFiles(importArgs)

csg_pywaapi.saveWwiseProject()

# Close the undo groupr
try:
    csg_pywaapi.endUndoGroup("Auto Import Dialogue")
except Exception as ex:
    print("close undo group error: {}".format(ex))
    csg_pywaapi.cancelUndoGroup()

##### Pause the script to display results ######
# input('Press <ENTER> to continue')

# Exit
csg_pywaapi.exit()