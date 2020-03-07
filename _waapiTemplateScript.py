import sys
import os

import asyncio
from autobahn.asyncio.component import run
import autobahn.asyncio.wamp

sys.path.append('..')


from includes.ak_autobahn import AkComponent
from includes.MyWwiseComponent import myWaapiComponent
from includes.waapi import WAAPI_URI



class MyComponent(AkComponent):


    def onJoin(self, details):

############# Function definitions #########################################
        def exit():
            yield from self.leave()

        def beginUndoGroup():
            yield from self.call(WAAPI_URI.ak_wwise_core_undo_begingroup)

        def cancelUndoGroup():
            yield from self.call(WAAPI_URI.ak_wwise_core_undo_cancelgroup)

        def endUndoGroup():
            undoArgs = {"displayName": "My Waapi Script"}
            yield from self.call(WAAPI_URI.ak_wwise_core_undo_endgroup, {}, **undoArgs)

        def saveWwiseProject():
            yield from self.call(WAAPI_URI.ak_wwise_core_project_save)

        def getAudioFilesInWwise(IDorPath):
            #print("Get a list of the audio files currently in the project, under the selected object")
            arguments = {
                "from": {"path": [IDorPath]},
                "transform": [
                    {"select": ["descendants"]},
                    {"where":["type:isIn",["Sound"]]}
                ],
                "options": {
                    "return": ["id","type", "name", "path", "sound:originalWavFilePath", "isPlayable","audioSource:playbackDuration"]
                }
            }
            try:
                res = yield from self.call(WAAPI_URI.ak_wwise_core_object_get, **arguments)
            except Exception as ex:
                print("call error: {}".format(ex))
                return 0
            else:
                return res.kwresults["return"]

############## End of Function definitions ##############################################



############### Main Script logic flow ####################################################
        ## First try to connect to wwise to get Wwise info
        try:
            res = yield from self.call(WAAPI_URI.ak_wwise_core_getinfo)  # RPC call without arguments
        except Exception as ex:
            print("call error: {}".format(ex))
        else:
            # Call was successful, displaying information from the payload.
            print("Hello {} {}".format(res.kwresults['displayName'], res.kwresults['version']['displayName']))



    ###########  Do Some Cool stuff here ##############

        beginUndoGroup()

        # Get all the audio files from a Wwise path
        
        ###### List all audio files in the project ####
        
        #listOfAudioFiles = yield from getAudioFilesInWwise("\\Actor-Mixer Hierarchy\\")
        #print(listOfAudioFiles)
        
        print("........  Hello fellow sound warrior! ........")
        

        endUndoGroup()


    ############### Exit  #############################
        saveWwiseProject()
        
        ##### Pause the script to display results ###### 
        input('Press <ENTER> to continue')
        
        
        #exit()
        yield from self.leave()
        #asyncio.get_event_loop().stop()


    def onDisconnect(self):
        print("The client was disconnected.")



if __name__ == '__main__':
    newComponent = myWaapiComponent
    newComponent.session_factory = MyComponent

    try:
        # runner.run(MyComponent)
        run([newComponent])
    except Exception as e:
        print(type(e).__name__ + ": Is Wwise running and Wwise Authoring API enabled?")
