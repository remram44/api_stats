#!/bin/sh

set -eux

case "$TEST_MODE"
in
    run_tests|coverage)
        if [ $TRAVIS_PYTHON_VERSION = "2.6" ]; then pip install unittest2; fi
        if [ TEST_MODE = "coverage" ]; then pip install coverage codecov; fi
        pip install "$PWD"
        ;;
    check_style)
        pip install flake8
        ;;
esac
