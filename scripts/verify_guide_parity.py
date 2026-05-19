#!/usr/bin/env python3
import os
import re

# Path definitions
ROOT_DIR = "/Users/sergey/Documents/_WORK/Переводы/Cowork Guide/claude-code-ultimate-guide"
EN_FILE = os.path.join(ROOT_DIR, "guide/ultimate-guide.md")
UK_FILE = os.path.join(ROOT_DIR, "guide/ultimate-guide.uk.md")

def parse_markdown(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Track code block fence state following CommonMark specifications
    in_code_block = False
    fence_char = None
    fence_length = 0
    code_blocks_count = 0

    headers = {
        "H1": [],
        "H2": [],
        "H3": [],
        "H4": []
    }

    for line in content.splitlines():
        # Check for code block fence
        # Matches lines starting with optional whitespace followed by 3 or more backticks or tildes
        match = re.match(r'^\s*([`~]{3,})', line)
        if match:
            fence = match.group(1)
            char = fence[0]
            length = len(fence)
            
            if not in_code_block:
                # Open a new code block
                in_code_block = True
                fence_char = char
                fence_length = length
                code_blocks_count += 1
                continue
            else:
                # We are in a code block. Check if this line closes it.
                # It closes if the character matches and length is at least the opening fence length
                if char == fence_char and length >= fence_length:
                    in_code_block = False
                    continue
                    
        # Check headers only when not in a code block
        if not in_code_block:
            if line.startswith("# "):
                headers["H1"].append(line)
            elif line.startswith("## "):
                headers["H2"].append(line)
            elif line.startswith("### "):
                headers["H3"].append(line)
            elif line.startswith("#### "):
                headers["H4"].append(line)

    return {
        "content": content,
        "code_blocks": code_blocks_count,
        "headers": headers
    }

def main():
    print("=== Verification of Guide Parity ===")
    
    en_data = parse_markdown(EN_FILE)
    uk_data = parse_markdown(UK_FILE)
    
    if not en_data or not uk_data:
        return
        
    print("\n--- Structural Counts ---")
    print(f"{'Metric':<25} | {'English':<10} | {'Ukrainian':<10} | {'Status':<15}")
    print("-" * 68)
    
    # 1. Compare Code Blocks
    cb_status = "MATCH" if en_data["code_blocks"] == uk_data["code_blocks"] else "MISMATCH"
    print(f"{'Code Blocks':<25} | {en_data['code_blocks']:<10} | {uk_data['code_blocks']:<10} | {cb_status}")
    
    # 2. Compare Headers
    for lvl in ["H1", "H2", "H3", "H4"]:
        count_en = len(en_data["headers"][lvl])
        count_uk = len(uk_data["headers"][lvl])
        
        status = "MATCH"
        if count_en != count_uk:
            # Chapter 9 is split into A and B in Ukrainian, which adds one H1 header
            if lvl == "H1" and count_uk == count_en + 1:
                status = "EXPECTED SPLIT"
            else:
                status = "MISMATCH"
                
        print(f"{lvl + ' Headers':<25} | {count_en:<10} | {count_uk:<10} | {status}")
        
    print("\n--- Verification Details ---")
    
    # Check H1 Header structure
    print(f"\nH1 Headers in English ({len(en_data['headers']['H1'])}):")
    for h in en_data['headers']['H1']:
        print(f"  {h}")
        
    print(f"\nH1 Headers in Ukrainian ({len(uk_data['headers']['H1'])}):")
    for h in uk_data['headers']['H1']:
        print(f"  {h}")
        
    # Check for Footer
    print("\n--- Footer Check ---")
    has_footer = "Локалізація" in uk_data["content"] and "MacPlus Software" in uk_data["content"]
    if has_footer:
        print("[SUCCESS] Localization footer was successfully detected in guide/ultimate-guide.uk.md!")
    else:
        print("[WARNING] Localization footer not found or misspelled!")

if __name__ == "__main__":
    main()
