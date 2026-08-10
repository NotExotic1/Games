import os
import shutil
import subprocess
import sys
import tempfile

# ============================================================
# CONFIG
# ============================================================

REPO = "https://github.com/NotExotic1/Games.git"
BRANCH = "main"
DESTINATION = "ports"

# ============================================================
# PATHS
# ============================================================

SCRIPT_PATH = os.path.abspath(__file__)
SOURCE_FOLDER = os.path.dirname(SCRIPT_PATH)
FOLDER_NAME = os.path.basename(SOURCE_FOLDER)

# Temporary clone location
CLONE_FOLDER = os.path.join(
    tempfile.gettempdir(),
    "Games_GitHub_Upload"
)

# ============================================================
# RUN COMMAND
# ============================================================

def run(command, cwd=None):
    print()
    print("> " + " ".join(command))
    print()

    result = subprocess.run(
        command,
        cwd=cwd,
        text=True
    )

    if result.returncode != 0:
        print()
        print("COMMAND FAILED.")
        sys.exit(result.returncode)

# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("       NexusXV GitHub Uploader")
    print("========================================")
    print()

    print("Source:")
    print(SOURCE_FOLDER)
    print()

    print("Destination:")
    print(
        f"https://github.com/NotExotic1/Games/tree/main/"
        f"ports/{FOLDER_NAME}"
    )
    print()

    # --------------------------------------------------------
    # Check Git
    # --------------------------------------------------------

    try:
        subprocess.run(
            ["git", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except Exception:
        print("Git is NOT installed.")
        print()
        print("Install Git from:")
        print("https://git-scm.com/download/win")
        print()
        input("Press Enter to exit...")
        return

    # --------------------------------------------------------
    # Remove old temporary clone
    # --------------------------------------------------------

    if os.path.exists(CLONE_FOLDER):
        print("Removing old temporary repository...")
        shutil.rmtree(CLONE_FOLDER)

    # --------------------------------------------------------
    # Clone repository
    # --------------------------------------------------------

    print("Cloning GitHub repository...")

    run([
        "git",
        "clone",
        "--branch",
        BRANCH,
        REPO,
        CLONE_FOLDER
    ])

    # --------------------------------------------------------
    # Create destination
    # --------------------------------------------------------

    destination = os.path.join(
        CLONE_FOLDER,
        DESTINATION,
        FOLDER_NAME
    )

    os.makedirs(destination, exist_ok=True)

    # --------------------------------------------------------
    # Copy files
    # --------------------------------------------------------

    print()
    print("Copying files...")
    print()

    copied = 0

    for root, directories, files in os.walk(SOURCE_FOLDER):

        # Don't enter Git folders
        directories[:] = [
            d for d in directories
            if d != ".git"
        ]

        for filename in files:

            source_file = os.path.join(root, filename)

            # Never copy this uploader
            if os.path.abspath(source_file) == SCRIPT_PATH:
                continue

            relative = os.path.relpath(
                source_file,
                SOURCE_FOLDER
            )

            target_file = os.path.join(
                destination,
                relative
            )

            os.makedirs(
                os.path.dirname(target_file),
                exist_ok=True
            )

            shutil.copy2(
                source_file,
                target_file
            )

            size = os.path.getsize(source_file)

            print(
                f"Copied: {relative} "
                f"({size / 1024 / 1024:.2f} MB)"
            )

            copied += 1

    print()
    print(f"Copied {copied} file(s).")

    # --------------------------------------------------------
    # Git status
    # --------------------------------------------------------

    run(
        ["git", "status", "--short"],
        cwd=CLONE_FOLDER
    )

    # --------------------------------------------------------
    # Add files
    # --------------------------------------------------------

    print("Adding files...")

    run(
        ["git", "add", "--", f"ports/{FOLDER_NAME}"],
        cwd=CLONE_FOLDER
    )

    # --------------------------------------------------------
    # Commit
    # --------------------------------------------------------

    print("Creating commit...")

    result = subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"Add {FOLDER_NAME} game port"
        ],
        cwd=CLONE_FOLDER,
        text=True
    )

    # No changes isn't necessarily an error
    if result.returncode != 0:
        print()
        print("Nothing new to commit.")
        print()
        input("Press Enter to exit...")
        return

    # --------------------------------------------------------
    # Push
    # --------------------------------------------------------

    print()
    print("Pushing to GitHub...")
    print()

    run(
        ["git", "push", "origin", BRANCH],
        cwd=CLONE_FOLDER
    )

    # --------------------------------------------------------
    # Done
    # --------------------------------------------------------

    print()
    print("========================================")
    print("          UPLOAD COMPLETE")
    print("========================================")
    print()
    print(f"Folder: ports/{FOLDER_NAME}")
    print(f"Files:  {copied}")
    print()
    print(
        f"https://github.com/NotExotic1/Games/tree/main/"
        f"ports/{FOLDER_NAME}"
    )
    print()

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()