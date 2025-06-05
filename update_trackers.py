import requests
import time

# Tracker源URL列表
tracker_urls = [
    "https://cf.trackerslist.com/all.txt",
    "https://api.yaozuopan.top:88/composite?key=bt&auth=3cae9a3a53f1daef137126648a535ab7",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt"
]

all_trackers = set()

print("Fetching trackers...")
for url in tracker_urls:
    try:
        # 增加超时和重试机制会更健壮，这里简化处理
        print(f"Fetching from: {url}")
        response = requests.get(url, timeout=30) # 30秒超时
        response.raise_for_status()  # 如果HTTP错误，则抛出异常
        
        # 按行分割，并去除首尾空格
        trackers_from_source = [t.strip() for t in response.text.splitlines()]
        
        # 过滤空行和非http/udp开头的行（可选，增强健壮性）
        valid_trackers = {
            t for t in trackers_from_source 
            if t and (t.startswith("http://") or t.startswith("https://") or t.startswith("udp://"))
        }
        
        print(f"  Found {len(valid_trackers)} valid trackers.")
        all_trackers.update(valid_trackers)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with {url}: {e}")
    time.sleep(1) # 稍微停顿一下，避免请求过于频繁

# 将集合转换为列表并排序（可选）
sorted_trackers = sorted(list(all_trackers))

# 写入到文件
output_filename = "trackers_combined.txt"
with open(output_filename, "w") as f:
    for tracker in sorted_trackers:
        f.write(tracker + "\n")

print(f"\nTotal unique trackers: {len(sorted_trackers)}")
print(f"Combined list saved to {output_filename}")
