import subprocess
from datetime import datetime

def run_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}\n{e.stderr}")
        return None

def update_github_repo():
    """Pull, add, commit, and push changes to the GitHub repository."""
    try:
        # Step 1: Pull the latest changes from the remote repository
        print("Pulling the latest changes...")
        run_command(["git", "pull"])

        # Step 2: Add all new or modified files
        print("Adding new and modified files...")
        run_command(["git", "add", "."])

        # Step 3: Commit the changes with a timestamp
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Reports add on {current_date}"
        print(f"Committing changes with message: {commit_message}")
        run_command(["git", "commit", "-m", commit_message])

        # Step 4: Push the changes to the remote repository
        print("Pushing changes to the remote repository...")
        run_command(["git", "push"])
        print("Repository updated successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Starting repository update...")
    update_github_repo()
