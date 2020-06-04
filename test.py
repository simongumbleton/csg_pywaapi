#import csg_pywaapi.csg_pywaapi as csg_pywaapi
#import csg_helpers as p
import csg_pywaapi


print(dir(csg_pywaapi))

res = csg_pywaapi.connect()
#res = p.connect()
print(res)

csg_pywaapi.exit()

exit()