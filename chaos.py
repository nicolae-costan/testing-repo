
import random
import subprocess
import os
from pathlib import Path

# CONFIGURATION
REPO = "https://github.com/nicolae-costan/testing-repo.git"
TOTAL_COMMITS = 100
TOTAL_PRS = 20

commit_messages = [
    "final fix",
    "final fix v2",
    "final fix v3 REALLY FINAL",
    "hope this works",
    "please work",
    "fixed the fix",
    "undoing what I just did",
    "this should fix it",
    "probably fixed",
    "idk why this works",
    "temporary solution (permanent)",
    "don't touch this",
    "works on my machine",
    "added more console logs",
    "removed some console logs",
    "what is happening",
    "I hate CSS",
    "fixed by accident",
    "revert the revert",
    "revert the revert of the revert",
    "ship it and pray",
    "one last attempt",
    "this is not my fault",
    "trust me bro",
    "fixed maybe",
    "please stop breaking",
    "code is code",
    "we don't talk about this",
    "hotfix but cold",
    "I need sleep"
]

pr_titles = [
    "Fix everything (hopefully)",
    "Please approve I am tired",
    "Another attempt at being a developer",
    "This PR fixes the previous PR",
    "The great CSS incident",
    "I have no idea what I'm doing",
    "Final final final fix",
    "Production is probably fine",
    "Introducing 3 new bugs to fix 1",
    "Works locally, good luck",
    "Please don't review too closely",
    "The code is now slightly less bad",
    "A questionable improvement",
    "Delete this if it breaks",
    "Fixes literally nothing (maybe)",
    "My debugger is crying",
    "Refactor until it works",
    "I swear this is the last one",
    "We don't talk about this implementation",
    "One more fix, I promise"
]

pr_bodies = [
    "What:\n- Changed some stuff\n- Broke something probably\n\nWhy:\n- Don't ask.",
    "Tested everything.\n\nBy everything I mean one button.",
    "I don't know why this works.\nI am afraid to investigate.",
    "Please merge. I have been staring at this for 6 hours.",
    "This seemed like a good idea at 2 AM.",
    "Fixes the bug I introduced while fixing another bug.",
    "QA status: vibes-based testing.",
    "If it breaks, it was working yesterday."
]

def run(command):
    subprocess.run(command, check=True)

# Create local repository
Path("chaos-repo").mkdir(exist_ok=True)
os.chdir("chaos-repo")

run(["git", "init"])
run(["git", "branch", "-M", "main"])

run(["git", "config", "user.name", "Totally Legit Developer"])
run(["git", "config", "user.email", "YOUR_GITHUB_EMAIL"])

# Initial commit
Path("README.md").write_text("# The Chaos Project\n\nPlease don't inspect this repository.\n")
run(["git", "add", "."])
run(["git", "commit", "-m", "initial commit (mistake)"])

# Generate commits
for i in range(TOTAL_COMMITS):
    Path("chaos.txt").write_text(
        f"Attempt #{i + 1}\n"
        f"Status: probably broken\n"
        f"Confidence: {random.randint(0, 100)}%\n"
    )

    run(["git", "add", "."])
    run(["git", "commit", "-m", random.choice(commit_messages)])

# Connect and push
subprocess.run(
    ["git", "pull", "origin", "main", "--rebase"],
    check=True
)

run(["git", "push", "-u", "origin", "main"])

# Generate PRs
for i in range(TOTAL_PRS):
    branch = f"fix/the-problem-{i + 1}"

    run(["git", "checkout", "main"])
    run(["git", "checkout", "-b", branch])

    Path("chaos.txt").write_text(
        f"Attempt #{i + 1}\n"
        "We fixed it. Probably.\n"
    )

    run(["git", "add", "."])
    run([
        "git", "commit", "-m",
        random.choice(commit_messages)
    ])

    run(["git", "push", "-u", "origin", branch])

    subprocess.run([
        "gh", "pr", "create",
        "--title", random.choice(pr_titles),
        "--body", random.choice(pr_bodies),
        "--base", "main",
        "--head", branch
    ], check=True)

print("\nCHAOS SUCCESSFULLY DEPLOYED.")
