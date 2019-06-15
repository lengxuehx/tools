#!/bin/bash
#find  ./app/bower_components  -maxdepth 1 -mindepth 1 -type l  -exec git --git-dir={}/.git --work-tree=$PWD/{} pull +
find  ./app/bower_components  -maxdepth 1 -mindepth 1 -type l | xargs -P 8 -I '{}' git --git-dir='{}'/.git --work-tree=$PWD/'{}' pull
