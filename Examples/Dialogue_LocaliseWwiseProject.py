import csg_pywaapi
import sys
import os
from pprint import pprint


def setupArgsForLoc(path, id, wavFile, language):
    importFilelist = []
    importFilelist.append(
        {
            "audioFile": wavFile,
            "objectPath": path,
            "objectType": "Sound"
        }
    )
    importArgs = {
        "importOperation": "useExisting",
        "default": {
            "importLanguage": language,
            "importLocation": id,
        },
        "imports": importFilelist,
        # "autoAddToSourceControl":False  #not yet supported
    }
    return importArgs

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

projectInfo = csg_pywaapi.getProjectInfo()
projectlanguages = csg_pywaapi.getLanguages()
projectlanguages.remove(projectInfo["@DefaultLanguage"])


## Do some opertation on each object that was passed in
for id in ids:
    print("This is where you do your operations on each object")

    
    audioFiles = csg_pywaapi.getDescendantObjectsOfType(id,"Sound",["sound:originalWavFilePath","@IsVoice"])
    voicefiles = []
    for file in audioFiles:
        if file["type"]=="Sound" and file["@IsVoice"]==True:
            name = str(file["name"])
            voicefiles.append(file)

    if len(voicefiles) == 0:
        print("List of Existing Wwise Voices is Empty...")
        print("Unable to localise into selected wwise object...")
        print("...Exiting...")
        break

    for voice in voicefiles:
        path = voice['path']
        id = voice['id']
        name = voice['name']
        if "sound:originalWavFilePath" in voice:
            originalWavpath = voice["sound:originalWavFilePath"].replace('\\', '/').replace("Y:", "~")
            originalWavpath = os.path.normpath(os.path.expanduser(originalWavpath))
            for language in projectlanguages:
                # (path, filename, fileList, language)
                languageWav = os.path.normpath(originalWavpath.replace(projectInfo["@DefaultLanguage"], language))
                args = setupArgsForLoc(path, id, str(languageWav), language)
                res = csg_pywaapi.importAudioFiles(args)
                print(languageWav)
        else:
            print("sound:originalWavFilePath NOT in file")


# Close the undo groupr
csg_pywaapi.endUndoGroup("MyUndoGroup")

##### Pause the script to display results ###### 
#input('Press <ENTER> to continue')

# Exit
csg_pywaapi.exit()