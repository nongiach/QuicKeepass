# commands to upload this package on pypi
python3 setup.py sdist
twine upload dist/*
