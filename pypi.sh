# commands to upload this package on pypi
rm -rf ./dist/ ./QuicKeepass.egg-info/
python3 setup.py sdist
twine upload --verbose --skip-existing dist/*
