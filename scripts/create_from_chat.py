#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path


def process_chat_history(content):
    """Process chat history and create files."""
    # Pattern to match file headers like [file:name](path) line:x-y
    file_pattern = r"\[file:([^]]+)\]\(([^)]+)\)"

    # Split content on markdown code blocks
    blocks = content.split("```")

    current_file = None
    for i, block in enumerate(blocks):
        if i % 2 == 0:  # Non-code block, look for file headers
            match = re.search(file_pattern, block)
            if match:
                current_file = match.group(2)
        else:  # Code block
            if current_file:
                # Skip the language identifier line if present
                code = block.split("\n", 1)[1] if block.find("\n") != -1 else block

                # Create directory if needed
                file_path = Path(current_file)
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Write the file
                file_path.write_text(code.strip())
                print(f"Created: {current_file}")
                current_file = None


def make_executable(file_path):
    """Make a file executable."""
    mode = os.stat(file_path).st_mode
    os.chmod(file_path, mode | 0o111)  # Add executable bit


def main():
    if len(sys.argv) != 2:
        print("Usage: create_from_chat.py <chat_history_file>")
        sys.exit(1)

    chat_file = Path(sys.argv[1])
    if not chat_file.exists():
        print(f"Error: File {chat_file} not found")
        sys.exit(1)

    content = chat_file.read_text()
    process_chat_history(content)

    # Make specific files executable
    executable_files = ["backend/celery_worker.sh", "scripts/create_from_chat.py"]

    for file in executable_files:
        if os.path.exists(file):
            make_executable(file)
            print(f"Made executable: {file}")


if __name__ == "__main__":
    main()
