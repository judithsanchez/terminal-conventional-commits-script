import subprocess


def unstage_all_files() -> None:
    """Unstage all files that were staged for commit"""
    subprocess.run(
        ["git", "reset", "HEAD"],
        capture_output=True,
        text=True
    )
