#!/usr/bin/env python3
import base64
import re
import os
import sys
from glob import glob

def is_ip(s):
    if not s:
        return False
    if s.endswith('^'):
        s = s[:-1]
    if '.' in s and ':' not in s:
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ipv4_pattern, s):
            parts = s.split('.')
            if all(0 <= int(p) <= 255 for p in parts):
                return True
    if ':' in s:
        ipv6_pattern = r'^([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}$|^(::)$|^::1$'
        if re.match(ipv6_pattern, s):
            return True
        if s.startswith('::ffff:'):
            ipv4_in_v6_pattern = r'^::ffff:(\d{1,3}\.){3}\d{1,3}$'
            if re.match(ipv4_in_v6_pattern, s):
                return True
        return False
    return False

def is_cidr(s):
    if '/' not in s:
        return False
    ip_part = s.split('/')[0]
    suffix = s.split('/')[1]
    if not suffix.isdigit():
        return False
    suffix_val = int(suffix)
    if '.' in ip_part and ':' not in ip_part:
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ipv4_pattern, ip_part):
            parts = ip_part.split('.')
            if all(0 <= int(p) <= 255 for p in parts):
                if 0 <= suffix_val <= 32:
                    return True
        return False
    if ':' in ip_part:
        ipv6_pattern = r'^([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}$|^(::)$|^::1$'
        if re.match(ipv6_pattern, ip_part):
            if 0 <= suffix_val <= 128:
                return True
        if ip_part.startswith('::ffff:'):
            ipv4_in_v6_pattern = r'^::ffff:(\d{1,3}\.){3}\d{1,3}$'
            if re.match(ipv4_in_v6_pattern, ip_part):
                if 0 <= suffix_val <= 128:
                    return True
        return False
    return False

def normalize_ip_rule(ip_rule):
    ip_rule = ip_rule.strip()
    if not ip_rule:
        return None
    if ip_rule.endswith('^'):
        ip_rule = ip_rule[:-1]
    if is_ip(ip_rule) or is_cidr(ip_rule):
        return ip_rule
    return None

def normalize_ip_for_clash(ip_rule):
    if is_cidr(ip_rule):
        return ip_rule
    if is_ip(ip_rule):
        if ':' in ip_rule:
            return ip_rule + '/128'
        return ip_rule + '/32'
    return None

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
        domain = domain_match.group(1)
        if domain and not is_ip(domain) and not is_cidr(domain):
            return domain
    return None

def parse_gfwlist(content):
    domain_blacklist = []
    domain_whitelist = []
    ip_blacklist = []
    ip_whitelist = []

    try:
        decoded = base64.b64decode(content).decode('utf-8')
    except:
        decoded = content

    for line in decoded.split('\n'):
        line = line.strip()

        if not line or line.startswith('!') or line.startswith('['):
            continue
        
        # 忽略特定的无效规则
        if line == '||addons.mozilla.org/*-*/firefox/addon/ublock-origin/*':
            continue
        if line == '||addons.mozilla.org/firefox/downloads/file/*/ublock_origin-*.xpi':
            continue

        if line.startswith('@@||'):
            rule = line[4:]
            if rule.endswith('^'):
                rule = rule[:-1]
            if is_ip(rule) or is_cidr(rule):
                normalized = normalize_ip_rule(rule)
                if normalized:
                    ip_whitelist.append(normalized)
            else:
                domain_whitelist.append(rule)
        elif line.startswith('||'):
            rule = line[2:]
            if rule.endswith('^'):
                rule = rule[:-1]
            if is_ip(rule) or is_cidr(rule):
                normalized = normalize_ip_rule(rule)
                if normalized:
                    ip_blacklist.append(normalized)
            else:
                domain_blacklist.append(rule)
        elif line.startswith('@@|') and len(line) > 3:
            domain = extract_domain_from_url(line[3:])
            if domain:
                domain_whitelist.append(domain)
        elif line.startswith('|') and len(line) > 1:
            domain = extract_domain_from_url(line[1:])
            if domain:
                domain_blacklist.append(domain)

    return domain_blacklist, domain_whitelist, ip_blacklist, ip_whitelist

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

def format_ip_cidr_rules(ip_rules):
    rules = []
    for ip in sorted(set(ip_rules)):
        normalized = normalize_ip_for_clash(ip)
        if normalized:
            if ':' in normalized:
                rules.append(f"IP-CIDR6,{normalized},no-resolve")
            else:
                rules.append(f"IP-CIDR,{normalized},no-resolve")
    return rules

def format_ip_cidr_acl_rules(ip_rules):
    rules = []
    for ip in sorted(set(ip_rules)):
        if ip:
            rules.append(ip)
    return rules

def parse_yaml_rule_line(line):
    line = line.strip()
    if not line:
        return None, None
    rule = None
    if line.startswith('- '):
        rule = line[2:]
    elif line.startswith('  - '):
        rule = line[4:]
    else:
        return None, None
    if ',' in rule:
        return rule.split(',', 1)
    return rule, ''

def parse_list_rule_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None, None
    if ',' in line:
        return line.split(',', 1)
    return line, ''

def is_domain_rule_type(rule_type):
    return rule_type in ('DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'DOMAIN-REGEX')

def is_ip_rule_type(rule_type):
    return rule_type in ('IP-CIDR', 'IP-CIDR6', 'IP-SUFFIX', 'IP-ASN')

def split_existing_rule_files():
    print("Splitting existing rule files for mrs conversion...")

    for filepath in glob('Clash/Providers/*.yaml'):
        if '_domain' in filepath or '_ip' in filepath:
            continue
        split_yaml_file(filepath)

    for filepath in glob('Clash/Providers/Ruleset/*.yaml'):
        if '_domain' in filepath or '_ip' in filepath:
            continue
        split_yaml_file(filepath)

    for filepath in glob('Clash/Ruleset/*.list'):
        if '_domain' in filepath or '_ip' in filepath:
            continue
        split_list_file(filepath)

def split_yaml_file(filepath):
    domains = []
    ips = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                rule_type, rule_value = parse_yaml_rule_line(line)
                if not rule_type or not rule_value:
                    continue
                if is_domain_rule_type(rule_type):
                    domains.append((rule_type, rule_value.strip()))
                elif is_ip_rule_type(rule_type):
                    ips.append((rule_type, rule_value.strip()))
    except Exception as e:
        print(f"Warning: Failed to read {filepath}: {e}")
        return

    base_name = os.path.splitext(filepath)[0]
    if domains:
        unique_domains = sorted(set(domains))
        domain_yaml = "payload:\n"
        for rule_type, d in unique_domains:
            domain_yaml += f"  - {rule_type},{d}\n"
        write_file(f"{base_name}_domain.yaml", domain_yaml)
    if ips:
        unique_ips = sorted(set(ips))
        ip_yaml = "payload:\n"
        for rule_type, ip in unique_ips:
            # 去掉 no-resolve 参数，只保留纯 IP/CIDR
            clean_ip = ip.split(',')[0].strip()
            ip_yaml += f"  - {clean_ip}\n"
        write_file(f"{base_name}_ip.yaml", ip_yaml)

def split_list_file(filepath):
    domains = []
    ips = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                rule_type, rule_value = parse_list_rule_line(line)
                if not rule_type or not rule_value:
                    continue
                if is_domain_rule_type(rule_type):
                    domains.append((rule_type, rule_value.strip()))
                elif is_ip_rule_type(rule_type):
                    ips.append((rule_type, rule_value.strip()))
    except Exception as e:
        print(f"Warning: Failed to read {filepath}: {e}")
        return

    base_name = os.path.splitext(filepath)[0]
    if domains:
        unique_domains = sorted(set(domains))
        domain_text = ""
        for rule_type, d in unique_domains:
            domain_text += f"{rule_type},{d}\n"
        write_file(f"{base_name}_domain.list", domain_text)
    if ips:
        unique_ips = sorted(set(ips))
        ip_text = ""
        for rule_type, ip in unique_ips:
            # 去掉 no-resolve 参数，只保留纯 IP/CIDR
            clean_ip = ip.split(',')[0].strip()
            ip_text += f"{clean_ip}\n"
        write_file(f"{base_name}_ip.list", ip_text)

def generate_acl_file(domain_list, ip_list, filename, title="GFWList Rules"):
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
    domain_rules = format_acl_rules(domain_list)
    ip_rules = format_ip_cidr_acl_rules(ip_list)
    all_rules = domain_rules + ip_rules
    content = header + '\n'.join(all_rules) + '\n'
    write_file(filename, content)

def generate_clash_provider_yaml(domain_list, ip_list, filename, title="payload"):
    unique_domains = sorted(set(domain_list))
    content = f"{title}:\n"
    for domain in unique_domains:
        content += f"  - DOMAIN-SUFFIX,{domain}\n"
    ip_rules = format_ip_cidr_rules(ip_list)
    for rule in ip_rules:
        content += f"  - {rule}\n"
    write_file(filename, content)
    
    # 生成分离的临时文件用于 mrs 转换
    base_name = filename.replace('.yaml', '')
    # 域名规则 - YAML 格式
    if unique_domains:
        domain_yaml = f"{title}:\n"
        for domain in unique_domains:
            domain_yaml += f"  - DOMAIN-SUFFIX,{domain}\n"
        write_file(f"{base_name}_domain.yaml", domain_yaml)
    
    # IP 规则 - YAML 格式
    if ip_rules:
        ip_yaml = f"{title}:\n"
        for rule in ip_rules:
            # 去掉规则类型前缀和 no-resolve 参数，只保留纯 IP/CIDR
            clean_rule = rule.split(',')[1].strip() if ',' in rule else rule
            ip_yaml += f"  - {clean_rule}\n"
        write_file(f"{base_name}_ip.yaml", ip_yaml)

def generate_clash_ruleset_list(domain_list, ip_list, filename, title="GFWList"):
    unique_domains = sorted(set(domain_list))
    ip_rules = format_ip_cidr_rules(ip_list)
    total = len(unique_domains) + len(ip_rules)
    content = f"# 内容：{title}\n# 数量：{total}条\n"
    for domain in unique_domains:
        content += f"DOMAIN-SUFFIX,{domain}\n"
    for rule in ip_rules:
        content += f"{rule}\n"
    write_file(filename, content)
    
    # 生成分离的临时文件用于 mrs 转换
    base_name = filename.replace('.list', '')
    # 域名规则 - text 格式
    if unique_domains:
        domain_text = ""
        for domain in unique_domains:
            domain_text += f"DOMAIN-SUFFIX,{domain}\n"
        write_file(f"{base_name}_domain.list", domain_text)
    
    # IP 规则 - text 格式
    if ip_rules:
        ip_text = ""
        for rule in ip_rules:
            # 去掉规则类型前缀和 no-resolve 参数，只保留纯 IP/CIDR
            clean_rule = rule.split(',')[1].strip() if ',' in rule else rule
            ip_text += f"{clean_rule}\n"
        write_file(f"{base_name}_ip.list", ip_text)

def main():
    print("Fetching GFWList...")
    content = fetch_gfwlist()

    print("Parsing GFWList...")
    domain_blacklist, domain_whitelist, ip_blacklist, ip_whitelist = parse_gfwlist(content)

    print(f"Domain blacklist entries: {len(domain_blacklist)}")
    print(f"Domain whitelist entries: {len(domain_whitelist)}")
    print(f"IP blacklist entries: {len(ip_blacklist)}")
    print(f"IP whitelist entries: {len(ip_whitelist)}")

    existing_unban_domains = []
    existing_unban_ips = []

    if os.path.exists('Clash/Providers/UnBan.yaml'):
        with open('Clash/Providers/UnBan.yaml', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('- DOMAIN-SUFFIX,'):
                    existing_unban_domains.append(line.replace('- DOMAIN-SUFFIX,', '', 1))
                elif line.startswith('- IP-CIDR') or line.startswith('  - IP-CIDR'):
                    parts = line.replace('  - ', '').split(',')
                    if len(parts) >= 2:
                        existing_unban_ips.append(parts[1])

    if os.path.exists('Clash/Ruleset/UnBan.list'):
        with open('Clash/Ruleset/UnBan.list', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('DOMAIN-SUFFIX,'):
                    existing_unban_domains.append(line.replace('DOMAIN-SUFFIX,', '', 1))
                elif line.startswith('IP-CIDR'):
                    parts = line.split(',')
                    if len(parts) >= 2:
                        existing_unban_ips.append(parts[1])

    if existing_unban_domains:
        new_count = 0
        for d in existing_unban_domains:
            if d and d not in domain_whitelist:
                domain_whitelist.append(d)
                new_count += 1
        if new_count > 0:
            print(f"Merged {new_count} existing UnBan domains")

    if existing_unban_ips:
        new_count = 0
        for ip in existing_unban_ips:
            if ip and ip not in ip_whitelist:
                ip_whitelist.append(ip)
                new_count += 1
        if new_count > 0:
            print(f"Merged {new_count} existing UnBan IPs")

    generate_acl_file(domain_blacklist, ip_blacklist, 'Acl/fullgfwlist.acl', "GFWList Blacklist")
    print("Generated: Acl/fullgfwlist.acl")

    generate_clash_provider_yaml(domain_blacklist, ip_blacklist, 'Clash/Providers/ProxyGFWlist.yaml', 'payload')
    print("Generated: Clash/Providers/ProxyGFWlist.yaml")

    generate_clash_ruleset_list(domain_blacklist, ip_blacklist, 'Clash/Ruleset/ProxyGFWlist.list', 'GFWList 黑名单')
    print("Generated: Clash/Ruleset/ProxyGFWlist.list")

    generate_clash_provider_yaml(domain_whitelist, ip_whitelist, 'Clash/Providers/UnBan.yaml', 'payload')
    print("Generated: Clash/Providers/UnBan.yaml")

    generate_clash_ruleset_list(domain_whitelist, ip_whitelist, 'Clash/Ruleset/UnBan.list', 'GFWList 白名单')
    print("Generated: Clash/Ruleset/UnBan.list")

    split_existing_rule_files()

if __name__ == "__main__":
    main()
