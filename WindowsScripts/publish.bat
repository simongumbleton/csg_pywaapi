cd %~dp0
cd ..
cd csg_pywaapi
python -m pip install twine
python -m twine upload dist/*
