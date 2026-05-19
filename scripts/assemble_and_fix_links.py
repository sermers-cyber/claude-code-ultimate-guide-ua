#!/usr/bin/env python3
import os
import re

# Path definitions
ROOT_DIR = "/Users/sergey/Documents/_WORK/Переводы/Cowork Guide/claude-code-ultimate-guide"
PARTS_DIR = os.path.join(ROOT_DIR, "guide/ultimate-guide-uk-parts")
OUTPUT_FILE = os.path.join(ROOT_DIR, "guide/ultimate-guide.uk.md")

ordered_files = [
    "ultimate-guide-uk-index.md",
    "ultimate-guide-uk-01-quick-start.md",
    "ultimate-guide-uk-02-core-concepts.md",
    "ultimate-guide-uk-03-memory-settings.md",
    "ultimate-guide-uk-04-agents.md",
    "ultimate-guide-uk-05-skills.md",
    "ultimate-guide-uk-06-commands.md",
    "ultimate-guide-uk-07-hooks.md",
    "ultimate-guide-uk-08-mcp-servers.md",
    "ultimate-guide-uk-09a-advanced-patterns.md",
    "ultimate-guide-uk-09b-advanced-patterns.md",
    "ultimate-guide-uk-10-reference.md",
    "ultimate-guide-uk-11-ecosystem.md",
]

file_to_anchor = {
    "ultimate-guide-uk-index.md": "#the-ultimate-claude-code-guide--український-переклад",
    "ultimate-guide-uk-01-quick-start.md": "#1-швидкий-старт-день-1",
    "ultimate-guide-uk-02-core-concepts.md": "#2-основні-концепції",
    "ultimate-guide-uk-03-memory-settings.md": "#3-пам'ять-та-налаштування",
    "ultimate-guide-uk-04-agents.md": "#4-агенти",
    "ultimate-guide-uk-05-skills.md": "#5-скіли",
    "ultimate-guide-uk-06-commands.md": "#6-команди",
    "ultimate-guide-uk-07-hooks.md": "#7-хуки",
    "ultimate-guide-uk-08-mcp-servers.md": "#8-mcp-сервери",
    "ultimate-guide-uk-09a-advanced-patterns.md": "#9-розширені-патерни-частина-a",
    "ultimate-guide-uk-09b-advanced-patterns.md": "#9-розширені-патерни-частина-b",
    "ultimate-guide-uk-10-reference.md": "#10-довідник",
    "ultimate-guide-uk-11-ecosystem.md": "#11-ai-екосистема"
}

def fix_markdown_links(content):
    # Stats
    cross_file_anchors = 0
    cross_file_chapters = 0
    relative_path_adjustments = 0

    # 1. Resolve cross-file links with anchor (e.g. [Text](ultimate-guide-uk-01-quick-start.md#anchor))
    # We match [text](filename.md#anchor) and replace it with [text](#anchor)
    def replace_cross_file_anchor(match):
        nonlocal cross_file_anchors
        text = match.group(1)
        anchor = match.group(3)  # includes '#'
        cross_file_anchors += 1
        return f"[{text}]({anchor})"

    # RegEx matching [text](ultimate-guide-uk-something.md#anchor) or [text](ultimate-guide.md#anchor)
    content = re.sub(
        r'\[([^\]]+)\]\(((?:ultimate-guide-uk-[^#)]+\.md)|(?:ultimate-guide\.md))(#[^)]+)\)',
        replace_cross_file_anchor,
        content
    )

    # 2. Resolve cross-file links without anchor (e.g. [Text](ultimate-guide-uk-01-quick-start.md))
    # We look up the anchor from the dictionary
    def replace_cross_file_chapter(match):
        nonlocal cross_file_chapters
        text = match.group(1)
        filename = match.group(2)
        cross_file_chapters += 1
        
        if filename == "ultimate-guide.md":
            # Keep pointer to english file if it's there
            return f"[{text}](ultimate-guide.md)"
            
        anchor = file_to_anchor.get(filename, "")
        if anchor:
            return f"[{text}]({anchor})"
        else:
            print(f"Warning: could not find anchor for {filename}")
            return f"[{text}]({filename})"

    content = re.sub(
        r'\[([^\]]+)\]\(((?:ultimate-guide-uk-[^#)]+\.md)|(?:ultimate-guide\.md))\)',
        replace_cross_file_chapter,
        content
    )

    # 3. Adjust relative paths of other links
    # Match any [text](relative_url) where relative_url is a relative path (not starting with http, https, #, mailto, etc.)
    def replace_relative_link(match):
        nonlocal relative_path_adjustments
        text = match.group(1)
        url = match.group(2)
        
        # Skip absolute links, internal anchors, mailto, etc.
        if (url.startswith("http://") or 
            url.startswith("https://") or 
            url.startswith("#") or 
            url.startswith("mailto:") or 
            url.startswith("javascript:")):
            return match.group(0)
            
        # Perform relative adjustment
        new_url = url
        if url.startswith("../../"):
            new_url = url[3:]  # e.g., ../../examples -> ../examples
            relative_path_adjustments += 1
        elif url.startswith("../"):
            new_url = "./" + url[3:]  # e.g., ../core -> ./core
            relative_path_adjustments += 1
            
        return f"[{text}]({new_url})"

    # RegEx matching [text](url)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_relative_link, content)

    return content, cross_file_anchors, cross_file_chapters, relative_path_adjustments

def main():
    print("=== Assembling ultimate-guide.uk.md ===")
    
    total_cross_file_anchors = 0
    total_cross_file_chapters = 0
    total_relative_adjustments = 0
    
    assembled_blocks = []
    
    for filename in ordered_files:
        filepath = os.path.join(PARTS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Error: Required chapter file not found: {filepath}")
            return
        
        print(f"Reading: {filename}...")
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
            
        # Apply link fixes to the individual chapter
        fixed_content, anchors_fixed, chapters_fixed, rels_fixed = fix_markdown_links(file_content)
        total_cross_file_anchors += anchors_fixed
        total_cross_file_chapters += chapters_fixed
        total_relative_adjustments += rels_fixed
        
        # Standardize whitespace and append to blocks
        fixed_content = fixed_content.strip()
        assembled_blocks.append(fixed_content)
        
    # Join the chapters with a single separator (let's use 2 newlines + a clean divider line)
    # The English master guide matches the H1 directly. We will separate using two newlines and a standard blank line
    separator = "\n\n"
    compiled_guide = separator.join(assembled_blocks)
    
    # Add localization footer
    footer = "\n\n---\n**Локалізація**: [Serhii (MacPlus Software)](https://macplus-software.com)\n*Остання синхронізація: Травень 2026*\n"
    compiled_guide += footer
    
    # Write to final master file
    print(f"Writing assembled master file to: {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(compiled_guide)
        
    print("\nAssembly Completed successfully!")
    print(f"- Cross-file anchor links simplified: {total_cross_file_anchors}")
    print(f"- Cross-file chapter links converted to anchors: {total_cross_file_chapters}")
    print(f"- Relative folder links adjusted (going up 1 fewer level): {total_relative_adjustments}")
    print(f"- Localization footer appended.")
    print(f"- Estimated size: {os.path.getsize(OUTPUT_FILE) / 1024:.2f} KB")

if __name__ == "__main__":
    main()
