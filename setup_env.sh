#!/bin/bash

dir=`dirname $BASH_SOURCE`
export PYTHONPATH=`readlink -f $dir`:$PYTHONPATH
