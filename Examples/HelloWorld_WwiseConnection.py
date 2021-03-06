import csg_pywaapi
from pprint import pprint

"""
This is a basic "Hello World" type example. 
Demonstrating basic connection on a given waapi port, and printing the result showing details of the wwise connection
"""


pprint("................")
pprint("Hello fellow sound warrior!")
pprint("Here is your current Wwise connection!")
pprint("................")

result = csg_pywaapi.connect(8080)
pprint(result)
if not result:
    exit()


##### Pause the script to display results ###### 
input('Press <ENTER> to continue')

csg_pywaapi.exit()