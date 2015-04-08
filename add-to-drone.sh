#!/bin/bash
set -e

REPO=$(git remote -v | head -n1 | cut -f2 | cut -f1 -d' ' | cut -f2 -d'@' | sed 's/.git//' | sed 's/:/\//')
drone enable $REPO
drone set-params $REPO $PARAMS_FILE
