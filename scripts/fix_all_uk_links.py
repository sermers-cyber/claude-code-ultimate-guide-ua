#!/usr/bin/env python3
import os
import re

ROOT_DIR = "/Users/sergey/Documents/_WORK/Переводы/Cowork Guide/claude-code-ultimate-guide"
GUIDE_DIR = os.path.join(ROOT_DIR, "guide")

# Absolute GitHub repo patterns to match
# Match: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/... or similar
GITHUB_REPO_REGEX = re.compile(
    r'https://github\.com/(?:FlorianBruniaux|gerasimsergey)/claude-code-ultimate-guide(?:-ua)?/blob/main/([^)]+)'
)

def get_relative_path(from_file, to_file):
    """Calculates relative path from from_file directory to to_file."""
    from_dir = os.path.dirname(from_file)
    rel_path = os.path.relpath(to_file, from_dir)
    return rel_path

def fix_links_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    changes = []

    # Markdown links: [text](url)
    # We find all matches of markdown links
    def link_replacer(match):
        text = match.group(1)
        url = match.group(2)

        # 1. Check if it's an absolute GitHub URL to our repo
        github_match = GITHUB_REPO_REGEX.match(url)
        if github_match:
            repo_path_with_anchor = github_match.group(1)
            # Separate path and anchor
            parts = repo_path_with_anchor.split('#', 1)
            repo_path = parts[0]
            anchor = "#" + parts[1] if len(parts) > 1 else ""

            # Check if this file exists locally in our repo
            local_target_path = os.path.join(ROOT_DIR, repo_path)
            
            # If it is a markdown file, check if we have a .uk.md version
            if local_target_path.endswith(".md") and not local_target_path.endswith(".uk.md"):
                uk_target_path = local_target_path[:-3] + ".uk.md"
                if os.path.exists(uk_target_path):
                    local_target_path = uk_target_path
                    repo_path = repo_path[:-3] + ".uk.md"

            if os.path.exists(local_target_path):
                # We can convert it into a beautiful relative link!
                rel_url = get_relative_path(filepath, local_target_path)
                if anchor:
                    rel_url += anchor
                changes.append(f"Absolute GtHub -> Relative: {url} -> {rel_url}")
                return f"[{text}]({rel_url})"

        # 2. Check if it's a relative/local markdown link pointing to .md
        # Skip absolute web URLs, mailto, anchor-only links
        if (url.startswith("http://") or 
            url.startswith("https://") or 
            url.startswith("#") or 
            url.startswith("mailto:") or 
            url.startswith("javascript:")):
            return match.group(0)

        # Separate path and anchor
        url_parts = url.split('#', 1)
        path_part = url_parts[0]
        anchor_part = "#" + url_parts[1] if len(url_parts) > 1 else ""

        # If it points to a .md file (and not already .uk.md)
        if path_part.endswith(".md") and not path_part.endswith(".uk.md"):
            # Determine absolute path of target
            file_dir = os.path.dirname(filepath)
            target_abs = os.path.abspath(os.path.join(file_dir, path_part))

            # Check if corresponding .uk.md exists
            uk_target_abs = target_abs[:-3] + ".uk.md"
            if os.path.exists(uk_target_abs):
                # Replace link path with .uk.md
                new_path_part = path_part[:-3] + ".uk.md"
                new_url = new_path_part + anchor_part
                changes.append(f"Relative .md -> .uk.md: {url} -> {new_url}")
                return f"[{text}]({new_url})"

        return match.group(0)

    # Apply replacement using regex
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_replacer, content)

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return changes
    return []

def main():
    print("=== Scanning and Fixing Ukrainian Links across guide/ ===")
    total_files = 0
    modified_files = 0
    total_changes = 0

    for root, dirs, files in os.walk(GUIDE_DIR):
        for file in files:
            if file.endswith(".uk.md"):
                filepath = os.path.join(root, file)
                total_files += 1
                rel_filepath = os.path.relpath(filepath, ROOT_DIR)
                
                try:
                    changes = fix_links_in_file(filepath)
                    if changes:
                        modified_files += 1
                        total_changes += len(changes)
                        print(f"\nModified: {rel_filepath} ({len(changes)} changes):")
                        for change in changes[:10]: # Print first 10 changes
                            print(f"  - {change}")
                        if len(changes) > 10:
                            print(f"  - ... and {len(changes) - 10} more changes")
                except Exception as e:
                    print(f"Error processing {rel_filepath}: {e}")

    print("\n=== Scan Completed! ===")
    print(f"Total Ukrainian (.uk.md) files scanned: {total_files}")
    print(f"Total files modified: {modified_files}")
    print(f"Total link replacements made: {total_changes}")

if __name__ == "__main__":
    main()
