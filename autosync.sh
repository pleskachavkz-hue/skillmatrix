#!/bin/bash

LOGFILE="/Users/apkz/Desktop/Skillmatrix/autosync.log"

cd /Users/apkz/Desktop/Skillmatrix || exit 1

echo "========== $(date) ==========" >> "$LOGFILE"

git pull --rebase origin main >> "$LOGFILE" 2>&1

git add .

if ! git diff --cached --quiet; then
    COMMIT_MSG="autosync $(date '+%Y-%m-%d %H:%M:%S')"

    git commit -m "$COMMIT_MSG" >> "$LOGFILE" 2>&1
    git push origin main >> "$LOGFILE" 2>&1

    echo "Sync completed" >> "$LOGFILE"
else
    echo "No changes" >> "$LOGFILE"
fi
