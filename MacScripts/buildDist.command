#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
cd ..
cd csg_pywaapi
echo ".......Clean any old builds........"
 /bin/rm -r build
 /bin/rm -r csg_pywaapi.egg-info
 /bin/rm -r dist
echo "......Call setup to create the latest distribution......"
python3 setup.py sdist bdist_wheel
