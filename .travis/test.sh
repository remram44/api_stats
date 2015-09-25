#!/bin/sh

set -eux

case "$TEST_MODE"
in
    run_tests)
        python tests
        ;;
    coverage)
        coverage run --append --source=api_stats.py --branch tests/__main__.py
        ;;
    check_style)
        flake8 --ignore=E126 api_stats.py tests
        ;;
esac
