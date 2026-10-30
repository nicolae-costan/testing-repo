
import random
import subprocess
import os
from pathlib import Path

# =====================================
# CONFIGURATION
# =====================================

REPO = "https://github.com/nicolae-costan/testing-repo.git"
GITHUB_EMAIL = "costan.nicolae112@gmail.com"

TOTAL_COMMITS = 100
TOTAL_PRS = 20

# Commit into the repo this script lives in, not a nested one
REPO_DIR = Path(__file__).resolve().parent

# =====================================
# FUNNY COMMIT MESSAGES
# =====================================



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
    "I need sleep",
    "feat: introduce another bug",
    "refactor: move the mess",
    "fix: probably not broken anymore",
    "chore: pretend to be productive",
    "fix: CSS exorcism",
    "fix: works if you don't look",
]

# =====================================
# FUNNY PR TITLES
# =====================================

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
    "One more fix, I promise",
]

# =====================================
# FUNNY PR DESCRIPTIONS
# =====================================

pr_bodies = [
    "What:\n- Changed some stuff\n- Broke something probably\n\nWhy:\n- Don't ask.",
    "Tested everything.\n\nBy everything I mean one button.",
    "I don't know why this works.\nI am afraid to investigate.",
    "Please merge. I have been staring at this for 6 hours.",
    "This seemed like a good idea at 2 AM.",
    "Fixes the bug I introduced while fixing another bug.",
    "QA status: vibes-based testing.",
    "If it breaks, it was working yesterday.",
    "This code has been approved by absolutely nobody.",
    "I refuse to elaborate.",
]

# =====================================
# COMMAND HELPER
# =====================================

def run(command, check=True, capture=False):
    return subprocess.run(
        command,
        check=check,
        text=True,
        capture_output=capture
    )

def git(*args, check=True, capture=False):
    return run(["git", *args], check=check, capture=capture)

def gh(*args, check=True):
    return run(["gh", *args], check=check)

# =====================================
# CHECK REQUIREMENTS
# =====================================

if "YOUR_USERNAME" in REPO or "YOUR_REPO" in REPO:
    raise SystemExit("Set your GitHub repository URL first.")

if "YOUR_GITHUB_EMAIL" in GITHUB_EMAIL:
    raise SystemExit("Set your GitHub email first.")

run(["git", "--version"])
run(["gh", "--version"])

# Verify GitHub authentication
gh("auth", "status")

# =====================================
# INITIALIZE / RESUME REPOSITORY
# =====================================

REPO_DIR.mkdir(exist_ok=True)
os.chdir(REPO_DIR)

if not Path(".git").exists():
    git("init")
    git("branch", "-M", "main")

    git("config", "user.name", "Totally Legit Developer")
    git("config", "user.email", GITHUB_EMAIL)

    git("remote", "add", "origin", REPO)

    # Get the existing GitHub history, if any
    run(["git", "fetch", "origin"], check=False)

    result = git(
        "ls-remote", "--heads", "origin", "main",
        check=False, capture=True
    )

    # Already on an unborn "main"; only adopt remote history if it exists
    if result.stdout.strip():
        git("checkout", "-B", "main", "origin/main")

else:
    print("Existing repository detected. Resuming...")

    # Ensure the correct branch
    git("checkout", "main")

    # Ensure remote exists
    result = git("remote", check=False, capture=True)

    if "origin" not in result.stdout.split():
        git("remote", "add", "origin", REPO)

    git("config", "user.name", "Totally Legit Developer")
    git("config", "user.email", GITHUB_EMAIL)

# =====================================
# SYNC WITH GITHUB
# =====================================

git("fetch", "origin")

result = git(
    "rev-parse", "--verify", "origin/main",
    check=False
)

if result.returncode == 0:
    # Rebase local commits on top of remote history
    git("rebase", "--autostash", "origin/main")

# =====================================
# GENERATE COMMITS
# =====================================

print("\nGenerating ridiculous commits...\n")

chaos_file = Path("chaos.txt")

for i in range(TOTAL_COMMITS):

    # Unique marker prevents duplicate work on reruns
    marker = f"Chaos attempt #{i + 1}"

    current = chaos_file.read_text() if chaos_file.exists() else ""

    if marker in current:
        continue

    current += (
        f"\n{marker}\n"
        f"Status: probably broken\n"
        f"Confidence: {random.randint(0, 100)}%\n"
    )

    chaos_file.write_text(current)

    git("add", "chaos.txt")

    git(
        "commit",
        "-m",
        random.choice(commit_messages)
    )

    print(f"Commit {i + 1}/{TOTAL_COMMITS}")

# =====================================
# PUSH MAIN
# =====================================

print("\nPushing commits to GitHub...\n")

git("fetch", "origin")

# Rebase if remote advanced since our last fetch
result = git(
    "rev-parse", "--verify", "origin/main",
    check=False
)

if result.returncode == 0:
    git("rebase", "--autostash", "origin/main")

git("push", "-u", "origin", "main")

# =====================================
# CREATE PULL REQUESTS
# =====================================

print("\nCreating ridiculous pull requests...\n")

for i in range(TOTAL_PRS):

    branch = f"fix/the-problem-{i + 1}"

    # Check whether the PR already exists
    existing = subprocess.run(
        [
            "gh", "pr", "list",
            "--head", branch,
            "--base", "main",
            "--json", "number",
            "--jq", "length"
        ],
        capture_output=True,
        text=True
    )

    if existing.returncode != 0:
        print(f"Could not check PR {i + 1}. Skipping.")
        continue

    if existing.stdout.strip() != "0":
        print(f"PR {i + 1} already exists. Skipping.")
        continue

    # Check whether branch already exists remotely
    remote_branch = git(
        "ls-remote", "--heads", "origin", branch,
        check=False, capture=True
    )

    if remote_branch.stdout.strip():
        print(f"Branch {branch} already exists. Skipping.")
        continue

    git("checkout", "main")

    git("checkout", "-b", branch)

    Path("chaos.txt").write_text(
        f"Attempt #{i + 1}\n"
        "We fixed it. Probably.\n"
        "Please don't inspect further.\n"
    )

    git("add", "chaos.txt")

    git(
        "commit",
        "-m",
        random.choice(commit_messages)
    )

    git("push", "-u", "origin", branch)

    # Create PR
    title = random.choice(pr_titles)
    body = random.choice(pr_bodies)

    gh(
        "pr", "create",
        "--title", title,
        "--body", body,
        "--base", "main",
        "--head", branch
    )

    print(f"Created PR {i + 1}/{TOTAL_PRS}: {title}")

    git("checkout", "main")

# =====================================
# FINISHED
# =====================================

print("\n" + "=" * 45)
print("CHAOS SUCCESSFULLY DEPLOYED.")
print("=" * 45)

print(f"Commits target: {TOTAL_COMMITS}")
print(f"PRs target: {TOTAL_PRS}")
print("Check your GitHub repository for the damage.")
