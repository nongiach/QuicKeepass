# commands to upload this package on pypi
set -e
sudo rm -rf build ./dist/ ./QuicKeepass.egg-info/
python3 setup.py sdist
twine upload --verbose --skip-existing dist/*
