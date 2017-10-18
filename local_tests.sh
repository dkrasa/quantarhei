#! /bin/sh

#
# This script runs a test of the local source code of Quantarhei package.
# To test an installed version of Quantarhei run
#
#   > paver
#
# 
#
#
#


#
# Make sure now quantarhei is installed
#
pip uninstall quantarhei
#pip uninstall aceto

# point to the local version of the package
export PYTHONPATH=`pwd`

#
# Run tests
#
nosetests -vs tests/unit/core/test_saveable.py
nosetests -vs tests/unit/core/test_dfunction.py

#paver


