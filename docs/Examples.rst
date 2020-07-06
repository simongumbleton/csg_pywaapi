.. csg_pywaapi documentation master file, created by
   sphinx-quickstart on Wed Jun 17 18:43:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Examples
=======================================

Lets look at a few short examples of getting started using the module


***************
Getting sounds from the actor-mixer hierarchy
***************
This example demonstrates getting a list of sounds in the actor mixer hierarchy, and if the included flag is set, print the name of the sound.

.. code-block:: python

   import csg_pywaapi
   
   csg_pywaapi.connect()
   Sounds = csg_pywaapi.getDescendantObjectsOfType("\\Actor-Mixer Hierarchy", "Sound", ["@Inclusion"], "path")
   for sound in Sounds:
    if sound["@Inclusion"] == True:
       print(sound["name"])


***************
Setting properties
***************
This example demonstrates setting the volume property on the currently selected objects

.. code-block:: python

   import csg_pywaapi
   
   csg_pywaapi.connect()
   Selection = csg_pywaapi.getSelectedObjects()
   for object in Selection:
      csg_pywaapi.setProperty(object["id"],"@Volume", -6)


***************
Basic Importing of Audio
***************
This example demonstrates importing a list of new audio files into wwise under the first selected object

.. code-block:: python

   import csg_pywaapi


   ListOfAudioFiles = [] #Imagine a list of .wav files go here :)
   csg_pywaapi.connect()
   Selection = csg_pywaapi.getSelectedObjects()
   Parent = Selection[0]
   args = csg_pywaapi.setupImportArgs(Parent["id"],ListOfAudioFiles,"MyNewSounds","SFX")
   result = csg_pywaapi.importAudioFiles(args)
   print(result)
   


