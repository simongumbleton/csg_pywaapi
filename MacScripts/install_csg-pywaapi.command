#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd "${DIR}"
cd ..
cd csg_pywaapi
pip3 install -i https://test.pypi.org/simple/ csg-pywaapi
