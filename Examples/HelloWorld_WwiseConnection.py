import csg_pywaapi
from pprint import pprint

pprint("................")
pprint("Hello fellow sound warrior!")
pprint("Here is your current Wwise connection!")
pprint("................")

result = csg_pywaapi.connect()
pprint(result)
if not result:
    exit()


##### Pause the script to display results ###### 
input('Press <ENTER> to continue')

csg_pywaapi.exit()