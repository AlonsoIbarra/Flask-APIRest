#!/bin/sh

ERRORS_FOUND=`flake8 app | wc -l | tr -d ' '`;
MAX_FLAKE8_ERRORS_ALLOWED=10

RED='\033[91m';  # Red color
YELLOW='\033[93m';  # Yellow color
NC='\033[0m';  # No Color

if [ $ERRORS_FOUND -gt $MAX_FLAKE8_ERRORS_ALLOWED ]
then
    MESSAGE="${RED}
        ERROR: Flake8 found $ERRORS_FOUND style errors,
        are more than the $MAX_FLAKE8_ERRORS_ALLOWED allowed.${NC}";
    EXIT_CODE=1;
else
    MESSAGE="${YELLOW}
        WARNING: Flake8 found $ERRORS_FOUND style errors,
        is in the allowed range.${NC}";
    EXIT_CODE=0;
fi

echo $MESSAGE;
exit $EXIT_CODE;
