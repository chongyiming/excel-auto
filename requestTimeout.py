
# import re

# # Step 1: Read the log file
# with open("logfile.txt", "r", encoding="utf-8") as file:
#     content = file.read()

# # Step 2: Find all #[number] patterns
# matches = re.findall(r"#\d+", content)

# # Step 3: Remove duplicates and sort numerically
# unique_matches = sorted(set(matches), key=lambda x: int(x[1:]))

# # Step 4: Write to output file in comma-separated format
# with open("unique_hash_numbers.txt", "w", encoding="utf-8") as output:
#     output.write(",".join(unique_matches))

# print("✅ Done! Saved to 'unique_hash_numbers.txt'")

import re

completed_ids = set()
all_matches = []

# Step 1: 读取日志文件
with open("logfile.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    print(lines[0])

# Step 2: 找出所有 completed 的 orderid
for line in lines:
    if re.search(r"\bcompleted\b", line, re.IGNORECASE):
        found = re.findall(r"#\d+", line)
        completed_ids.update(found)

# Step 3: 找出所有非 completed 的 orderid
for line in lines:
    found = re.findall(r"#\d+", line)
    for order_id in found:
        if order_id not in completed_ids:
            all_matches.append(order_id)

# Step 4: 去重并按数字排序
unique_matches = sorted(set(all_matches), key=lambda x: int(x[1:]))

# Step 5: 写入文件
with open("unique_hash_numbers.txt", "w", encoding="utf-8") as output:
    output.write(",".join(unique_matches))

print("✅ Done! Saved to 'unique_hash_numbers.txt'")