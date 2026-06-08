#!/bin/bash

LOGFILE="/Users/apkz/Desktop/Skillmatrix/autosync.log"

echo "========== $(date) ==========" >> "$LOGFILE"

cd /Users/apkz/Desktop/Skillmatrix || {
    echo "ERROR: cannot enter project directory" >> "$LOGFILE"
    exit 1
}

echo "Pulling latest changes..." >> "$LOGFILE"
git pull --rebase origin main >> "$LOGFILE" 2>&1

git add .

if ! git diff --cached --quiet; then
    COMMIT_MSG="autosync $(date '+%Y-%m-%d %H:%M:%S')"

    echo "Changes detected" >> "$LOGFILE"
    echo "Commit: $COMMIT_MSG" >> "$LOGFILE"

    git commit -m "$COMMIT_MSG" >> "$LOGFILE" 2>&1

    echo "Pushing to GitHub..." >> "$LOGFILE"
    git push origin main >> "$LOGFILE" 2>&1

    echo "Sync completed" >> "$LOGFILE"
else
    echo "No changes" >> "$LOGFILE"
fi

echo "" >> "$LOGFILE"
