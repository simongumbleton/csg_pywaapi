#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
cd ..
cd csg_pywaapi
python3 setup.py sdist bdist_wheel
