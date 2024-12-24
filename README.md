# GitHub Activity CLI

The **GitHub Activity CLI** is a simple command-line interface tool that allows you to fetch and display the recent activity of a GitHub user. This project interacts with the GitHub API to retrieve user events and presents them in a clean, readable format.

---

## What It Does

This CLI fetches and displays the following types of GitHub events:

- **PushEvent**: Displays the number of commits pushed to a repository.
- **PublicEvent**: Indicates that a repository is made public.
- **WatchEvent**: Shows that a repository is starred by the user.

---

## How to Run

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/47thommy/github-activity-cli.git
   cd github-activity-cli
   ```

2. **Run the CLI**:

   ```bash
   python github_activity_cli.py
   ```

3. **Fetch User Activity**:

   - Type the command `github_activity <username>` to fetch recent activity for a specific GitHub user.
   - Example:
     ```bash
     github_activity 47thommy
     ```

4. **Exit the CLI**:
   - Type `exit` to quit.

---
