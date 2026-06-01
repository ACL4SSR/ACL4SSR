#!/usr/bin/env python3
import base64
import re
import os
import sys

def fetch_gfwlist(url="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"):
    try:
        import urllib.request
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching GFWList: {e}")
        sys.exit(1)

def extract_domain_from_url(url):
    url = url.strip()
    if url.endswith('^'):
        url = url[:-1]
    url = url.rstrip('/')

    domain_match = re.search(r'(?:https?://)?(?:www\.)?([^/:]+)', url)
    if domain_match:
        return domain_match.group(1)
    return url

def parse_gfwlist(content):
    blacklist = []
    whitelist = []
    
    try:
        decoded = base64.b64decode(content).decode('utf-8')
    except:
        decoded = content
    
    for line in decoded.split('\n'):
        line = line.strip()
        
        if not line or line.startswith('!') or line.startswith('['):
            continue
        
        if line.startswith('@@||'):
            domain = line[4:]
            if domain.endswith('^'):
                domain = domain[:-1]
            whitelist.append(domain)
        elif line.startswith('||'):
            domain = line[2:]
            if domain.endswith('^'):
                domain = domain[:-1]
            blacklist.append(domain)
        elif line.startswith('@@|') and len(line) > 3:
            domain = extract_domain_from_url(line[3:])
            if domain:
                whitelist.append(domain)
        elif line.startswith('|') and len(line) > 1:
            domain = extract_domain_from_url(line[1:])
            if domain:
                blacklist.append(domain)
    
    return blacklist, whitelist

def format_domain_suffix_rules(domains):
    rules = []
    for domain in sorted(set(domains)):
        if domain:
            rules.append(f"- DOMAIN-SUFFIX,{domain}")
    return rules

def format_acl_rules(domains):
    rules = []
    for domain in sorted(set(domains)):
        if domain:
            rules.append(f"(^|\\.){domain}$")
    return rules

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_acl_file(domains, filename, title="GFWList Rules"):
    header = f"""#**********************************************************************
# {title}
# Generated from GFWList
#
# 更新记录 https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/more/New.md
#
#**********************************************************************

[bypass_all]
### 默认直连 自己可以自定义
### [outbound_block_list] 禁止访问列表
### [bypass_list] 直连列表 禁止访问列表
### [proxy_list] 代理列表

#**********************************************************************
[proxy_list]

# GFWList
"""
    rules = format_acl_rules(domains)
    content = header + '\n'.join(rules) + '\n'
    write_file(filename, content)

def generate_clash_provider_yaml(domains, filename, title="payload"):
    unique_domains = sorted(set(domains))
    content = f"{title}:\n"
    for domain in unique_domains:
        content += f"  - DOMAIN-SUFFIX,{domain}\n"
    write_file(filename, content)

def generate_clash_ruleset_list(domains, filename, title="GFWList"):
    unique_domains = sorted(set(domains))
    content = f"# 内容：{title}\n# 数量：{len(unique_domains)}条\n"
    for domain in unique_domains:
        content += f"DOMAIN-SUFFIX,{domain}\n"
    write_file(filename, content)

def main():
    print("Fetching GFWList...")
    content = fetch_gfwlist()

    print("Parsing GFWList...")
    blacklist, whitelist = parse_gfwlist(content)

    print(f"Blacklist entries: {len(blacklist)}")
    print(f"Whitelist entries: {len(whitelist)}")

    generate_acl_file(blacklist, 'Acl/fullgfwlist.acl', "GFWList Blacklist")
    print("Generated: Acl/fullgfwlist.acl")

    generate_clash_provider_yaml(blacklist, 'Clash/Providers/ProxyGFWlist.yaml', 'payload')
    print("Generated: Clash/Providers/ProxyGFWlist.yaml")

    generate_clash_ruleset_list(blacklist, 'Clash/Ruleset/ProxyGFWlist.list', 'GFWList 黑名单')
    print("Generated: Clash/Ruleset/ProxyGFWlist.list")

    generate_clash_provider_yaml(whitelist, 'Clash/Providers/UnBan.yaml', 'payload')
    print("Generated: Clash/Providers/UnBan.yaml")

    generate_clash_ruleset_list(whitelist, 'Clash/Ruleset/UnBan.list', 'GFWList 白名单')
    print("Generated: Clash/Ruleset/UnBan.list")

if __name__ == "__main__":
    main()