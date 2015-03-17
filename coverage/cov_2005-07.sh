#!/bin/bash

# Run this script from within the "tests" directory of the Django checkout.

coverage run --omit="*/pyshared/*,modeltests/*,regressiontests/*,*test_sqlite*,*runtests*,urls,*pkg_resources*" cache_tests.py 
coverage run -a --omit="*/pyshared/*,modeltests/*,regressiontests/*,*test_sqlite*,*runtests*,urls,*pkg_resources*" template_inheritance
coverage run -a --omit="*/pyshared/*,modeltests/*,regressiontests/*,*test_sqlite*,*runtests*,urls,*pkg_resources*" template_tests
coverage report > report.txt

