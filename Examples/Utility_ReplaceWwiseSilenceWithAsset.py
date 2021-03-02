import os
import sys

import csg_pywaapi
from pprint import pprint

'''
This Script will find all instances of the Wwise Silence source plugin, and replace them with a WAV asset.
It demonstrates finding objects by type, filtering based on properties, deleting and importing.
'''

### Wwise silence class id = 6619138 ###   2019.1.3 - differs from the documentation
### Debug\UtilitySignals_SilenceMono_01.wav  - file in originals to replace

#Connect to Wwise
result = csg_pywaapi.connect(8095)
if not result:
    exit()

#Get a path to the desired asset to use, an existing wav in Originals in this case
pathToWwiseFolder = csg_pywaapi.getPathToWwiseProjectFolder()
originalsPath = "/Originals/SFX/Debug/"
silenceWav = "UtilitySignals_SilenceMono_01.wav"
pathToSilenceWav = pathToWwiseFolder+originalsPath+silenceWav

if not os.path.exists(pathToSilenceWav):
    pprint("!!!!!!!!!!!!")
    pprint("Path to replacement wav file not valid. Exiting")
    csg_pywaapi.exit()
    exit()

pprint("................")
pprint("Replacing all instances of Wwise silence with..")
pprint(silenceWav)
pprint("")


#Get all the source plugins, returning extra properties such as classID
SourcePlugins = csg_pywaapi.getDescendantObjectsOfType("\\Actor-Mixer Hierarchy", "SourcePlugin", ["classId", "parent", "owner", "audioSource:language"], "path")
#filter the list to get just wwise silence using class ID
WwiseSilences = csg_pywaapi.filterWwiseObjects(SourcePlugins, "classId", "==", 6619138)

csg_pywaapi.beginUndoGroup()

#Loop through the list and delete the silences, and import the wav into the same place
count = 0
for silence in WwiseSilences:
    #pprint(silence)
    parentID = silence["parent"]["id"]
    language = silence["audioSource:language"]["name"]
    csg_pywaapi.deleteWwiseObject(silence["id"])
    args = csg_pywaapi.setupImportArgs(parentID, [pathToSilenceWav], "Debug", language)
    csg_pywaapi.importAudioFiles(args)
    count += 1

csg_pywaapi.endUndoGroup("CSG - Replace Wwise Silence")

pprint("")
pprint("Replaced "+str(count)+" instances of Wwise Silence")
pprint("")

##### Pause the script to display results ######
input('Press <ENTER> to continue')

csg_pywaapi.exit()