import os
import subprocess
import sys

from infrastructure.framework.appcraft.core.app_runner import AppRunner


class GitRunner(AppRunner):
    @AppRunner.runner
    def create(self):
        GITHUB_USER = subprocess.getoutput("gh api user | jq -r .login")
        if "gh: command not found" in GITHUB_USER:
            print(
                "\
Error: GitHub CLI (gh) not found. Install it from: https://cli.github.com/"
            )
            sys.exit(1)

        repo_name = input("Repository name: ").strip()
        repo_desc = input("Repository description: ").strip()
        repo_visibility = (
            input("Public or Private? (public/private): ").strip().lower()
        )

        if repo_visibility not in ["public", "private"]:
            print("Error: Invalid visibility! Use 'public' or 'private'.")
            sys.exit(1)

        os.makedirs(repo_name, exist_ok=True)
        os.chdir(repo_name)
        subprocess.run(["git", "init"])
        subprocess.run(["git", "checkout", "-b", "main"])

        with open("README.md", "w") as f:
            f.write(f"# {repo_name}\n\n{repo_desc}")

        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Initial commit"])

        print("🔄 Creating repository on GitHub using GitHub CLI...")
        create_repo_command = [
            "gh",
            "repo",
            "create",
            repo_name,
            "--description",
            repo_desc,
            "--visibility",
            repo_visibility,
            "--confirm",
        ]

        result = subprocess.run(
            create_repo_command, capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ Repository successfully created!")
        else:
            print(
                f"\
❌ Error creating repository using GitHub CLI: {result.stderr}"
            )
            sys.exit(1)

        repo_url = f"https://github.com/{GITHUB_USER}/{repo_name}.git"

        subprocess.run(["git", "remote", "add", "origin", repo_url])
        subprocess.run(["git", "push", "-u", "origin", "main"])

        print(f"🚀 Repository '{repo_name}' created and synced with GitHub!")
