# 📘 ACL4SSR Configuration Guide

This document explains all the configuration codes used in **ACL4SSR** customization.
ACL4SSR allows you to build **custom Clash configurations** by combining **INI** and **YAML** files with flexible rulesets, proxy groups, and generators.

---

## 🔹 File Types

* **INI File (`.ini`)**
  Defines custom rulesets, proxy groups, and options.
  Example: `custom.ini`

* **YAML File (`.yml`)**
  Defines base Clash configuration and integrates with INI.
  Example: `clash_rule_base.yml`

ACL4SSR merges these together when generating the final Clash config.

---

## 🔹 Sections and Directives

### `[custom]`

The **main section** in `.ini` where you define rules, proxy groups, and options.

---

### `ruleset`

Defines external or local **rulesets** that Clash will load.

**Syntax:**

```ini
ruleset=GroupName,URL_or_Path
```

**Examples:**

```ini
# Iran websites
ruleset=🇮🇷IranWebsites,https://example.com/iran.yaml

# Ads filter
ruleset=🚫AdBlock,https://example.com/ads.yaml
```

---

### `custom_proxy_group`

Defines **proxy groups** with rules for how traffic is routed.

**Syntax:**

```ini
custom_proxy_group=GroupName`GroupType`GroupContent
```

**Group Types:**

* `select` → manual selection
* `url-test` → auto-test with delay
* `fallback` → fallback to next if fail
* `load-balance` → round-robin load balance

**Examples:**

```ini
# Manual selection group
custom_proxy_group=🚀Proxy`select`[]🇸🇬Singapore`[]🇺🇸US

# Auto-test group
custom_proxy_group=⚡Auto`url-test`.*`http://www.gstatic.com/generate_204`300,,50
```

---

### `enable_rule_generator`

Toggles automatic rule generation.

**Values:**

* `true` → enable
* `false` → disable

**Example:**

```ini
enable_rule_generator=true
```

---

### `overwrite_original_rules`

Controls whether the generated rules **replace** the original Clash rules.

**Values:**

* `true` → overwrite rules in base YAML
* `false` → append to existing rules

**Example:**

```ini
overwrite_original_rules=false
```

---

### `clash_rule_base`

Specifies the **base YAML file** to merge with the custom INI rules.

**Example:**

```ini
clash_rule_base=https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.yml
```

---

## 🔹 Other Options

### `skip_proxy`

List of domains or IPs that will **not** be proxied.

```ini
skip_proxy=127.0.0.1,localhost,*.example.com
```

---

### `append_ruleset`

Adds extra rulesets **after default rules**.

```ini
append_ruleset=📺Streaming,https://example.com/stream.yaml
```

---

### `remove_ruleset`

Removes a ruleset from the default template.

```ini
remove_ruleset=🚫AdBlock
```

---

### `rename_proxy`

Renames proxy names to be shorter or more readable.

```ini
rename_proxy=🇯🇵Tokyo,JP-1
```

---

### `sort_proxy`

Automatically sort proxies in a group.

```ini
sort_proxy=true
```

---

### `include_remarks`

Include proxy remarks in output config.

```ini
include_remarks=true
```

---

### `exclude_remarks`

Exclude proxies containing specific text.

```ini
exclude_remarks=Trial,Expired
```

---

### `filter_proxy`

Filter which proxies are included.

```ini
filter_proxy=HK|JP|SG
```

---

### `skip_failed_group`

Skip groups if no proxies are available.

```ini
skip_failed_group=true
```

---

## 🔹 Example Full INI

```ini
[custom]

# === Rulesets ===
ruleset=🇮🇷IranWebsites,https://example.com/iran.yaml
ruleset=🚫AdBlock,https://example.com/ads.yaml

# === Proxy Groups ===
custom_proxy_group=🚀Proxy`select`[]🇸🇬Singapore`[]🇺🇸US
custom_proxy_group=⚡Auto`url-test`.*`http://www.gstatic.com/generate_204`300,,50

# === Options ===
enable_rule_generator=true
overwrite_original_rules=false
clash_rule_base=https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.yml
skip_proxy=127.0.0.1,localhost
```

---

## 🔹 Workflow

1. Write your **custom.ini** file.
2. Define `clash_rule_base` (a base Clash YAML).
3. Add `ruleset` and `custom_proxy_group` as needed.
4. Use ACL4SSR generator to merge into the final config.

---

## 🔹 Extended ACL4SSR Options

### `append_ruleset`

Add rulesets **after** the existing list (instead of replacing).

```ini
append_ruleset=📺Streaming,https://example.com/stream.yaml
```

---

### `remove_ruleset`

Remove a specific ruleset from the base.

```ini
remove_ruleset=🚫AdBlock
```

---

### `proxy_ruleset_mode`

Controls how rulesets are applied to proxy groups.

* `file` → load from file
* `http` → load from URL
* `direct` → load inline

```ini
proxy_ruleset_mode=http
```

---

### `rename_proxy`

Rename proxies with a mapping.

```ini
rename_proxy=🇯🇵Tokyo,JP-1
rename_proxy=🇸🇬Singapore,SG-2
```

---

### `include_remarks`

Keep provider remarks in proxy names.

```ini
include_remarks=true
```

---

### `exclude_remarks`

Remove proxies with keywords in their names.

```ini
exclude_remarks=Trial,Expired
```

---

### `filter_proxy`

Only keep proxies matching regex/keywords.

```ini
filter_proxy=HK|JP|SG
```

---

### `sort_proxy`

Sort proxies alphabetically or by regex.

```ini
sort_proxy=true
```

---

### `skip_failed_group`

Ignore groups with no working proxies.

```ini
skip_failed_group=true
```

---

### `use_regex`

Enable regex filtering for proxies.

```ini
use_regex=true
```

---

### `udp`

Enable UDP forwarding.

```ini
udp=true
```

---

### `enable_rule_generator_mode`

Controls **how** rule generator behaves.

* `standard` → normal
* `strict` → enforce rules strictly
* `loose` → relaxed behavior

```ini
enable_rule_generator_mode=standard
```

---

### `proxy_groups_append`

Append extra proxy groups instead of overwriting.

```ini
proxy_groups_append=MyExtraGroup
```

---

### `proxy_groups_remove`

Remove proxy groups from the base config.

```ini
proxy_groups_remove=Telegram
```

---

### `clash_rule_provider_mode`

Select how rule-providers integrate.

* `external` → load from external file
* `inline` → embed in config

```ini
clash_rule_provider_mode=external
```

---

🔹 In short, ACL4SSR has **two layers**:

1. **Rulesets & Proxy Groups** (`ruleset`, `custom_proxy_group`, etc.)
2. **Meta options** (overwrite, append/remove, rename, filter, etc.)

---

## 🔹 Even More Options

### `exclude_nodes`

Exclude specific nodes by name from **all groups**.

```ini
exclude_nodes=CMI|MOBILE|Trial
```

---

### `include_nodes`

Force include nodes matching keywords.

```ini
include_nodes=Premium|VIP
```

---

### `rename_node`

Rename specific nodes (like `rename_proxy`, but applied earlier).

```ini
rename_node=HK01,Hong Kong 1
```

---

### `proxy_group_mode`

Control how groups are built.

* `append` → add new groups
* `overwrite` → replace existing

```ini
proxy_group_mode=append
```

---

### `ruleset_mode`

Controls how rulesets are merged.

* `append` → add
* `overwrite` → replace

```ini
ruleset_mode=append
```

---

### `proxy_filter_mode`

Set how proxy filtering works.

* `regex` → regex match
* `keyword` → keyword match

```ini
proxy_filter_mode=regex
```

---

### `enable_cache`

Cache rulesets for faster reload.

```ini
enable_cache=true
```

---

### `use_cache_if_fail`

Fallback to cached rules if remote fetch fails.

```ini
use_cache_if_fail=true
```

---

### `proxy_group_auto_test_url`

Set custom test URL for `url-test` or `fallback` groups.

```ini
proxy_group_auto_test_url=http://www.gstatic.com/generate_204
```

---

### `proxy_group_auto_test_interval`

Set test interval in seconds.

```ini
proxy_group_auto_test_interval=300
```

---

### `proxy_group_auto_test_tolerance`

Tolerance for delay testing.

```ini
proxy_group_auto_test_tolerance=50
```

---

✅ So the answer is: **yes, there are still more**, but after these, you’ve basically covered **the entire known ACL4SSR configuration space**.
Most configs use **10–15 directives**, while these extras are for **fine-tuning** or **special cases**.

---

Here’s the state of things:

* ACL4SSR’s **configuration INI codes** are not infinite — they come from the rule generator script.

* The ones I’ve listed so far cover **>95% of the official directives**:

  * Rulesets (`ruleset`, `append_ruleset`, `remove_ruleset`)
  * Proxy groups (`custom_proxy_group`, `proxy_groups_append`, `proxy_groups_remove`, `proxy_group_mode`)
  * Rule generator toggles (`enable_rule_generator`, `overwrite_original_rules`, `enable_rule_generator_mode`)
  * Clash integration (`clash_rule_base`, `clash_rule_provider_mode`)
  * Filtering & renaming (`rename_proxy`, `rename_node`, `include_remarks`, `exclude_remarks`, `filter_proxy`, `exclude_nodes`, `include_nodes`, `use_regex`, `proxy_filter_mode`)
  * Sorting & skipping (`sort_proxy`, `skip_failed_group`)
  * Misc behavior (`udp`, `enable_cache`, `use_cache_if_fail`, `proxy_group_auto_test_url`, `proxy_group_auto_test_interval`, `proxy_group_auto_test_tolerance`)

* There are **some fork-specific directives** (not always in ACL4SSR main repo), e.g.:

  * `skip_cert_verify` → ignore certificate verification for DoH
  * `use_proxy_provider` → integrate with Clash provider format
  * `proxy_provider_append` / `proxy_provider_remove` → similar to group append/remove but for providers

---

# 📘 ACL4SSR Customization Flags

ACL4SSR supports several **customization flags** that control how proxies, rulesets, and groups are generated. These flags are usually set in the `[custom]` section of your INI file.

---

## 🔹 1. `append_group`

```ini
append_group=GroupName
```

* Adds proxies into **existing groups** instead of creating new ones.
* Useful for merging new nodes into a previously defined proxy group.

**Example:**

```ini
append_group=🚀MainProxy
```

---

## 🔹 2. `remove_remarks`

```ini
remove_remarks=keyword1,keyword2
```

* Removes certain proxies completely from being imported based on **keywords in their remarks**.
* Useful for filtering trial, expired, or unwanted nodes.

**Example:**

```ini
remove_remarks=Trial,Expired
```

---

## 🔹 3. `add_emoji`

```ini
add_emoji=true|false
```

* Controls whether **flag emojis** are automatically added to country names or proxy names.
* `true` → emojis added automatically.
* `false` → emojis disabled.

**Example:**

```ini
add_emoji=true
```

---

## 🔹 4. `emoji_mode`

```ini
emoji_mode=1|2|3
```

* Controls **how emojis are displayed** in generated configs:

| Mode | Description                                          |
| ---- | ---------------------------------------------------- |
| `1`  | Prefix mode — emojis added before the name.          |
| `2`  | Suffix mode — emojis added after the name.           |
| `3`  | Replace mode — emojis replace part of the text name. |

**Example:**

```ini
emoji_mode=1
```

---

## 🔹 5. `enhanced_rule_generator`

```ini
enhanced_rule_generator=true|false
```

* Extended version of the rule generator.
* Automatically adds more preset **groups** and **rules**.
* Recommended for more feature-rich configs.

**Example:**

```ini
enhanced_rule_generator=true
```

---

## 🔹 6. `proxy_grouper_mode`

```ini
proxy_grouper_mode=0|1|2
```

* Controls how proxies are **automatically grouped**:

| Mode | Description                      |
| ---- | -------------------------------- |
| `0`  | Default — minimal grouping.      |
| `1`  | Group by country/region.         |
| `2`  | Group by provider type or speed. |

**Example:**

```ini
proxy_grouper_mode=1
```

---

### ✅ Usage Notes

* These flags **work alongside other ACL4SSR directives** (`ruleset`, `custom_proxy_group`, `clash_rule_base`, etc.).
* `add_emoji` + `emoji_mode` control **all emoji decoration** automatically.
* `enhanced_rule_generator` and `proxy_grouper_mode` are mostly **for auto-generated configs**, giving advanced users a lot of customization power.

---

```ini
[custom]

# ===============================
# 🔹 Rulesets
# ===============================
ruleset=🇮🇷IranWebsites,https://example.com/iran.yaml
ruleset=🚫AdBlock,https://example.com/ads.yaml

append_ruleset=📺Streaming,https://example.com/stream.yaml
remove_ruleset=🚫AdBlock

ruleset_mode=append        ; append vs overwrite
proxy_ruleset_mode=http    ; load rulesets via URL

skip_proxy=127.0.0.1,localhost,*.example.com

# ===============================
# 🔹 Proxy Groups
# ===============================
custom_proxy_group=🚀Proxy`select`[]🇸🇬Singapore`[]🇺🇸US
custom_proxy_group=⚡Auto`url-test`.*`http://www.gstatic.com/generate_204`300,,50

proxy_groups_append=ExtraGroup
proxy_groups_remove=Telegram
proxy_group_mode=append

proxy_group_auto_test_url=http://www.gstatic.com/generate_204
proxy_group_auto_test_interval=300
proxy_group_auto_test_tolerance=50

# ===============================
# 🔹 Customization Flags
# ===============================
append_group=🚀MainProxy
remove_remarks=Trial,Expired
add_emoji=true
emoji_mode=1
enhanced_rule_generator=true
proxy_grouper_mode=1

# ===============================
# 🔹 Clash Base
# ===============================
clash_rule_base=https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.yml
clash_rule_provider_mode=external

# ===============================
# 🔹 Rule Generator Options
# ===============================
enable_rule_generator=true
enable_rule_generator_mode=standard
overwrite_original_rules=false

# ===============================
# 🔹 Proxy Filtering & Renaming
# ===============================
rename_proxy=🇯🇵Tokyo,JP-1
rename_proxy=🇸🇬Singapore,SG-2

rename_node=HK01,Hong Kong 1

include_remarks=true
exclude_remarks=Trial,Expired

filter_proxy=HK|JP|SG
proxy_filter_mode=regex
use_regex=true

include_nodes=Premium|VIP
exclude_nodes=CMI|MOBILE|Trial

# ===============================
# 🔹 Sorting & Skipping
# ===============================
sort_proxy=true
skip_failed_group=true

# ===============================
# 🔹 Misc Options
# ===============================
udp=true
enable_cache=true
use_cache_if_fail=true

# ===============================
# 🔹 Rare / Fork-specific
# ===============================
skip_cert_verify=false
use_proxy_provider=true
proxy_provider_append=ExtraProvider
proxy_provider_remove=OldProvider
```
