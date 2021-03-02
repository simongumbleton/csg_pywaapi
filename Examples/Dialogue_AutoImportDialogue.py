import csg_pywaapi
from csg_helpers import gui
from csg_helpers import Files
import sys
import os
from pprint import pprint


SectionName = "NewSection"
SubsectionName = "NewSubSection"
CharacterName = "NewCharacter"

WU = "<WorkUnit>"
AM = "<ActorMixer>"
FD = "<Folder>"

ActorMixerStructure = (
        WU + SectionName + "\\"
        + AM + SectionName + "\\"
        + AM + SubsectionName + "\\"
        + AM + CharacterName + "\\"
)

EventStructure = (
        WU + SectionName + "\\"
        + FD + SubsectionName + "\\"
)

OriginalsStructure = (
        SectionName + os.sep
        + SubsectionName + os.sep
        + CharacterName + os.sep
)

def LAMS_GetDataForVOLine(VOline):
    lineData = {}
    lineData["line"] = VOline
    lineData["filepath"] = "" #GetfilepathFromLAMS(VOline)
    lineData["section"] = "MySection" #GetSectionFromLAMS(VOline)
    lineData["subsection"] = "MySubsection" #GetSubsectionFromLAMS(VOline)
    lineData["character"] = "MyCharacter" #GetCharacterFromLAMS(VOline)



def getObjectImportPath(relDir,filename):
    dirSteps = str.split(relDir, os.sep)
    #objectPath = "\\Actor-Mixer Hierarchy\\"
    objectPath = WU + dirSteps[0] + "\\"
    for dir in dirSteps:
        objectPath += AM + dir + "\\"
    #objectPath += "<Sound Voice>" + filename
    return  objectPath

def getEventImportPath(relDir,filename):
    dirSteps = str.split(relDir, os.sep)
    #objectPath = "\\Events\\"
    objectPath = WU + dirSteps[0] + "\\"
    #objectPath = ""
    for dir in dirSteps[1:]:
        objectPath += FD + dir + "\\"
    #objectPath += filename + "@Play"
    return  objectPath


# Connect to Wwise
result = csg_pywaapi.connect()
if not result:
    exit()



projectInfo = csg_pywaapi.getProjectInfo()
if not projectInfo:
    print("Could not get project info, is wwise project open?")
    csg_pywaapi.exit()
    exit()

defaultLanguage = projectInfo["@DefaultLanguage"]
pathToWwiseDir = csg_pywaapi.getPathToWwiseProjectFolder()
projectlanguages = csg_pywaapi.getLanguages()
projectlanguages.remove(projectInfo["@DefaultLanguage"])
res = csg_pywaapi.getSelectedObjects()


# Setup an undo group
csg_pywaapi.beginUndoGroup()

# If run from cmd/bat/wwise then usually IDs will be passed into the args
dirs = []
if (len(sys.argv) > 1):
    sysargs = set(sys.argv[1:])
    for arg in sysargs:
        dirs.append(arg)

# if no args are given, then get the currently selected objects instead
if not dirs:
    res = gui.askUserForDirectory()
    dirs.append(res)



## Do some opertation on each object that was passed in
for dir in dirs:
    directory = os.path.abspath(dir)
    filesToImport = Files.setupSourceFileList(directory)
    print(filesToImport)

    importFilelist = []
    for audiofile in filesToImport:
        foo = audiofile.rsplit('.')  # remove extension from filename
        audiofilepath = foo[0]
        audiofilename = os.path.basename(audiofilepath)
        relativepath = os.path.relpath(audiofilepath, directory)
        relativeDir = os.path.dirname(relativepath)

        AMpath = getObjectImportPath(relativeDir,audiofilename)
        AMobj = csg_pywaapi.createStructureFromPath(AMpath,"\\Actor-Mixer Hierarchy")
        AMobj = csg_pywaapi.getObjectProperties(AMobj["id"],["path"])
        Evpath = getEventImportPath(relativeDir,audiofilename)
        EvObj = csg_pywaapi.createStructureFromPath(Evpath,"\\Events")
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

    print(res)




# Close the undo groupr
csg_pywaapi.endUndoGroup("Auto Import Dialogue")

##### Pause the script to display results ######
# input('Press <ENTER> to continue')

# Exit
csg_pywaapi.exit()