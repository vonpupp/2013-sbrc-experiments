#!/bin/bash

cat $1 | sed "s/\--.*$//g" | sed "s/\-//g" > $1.best
cat $1 | sed "s/\-.*\--//g" > $1.media

