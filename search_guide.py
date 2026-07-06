with open("guide_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("--- CHAPTER SEARCH IN GUIDE ---")
for idx, line in enumerate(lines):
    if "chapter" in line.lower() or "methodology" in line.lower() or "system analysis" in line.lower() or "design" in line.lower():
        if len(line.strip()) < 100:
            print(f"L{idx+1}: {line.strip()}")
