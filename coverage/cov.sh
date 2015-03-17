#!/bin/bash

# Run this script from within the "tests" directory of the Django checkout.

coverage run --omit="*/pyshared/*,modeltests/*,regressiontests/*,*test_sqlite*,*runtests*,urls,*pkg_resources*" ./runtests.py --settings=test_sqlite
coverage report > report.txt

