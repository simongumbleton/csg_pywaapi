from waapi import WaapiClient
from pprint import pprint

client = WaapiClient(url="ws://127.0.0.1:8095/waapi")

def connect():
    result = client.call("ak.wwise.core.getInfo")
    return result


############# Function definitions #########################################
def exit():
    client.disconnect()

def beginUndoGroup():
    client.call("ak.wwise.core.undo.begingroup")

def cancelUndoGroup():
    client.call("ak.wwise.core.undo.cancelgroup")

def endUndoGroup():
    undoArgs = {"displayName": "My Waapi Script"}
    client.call("ak.wwise.core.undo.begingroup", undoArgs)

def saveWwiseProject():
    client.call("ak.wwise.core.project.save")

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


def createWwiseObject(args):
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


############## End of Function definitions ##############################################




