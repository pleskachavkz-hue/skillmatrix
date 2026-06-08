#!/bin/bash

cd /Users/apkz/Desktop/Skillmatrix

git add .

if ! git diff --cached --quiet; then
    git commit -m "autosync $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin main
fi
