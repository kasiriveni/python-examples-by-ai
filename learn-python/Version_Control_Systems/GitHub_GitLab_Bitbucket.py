# GitHub, GitLab, Bitbucket

# Example of pushing to a remote repository

# Add a remote repository
print("git remote add origin <repository_url>")

# Push changes to the remote repository
print("git push origin <branch_name>")

# Clone a repository
print("git clone <repository_url>")

# Pull changes from the remote repository
print("git pull origin <branch_name>")

# Additional Examples

# Beginner Level

# Initialize a new Git repository
print("git init")

# Check the status of the repository
print("git status")

# Add files to the staging area
print("git add <file_name>")

# Commit changes with a message
print("git commit -m \"Commit message\"")

# View the current branch
print("git branch")

# Advice Level

# Set up a global username and email for Git
print("git config --global user.name \"Your Name\"")
print("git config --global user.email \"your_email@example.com\"")

# Revert a commit
print("git revert <commit_hash>")

# Reset to a previous commit (destructive)
print("git reset --hard <commit_hash>")

# Create and switch to a new branch in one command
print("git checkout -b <new_branch_name>")

# Rebase a branch onto another branch
print("git rebase <branch_name>")

# Squash commits into a single commit
print("git rebase -i HEAD~<number_of_commits>")

# View detailed commit history with changes
print("git log -p")

# Add a tag to a specific commit
print("git tag -a <tag_name> -m \"Tag message\" <commit_hash>")

# Push tags to the remote repository
print("git push origin --tags")
