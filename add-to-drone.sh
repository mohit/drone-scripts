#!/bin/bash
set -e

cd $1
REPO=$(git remote -v | head -n1 | cut -f2 | cut -f1 -d' ' | cut -f2 -d'@' | sed 's/.git//' | sed 's/:/\//')
echo $REPO $2
#drone enable $REPO
#drone set-params $REPO $2
