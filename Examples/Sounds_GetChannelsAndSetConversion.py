import sys
import os
import csg_pywaapi
sys.path.append('..')

from csg_helpers.AudioFileReader import GetChannels

'''
This script sets a conversion shareset based on the number of channels of an audio source.
For each ID passed in sys.argv, it gets all audio sources under the given ID
and using the AudioFileReader helper, gets the channels of the wav file.
It sets the override conversion setting to true, and sets the surround conversion shareset if 5 or more channels
otherwise sets the default.
This demonstrates using the AudioFileReader helper, setting properties and references.
It also demonstrates how to operate on multiple objects passed in via arguments
(see Wwise command add-ons for details -https://www.audiokinetic.com/library/edge/?source=SDK&id=defining_custom_commands.html)
'''

#Path in wwise to the conversion sharesets to use
DefaultConversionShareset = "\\Conversion Settings\\Default Work Unit\\Default"
SurroundConversionShareset = "\\Conversion Settings\\Default Work Unit\\Surround"

def cleanfilePathFromWwise(path):
    cleanMacpath = path.replace("Y:","~").replace('\\', '/')
    return os.path.abspath(os.path.expanduser(cleanMacpath))

###########  Do Some Cool stuff here ##############
#Connect to Wwise
result = csg_pywaapi.connect()
if not result:
    exit()

print("...")
csg_pywaapi.beginUndoGroup()

# When called via wwise custom commands, the IDs of selected objects can be passed in as sys args
# Allowing scripts to operate with multi-selection in the wwise tool
ids = []
if (len(sys.argv) > 1):
    sysargs = set(sys.argv[1:])
    for arg in sysargs:
        ids.append(arg)

# If we didn't have any IDs passed in, we can try and get the currently selected wwise objects to act on
if not ids:
    # no arg given, use selected object instead
    res = csg_pywaapi.getSelectedObjects()
    #print(res)
    for obj in res:
        ids.append(obj["id"])

fixedSounds = []

# For each selected parent object, get all the audio file sources and check the number of channels in the wav.
# for any sounds with 5 or more channels, use the Surround conversion, otherwise use the default
for id in ids:
    wwiseSounds = csg_pywaapi.getDescendantObjectsOfType(id, "AudioFileSource", ["sound:originalWavFilePath", "parent"])
    for sound in wwiseSounds:
        wav = sound["sound:originalWavFilePath"]
        wavpath = cleanfilePathFromWwise(wav)
        wavChannels = GetChannels(wavpath)
        name = sound["name"]

        csg_pywaapi.setProperty(sound["parent"]["id"], "OverrideConversion", True)

        if wavChannels >= 5:
            csg_pywaapi.setReference(sound["parent"]["id"], "Conversion", SurroundConversionShareset)
        else:
            csg_pywaapi.setReference(sound["parent"]["id"], "Conversion", DefaultConversionShareset)
        fixedSounds.append(sound["name"])


print("fixed "+str(len(fixedSounds))+" conversion sharesets")

csg_pywaapi.endUndoGroup("Set Conversion Settings")


############### Exit  #############################
csg_pywaapi.saveWwiseProject()
print("......")
print("Script finished....exiting")
print("......")
##### Pause the script to display results ###### 
input('Press <ENTER> to continue')
csg_pywaapi.exit()

