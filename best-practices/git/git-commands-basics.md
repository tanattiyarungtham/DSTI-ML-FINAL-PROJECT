# Git Commands Guide

## 1. Initializing a Repository
```bash
git init
```
This command initializes a new Git repository in the current directory.

## 2. Adding Files to Staging
### Add all files
```bash
git add .
```
This command adds all modified and new files to the staging area.

### Add a specific file
```bash
git add <filename>
```
This command adds only the specified file to the staging area.

## 3. Committing Changes
```bash
git commit -m "Commit message"
```
This command creates a snapshot of the staged changes with a descriptive message.

## 4. Removing a File from Tracking
```bash
git rm --cached <filename>
```
This command removes a file from Git tracking but keeps it in the working directory.

## 5. Viewing Commit History
```bash
git log
```
This command displays a history of commits in the repository.

## 6. Ignoring Files
Create a `.gitignore` file and add patterns for files and folders to be ignored.
Example:
```
# Ignore all .log files
*.log
```

## 7. Pushing Code to a Remote Repository
```bash
git push origin <branch_name>
```
This command uploads the committed changes to the remote repository.

## 8. Pulling Updates from a Remote Repository
```bash
git pull origin <branch_name>
```
This command fetches and merges changes from the remote repository.

## 9. Checking the Status of the Repository
```bash
git status
```
This command displays the current state of the working directory and staging area.

## 10. Cloning a Repository
```bash
git clone <repository_url>
```
This command creates a local copy of a remote repository.

---
*This guide provides a quick overview of essential Git commands for version control.*
