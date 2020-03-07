import sys
import os
sys.path.append('..')

from waapi import WaapiClient
from pprint import pprint
import helpers.soundbank_helper as bankhelper
import operator




client = WaapiClient(url="ws://127.0.0.1:8095/waapi")

def connect():
    result = client.call("ak.wwise.core.getInfo")
    return result

def exit():
    client.disconnect()
############# Function definitions #########################################

### Project undo and save ######

def beginUndoGroup():
    client.call("ak.wwise.core.undo.beginGroup")

def cancelUndoGroup():
    client.call("ak.wwise.core.undo.cancelGroup")

def endUndoGroup(undogroup):
    undoArgs = {"displayName": undogroup}
    client.call("ak.wwise.core.undo.endGroup", undoArgs)

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
        return res["return"][0]

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

def getPathToWwiseProjectFolder():
    projectInfo = getProjectInfo()
    WwiseProjectPath = projectInfo["filePath"]
    WwiseProjectPath = WwiseProjectPath.replace("Y:", "~").replace('\\', '/')
    pathToWwiseFolder = os.path.expanduser(os.path.dirname(WwiseProjectPath))
    return pathToWwiseFolder

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
        res = client.call("ak.wwise.core.object.setProperty",setPropertyArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def setReference(object, reference, value):
    setArgs = {

        "object": object,
        "reference": reference,
        "value": value
    }
    try:
        res = client.call("ak.wwise.core.object.setReference",setArgs)
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

def setupImportArgs(parentID, fileList,originalsPath,language="SFX"):
    #print ("Args for audio importing")
    ParentID = str(parentID)
    importFilelist = []
    for audiofile in fileList:
        foo = audiofile.rsplit('.') #remove extension from filename
        audiofilename = foo[0]
        importFilelist.append(
            {
                "audioFile": audiofile,
                "objectPath": "<Sound SFX>"+os.path.basename(audiofilename)
            }
        )

    importArgs = {
        "importOperation": "useExisting",
        "autoAddToSourceControl": True,
        "default": {
            "importLanguage": language,
            "importLocation": ParentID,
            "originalsSubFolder": originalsPath
            },
        "imports": importFilelist
        }
    return importArgs


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
        res = client.call("ak.wwise.ui.getSelectedObjects",selectedObjectArgs)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        if res != None:
            return res["objects"]
        else:
            return []

def GetDescendantObjectsOfType(fromObject,ofType,returnProperties,tfrom="id",select="descendants"):
    #print("Get a list of the audio files currently in the project, under the selected object")
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [
            {"select": [select]},
            {"where":["type:isIn",[ofType]]}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        if res != None:
            return res["return"]
        else:
            return []

def GetObjectProperties(fromObject,returnProperties,tfrom="id"):
    #print("Get a list of the audio files currently in the project, under the selected object")
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {tfrom: [fromObject]},
        "transform": [],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        if res != None:
            return res["return"][0]
        else:
            return []

def GetAllObjectsOfType(ofType,returnProperties):
    #print("Get a list of the audio files currently in the project, under the selected object")
    baseProperties = ["id","type", "name", "path"]
    arguments = {
        "from": {"ofType": [ofType]},
        "transform": [
            #{"select": "parent"}
        ],
        "options": {
            "return": baseProperties+returnProperties
        }
    }
    try:
        res = client.call("ak.wwise.core.object.get", arguments)
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        if res != None:
            return res["return"]
        else:
            return []


def getListOfTypes():
    try:
        res = client.call("ak.wwise.core.object.getTypes")
    except Exception as ex:
        print("call error: {}".format(ex))
    else:
        return res

def filterWwiseObjects(objects,property,operation, value):
    results = []
    op = getOperator(operation)
    for obj in objects:
        if op(obj[property],value):
            results.append(obj)
    return results

def getOperator(string):
    if string == "==":
        return operator.eq
    elif string == ">":
        return operator.lt
    elif string == ">=":
        return operator.le
    elif string == "<":
        return operator.gt
    elif string == "<=":
        return operator.ge
    elif string == "!=":
        return operator.ne


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


def executeCommand(command,objects = []):
    args = {
        "command": command,
        "objects": [
            objects
        ]
    }
    res = client.call("ak.wwise.ui.commands.execute", args)
    return res

def automationMode(enabled):
    args = {
        "enable": enabled
    }
    res = client.call("ak.wwise.debug.enableAutomationMode", args)
    return res

############## End of Function definitions ##############################################




