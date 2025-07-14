#!/bin/bash
# scaffold-week.sh
# Usage: ./scaffold-week.sh 03

WEEK=$1

if [ -z "$WEEK" ]; then
  echo "❌ Usage: ./scaffold-week.sh <week-number-or-name>"
  exit 1
fi

FOLDER="modules/week-$WEEK"

mkdir -p "$FOLDER"

echo "# 🌍 Week $WEEK: Real-World Scenario" > $FOLDER/0_OVERVIEW.md
echo "# ✅ Guided Lab" > $FOLDER/1_GUIDED_LAB.md
echo "# 🚀 Challenge Lab" > $FOLDER/2_CHALLENGE_LAB.md
echo "# 🧘 Reflection" > $FOLDER/3_REFLECTION.md
echo "# 🔒 Security Notes" > $FOLDER/4_SECURITY.md

echo "✅ Scaffolded: $FOLDER with starter files!"
