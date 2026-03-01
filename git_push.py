import subprocess
import os
import sys

def run_cmd(cmd):
    print(f"Running: {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Error ({process.returncode}):\n{err}")
    else:
        print(f"Success:\n{out}")
    return process.returncode

target_dir = r"d:\workai\course-site"
os.chdir(target_dir)

# Initialize git if not already initialized
if not os.path.exists(".git"):
    run_cmd("git init")

# Ensure user config is set so commit doesn't fail
run_cmd('git config user.email "admin@example.com"')
run_cmd('git config user.name "AI Assistant"')

# Add all changes
run_cmd("git add .")

# Commit changes
run_cmd('git commit -m "Update construction law course and clean up scripts"')

# Configure remote and push
# Remove existing origin just in case
run_cmd("git remote remove origin")
run_cmd("git remote add origin https://github.com/chinys/course-site.git")

# Push to main (or master)
# Check current branch
branches = subprocess.check_output("git branch", shell=True, text=True)
branch_name = "main"
if "* master" in branches:
    run_cmd("git branch -m master main")

print("Pushing to origin main...")
ret = run_cmd("git push -u origin main --force")
print("Done.")
