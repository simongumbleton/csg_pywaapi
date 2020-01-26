import sys
import os
sys.path.append('..')

from waapi import WaapiClient
from pprint import pprint
import helpers.soundbank_helper as bankhelper




client = WaapiClient(url="ws://127.0.0.1:8095/waapi")

def connect():
    result = client.call("ak.wwise.core.getInfo")
    return result

def exit():
    client.disconnect()
############# Function definitions #########################################

### Project undo and save ######

def beginUndoGroup():
    client.call("ak.wwise.core.undo.begingroup")

def cancelUndoGroup():
    client.call("ak.wwise.core.undo.cancelgroup")

def endUndoGroup(undogroup):
    undoArgs = {"displayName": undogroup}
    client.call("ak.wwise.core.undo.endgroup", undoArgs)

def saveWwiseProject():
    client.call("ak.wwise.core.project.save")

def setupSubscription(subscription, target, returnArgs = ["id", "name", "path"]):
    client.subscribe(subscription, target, {"return": returnArgs})

def getProjectInfo():
    arguments = {
        "from": {"ofType": ["Project"]},
        "options": {
            "return": ["type","id", "name", "filePath","@DefaultLanguage"]
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get",arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def getLanguages():
    langlist=[]
    arguments = {
        "from": {"ofType": ["Language"]},
        "options": {
            "return": ["name"]
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        for lang in res.kwresults["return"]:
            if lang['name'] != 'SFX' and lang['name'] != 'External' and lang['name'] != 'Mixed':
                langlist.append(lang['name'])
        return langlist

###  Object creation and property setting ######


def createWwiseObject(parentID, otype="BlendContainer", oname="", conflict="merge"):

    createObjArgs = {

        "parent": parentID,
        "type": otype,
        "name": oname,
        "onNameConflict": conflict
    }
    try:
        res = client.call("ak.wwise.core.object.create", createObjArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def createWwiseObjectFromArgs(args = {}):
    try:
        res = client.call("ak.wwise.core.object.create", args)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def setProperty(object, property, value):
    setPropertyArgs = {

        "object": object,
        "property": property,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setproperty",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def importAudioFiles(args):
    try:
        res = client.call("ak.wwise.core.audio.import", args)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def deleteWwiseObject(object):
    args = {"object":object}
    try:
        client.call("ak.wwise.core.object.delete",args)
    except Exception as ex:
        print("call error: {}".format(ex))

###  Searching the project  ######

def getSelectedObjects(properties=["id","type", "name", "path"]):
    selectedObjectArgs = {
        "options": {
            "return": properties
        }
    }
    try:
        res = client.call("ak.wwise.ui.getselectedobjects",selectedObjectArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def GetDescendantObjectsOfType(object,type,properties=["id","type", "name", "path"]):
    #print("Get a list of the audio files currently in the project, under the selected object")
    arguments = {
        "from": {"id": [object]},
        "transform": [
            {"select": ["descendants"]},
            {"where":["type:isIn",[type]]}
        ],
        "options": {
            "return": properties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res


#####  Soundbanks #####
def generateSoundbanks(banklist = []):
    args = {
        "command": "GenerateSelectedSoundbanksAllPlatforms",
        "objects": [
            banklist
        ]
    }
    client.call("ak.wwise.ui.commands.execute", args)

def GetSoundbanks(fromType,fromValue):
    # Return all Soundbanks referencing any object of the Work Unit directly
    BankList =[]
    for transform in bankhelper.bankTransforms:
        arguments = {
            "from": {fromType: [fromValue]},
            "transform": transform,
            "options": {
                "return": ['id', 'name', 'type']
            }
        }
        try:
            res = client.call("ak.wwise.core.object.get", arguments)
        except Exception as ex:
            print("call error: {}".format(ex))
        else:
            # print (res.kwresults["return"])
            for bank in res.kwresults["return"]:
                if bank["name"] not in BankList:
                    BankList.append((bank["name"]))
    return BankList

############## End of Function definitions ##############################################




