import sys
import os

sys.path.append('..')

import csg_pywaapi
import csg_helpers.gui as gui
import csg_helpers.Files


'''
This script asks the user for a directory.
It recursively finds all .mp4 video files in the given directory
and creates a Started and Ended event in Wwise for each video found.
It demonstrates use of the gui and Files helper modules, as well as creating objects from custom arguments.

'''


############# Function definitions #########################################



def setupCreateArgs(parentID, otype="BlendContainer", oname="", conflict="merge"):
    createObjArgs = {

        "parent": parentID,
        "type": otype,
        "name": oname,
        "onNameConflict": conflict
    }
    return createObjArgs


def EventCreateArgs(parentID, fname, enterExit):
    createObjArgs = {

        "parent": parentID,
        "type": "Event",
        "name": fname+"_"+enterExit,
        "onNameConflict": "merge"
    }
    return createObjArgs


############## End of Function definitions ##############################################

#Connect to Wwise
result = csg_pywaapi.connect(8080)
if not result:
    exit()


csg_pywaapi.beginUndoGroup()
print("...")

currentWorkingDir = os.getcwd()
print("Current Working Directory = " + currentWorkingDir)


sourceDir = os.path.expanduser(gui.askUserForDirectory())
if (sourceDir != ""):
    videoFolderName = os.path.basename(sourceDir)
    print(videoFolderName)

    sourceFiles = csg_helpers.Files.setupSourceFileList(sourceDir, '*.mp4')

    videoNames = []
    for mp4 in sourceFiles:
        mp4name = str(mp4)
        mp4name = mp4name.replace(".mp4", "")
        videoNames.append(mp4name)
        print(mp4name)


    eventParent = "\\Events\\"
    args = setupCreateArgs(eventParent, "Folder", videoFolderName)
    csg_pywaapi.createWwiseObjectFromArgs(args)

    for mp4 in videoNames:
        args = EventCreateArgs(eventParent + videoFolderName + "\\", mp4, "Started")
        csg_pywaapi.createWwiseObjectFromArgs(args)
        args = EventCreateArgs(eventParent + videoFolderName + "\\", mp4, "Ended")
        csg_pywaapi.createWwiseObjectFromArgs(args)
else:
    print("No directory selected....exiting....")


csg_pywaapi.endUndoGroup("Create Map Events")





############### Exit  #############################
csg_pywaapi.saveWwiseProject()

print("......")
print("Script finished....exiting")
print("......")

# Exit
csg_pywaapi.exit()
