import os
import re
from collections import defaultdict

INPUT_FILE = "bootcamp.txt"
OUTPUT_DIR = "DevSecOpsBootcamp"

# Updated weeks to match the revised syllabus
REVISED_WEEKS = [
    "Week05", "Week06", "Week07", "Week08",
    "Week09", "Week10", "Week11", "Week12",
    "Week13", "Week14", "Week15", "Week16",
    "Week17", "Week18", "Week19", "Week19.5", "Week20"
]

EXPECTED_FILES = {"Overview.md", "GuidedLab.md", "ChallengeLab.md", "Security.md", "Reflection.md"}

# Regex to find each 📁 WeekXX/Filename.md
FOLDER_PATTERN = re.compile(r"📁\s*(Week\d{2}(?:\.5)?)\/([A-Za-z]+\.md)")

def parse_weeks(transcript):
    matches = list(FOLDER_PATTERN.finditer(transcript))
    weeks = defaultdict(dict)

    for i, match in enumerate(matches):
        week = match.group(1)
        filename = match.group(2)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(transcript)
        content = transcript[start:end].strip()

        if week in REVISED_WEEKS and filename in EXPECTED_FILES:
            # Always overwrite with the latest occurrence (latest is most accurate)
            weeks[week][filename] = content

    return weeks

def write_weeks_to_disk(weeks):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for week in REVISED_WEEKS:
        week_path = os.path.join(OUTPUT_DIR, week)
        os.makedirs(week_path, exist_ok=True)
        files = weeks.get(week, {})

        for fname in EXPECTED_FILES:
            content = files.get(fname, f"# {fname}\n\n*Section missing or skipped in transcript.*")
            with open(os.path.join(week_path, fname), "w", encoding="utf-8") as f:
                f.write(content)

    print(f"✅ Final DevSecOps bootcamp exported to '{OUTPUT_DIR}' aligned with corrected syllabus.")

# === MAIN ===
if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Missing file: {INPUT_FILE}")
    else:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            transcript = f.read()

        parsed = parse_weeks(transcript)
        write_weeks_to_disk(parsed)
