#!/bin/bash
set -e

drone enable $1
drone set-params $1 $2
