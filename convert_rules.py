import requests
import yaml
import os

# ================= 配置区域 =================
# 格式： "输出文件名": ["URL地址1", "URL地址2", ...]
# 每一个 key 代表一个生成的 YAML 文件
TASKS = {
    "Web3.yaml": [
        "https://raw.githubusercontent.com/szkane/ClashRuleSet/main/Clash/Web3.list",
    ],
    "AI.yaml": [
        "https://raw.githubusercontent.com/szkane/ClashRuleSet/main/Clash/Ruleset/AiDomain.list"
    ]
}
# ===========================================

def fetch_and_convert():
    # 遍历任务字典
    for filename, urls in TASKS.items():
        print(f"\n========== Processing Task: {filename} ==========")
        unique_rules = set() # 使用集合去重

        for url in urls:
            print(f"Downloading: {url}...")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                content = response.text
                count = 0
                
                for line in content.splitlines():
                    line = line.strip()
                    if not line or line.startswith('#') or line.startswith('//'):
                        continue
                    
                    # 清洗逻辑：去除末尾的策略后缀
                    parts = line.split(',')
                    clean_rule = ""
                    
                    if len(parts) >= 2:
                        # 格式如: DOMAIN-SUFFIX,google.com,Proxy -> DOMAIN-SUFFIX,google.com
                        clean_rule = f"{parts[0].strip()},{parts[1].strip()}"
                    elif len(parts) == 1:
                        # 格式如: google.com (这种很少见，如果有，需根据情况处理，这里直接保留)
                        clean_rule = line
                    
                    if clean_rule:
                        unique_rules.add(clean_rule)
                        count += 1
                print(f"  -> Found {count} rules.")

            except Exception as e:
                print(f"  -> [Error] Failed to fetch {url}: {e}")
                continue

        # 排序并写入文件
        if unique_rules:
            sorted_rules = sorted(list(unique_rules))
            yaml_data = {"payload": sorted_rules}

            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
            
            print(f"Success! Saved {len(sorted_rules)} rules to {filename}")
        else:
            print(f"Warning: No rules found for {filename}, skipping file creation.")

if __name__ == "__main__":
    fetch_and_convert()