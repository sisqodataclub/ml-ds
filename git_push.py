import os
import subprocess

# Replace this with your specific GitHub repository URL
repo_url = "https://github.com/sisqodataclub/ml-ds.git"  # Replace with your GitHub repository URL

# Git commands to push the entire folder
commands = [
    "git init",
    "git add .",  # Add all files in the current folder
    'git commit -m "Added project files"',
    f"git remote add origin {repo_url}",
    "git branch -M main",
    "git push -u origin main"
]

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running command: {command}")
        print(e)

for command in commands:
    run_command(command)

print("✅ Project folder successfully pushed to GitHub!")
