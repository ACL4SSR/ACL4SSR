
---

# 📖 Ruleset README – Adblock Example

## 🔹 What is this ruleset?

This ruleset is a **Clash/ACL4SSR compatible YAML fragment** designed to block ads.
It contains **payload rules** such as `DOMAIN-KEYWORD` entries that match common ad services (e.g. `admarvel`, `admaster`).

* ✅ Lightweight – only includes known advertising domains/keywords
* ✅ Safe – no false positives for normal browsing
* ✅ Compatible – can be directly used with Clash and ACL4SSR

Example snippet:

```yaml
# 本碎片只包含常见广告关键字、广告联盟。无副作用，放心使用
payload:

# 广告关键词
  - DOMAIN-KEYWORD,admarvel
  - DOMAIN-KEYWORD,admaster
```

---

## 🔹 How it works

* `payload` is the container for rules.
* Each rule line defines a **match pattern**:

  * `DOMAIN-KEYWORD,xxx` → matches any domain containing `xxx`.
* When traffic matches, it will be handled by the **rule target** you assign in your Clash config (usually an `ADBlock` or `REJECT` group).

---

## 🔹 How to use with ACL4SSR

### 1. Add the ruleset to your config

In your ACL4SSR `.ini` or custom config, reference this file:

```ini
[custom]
ruleset=🚫AdBlock,https://your-repo/raw/branch/ruleset/adblock.yaml
```

### 2. Define a Proxy Group for Ads

In your Clash config or ACL4SSR custom file, create a group for ads:

```ini
custom_proxy_group=🚫AdBlock`select`[]REJECT`[]DIRECT
```

* `REJECT` → blocks requests (recommended for ads)
* `DIRECT` → lets them through (use only for troubleshooting)

### 3. Rule application order

Clash/ACL4SSR processes rules **from top to bottom**.
Place AdBlock rules **before GEOIP/Final rules** to ensure they are matched first.

---

## 🔹 Example usage in ACL4SSR

```ini
[custom]

; === Rulesets ===
ruleset=🚫AdBlock,https://your-repo/raw/branch/ruleset/adblock.yaml
ruleset=🌍Global,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyGFWlist.yaml

; === Groups ===
custom_proxy_group=🚫AdBlock`select`[]REJECT`[]DIRECT
custom_proxy_group=🌍Global`select`[]🇭🇰HongKong`[]🇸🇬Singapore`[]🇺🇸United States
```

---

## 🔹 Notes

* Always keep rulesets updated for the latest ad domains.
* This fragment is **modular** – you can combine it with other ACL4SSR rulesets like China sites, global sites, trackers, etc.
* Default behavior is to **REJECT ads** for better browsing experience.

---

👉 In short:

1. Add ruleset → 2. Assign group (usually REJECT) → 3. Enjoy ad-free browsing 🚫

---

# 📖 Using with Rule-Provider Method in ACL4SSR

## 🔹 What is `rule-providers`?

Instead of embedding rules directly with `ruleset=...` (old ACL4SSR `.ini` style), Clash Meta supports **`rule-providers`**.

* Rule providers fetch YAML rulesets from a URL and keep them **updated automatically**.
* In your main config, you only reference them with `RULE-SET`.

This is now the **recommended** way to integrate modular rulesets like ads, trackers, Iran, etc.

---

## 🔹 Example Rule-Provider Definition

Add this under your `rule-providers:` section:

```yaml
rule-providers:
  ads:
    type: http
    behavior: domain
    format: yaml
    path: ./ruleset/ads.yaml
    url: "https://your-repo/raw/branch/ruleset/adblock.yaml"
    interval: 86400
```

* `type: http` → downloaded from remote
* `behavior: domain` → because this file contains `DOMAIN-KEYWORD` rules
* `path` → local cache filename
* `interval` → update every 24 hours

---

## 🔹 Example Rules Section

Now reference it in the `rules:` section of Clash:

```yaml
rules:
  - RULE-SET,ads,🚫AdBlock
  - GEOIP,CN,🇨🇳Direct
  - MATCH,🌍Proxy
```

This means:

* Any domain that matches your ad keywords will be sent to the `🚫AdBlock` proxy group.
* The rest follow normal rules (e.g., China → direct, global → proxy).

---

## 🔹 Example Proxy Group

Define the group used by ads:

```yaml
proxy-groups:
  - name: 🚫AdBlock
    type: select
    proxies:
      - REJECT
      - DIRECT
```

* Default: `REJECT` (ads blocked)
* Optionally switch to `DIRECT` if you want to test

---

## 🔹 Full Minimal Example

```yaml
rule-providers:
  ads:
    type: http
    behavior: domain
    format: yaml
    path: ./ruleset/ads.yaml
    url: "https://your-repo/raw/branch/ruleset/adblock.yaml"
    interval: 86400

proxy-groups:
  - name: 🚫AdBlock
    type: select
    proxies:
      - REJECT
      - DIRECT

rules:
  - RULE-SET,ads,🚫AdBlock
  - GEOIP,CN,DIRECT
  - MATCH,🌍Proxy
```

---

## 🔹 Notes

* **ACL4SSR already has many rule-providers** (China, Global, Ads, Trackers, etc). You can just add your own provider alongside theirs.
* Use `behavior: classical` only if your file contains mixed rules (e.g. `DOMAIN-SUFFIX`, `IP-CIDR`).
* With ACL4SSR’s auto-update configs, your ruleset will update daily without manual changes.

---

👉 TL;DR:
Put your `adblock.yaml` inside `rule-providers`, reference it with `RULE-SET` in `rules:`, and map it to an `🚫AdBlock` group.

---

# 📖 ACL4SSR with Rule-Providers – Template

## 🔹 1. Rule-Providers Section

This is where you define your rulesets. ACL4SSR already provides many, but here’s how you add your own **AdBlock provider** alongside them:

```yaml
rule-providers:
  # --- Custom Adblock Ruleset ---
  ads:
    type: http
    behavior: domain
    format: yaml
    path: ./ruleset/ads.yaml
    url: "https://your-repo/raw/branch/ruleset/adblock.yaml"
    interval: 86400

  # --- Example ACL4SSR Providers ---
  china:
    type: http
    behavior: domain
    format: yaml
    path: ./ruleset/china.yaml
    url: "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.yaml"
    interval: 86400

  gfw:
    type: http
    behavior: domain
    format: yaml
    path: ./ruleset/gfw.yaml
    url: "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyGFWlist.yaml"
    interval: 86400
```

---

## 🔹 2. Proxy Groups Section

Define which group handles ads, China, and global traffic.

```yaml
proxy-groups:
  - name: 🚫AdBlock
    type: select
    proxies:
      - REJECT
      - DIRECT

  - name: 🇨🇳China
    type: select
    proxies:
      - DIRECT
      - 🌍Proxy

  - name: 🌍Proxy
    type: select
    proxies:
      - 🇭🇰HongKong
      - 🇸🇬Singapore
      - 🇺🇸United States
      - DIRECT
```

*(You can adjust your actual proxy names here — ACL4SSR usually fills them dynamically.)*

---

## 🔹 3. Rules Section

Now wire the providers into your routing rules:

```yaml
rules:
  - RULE-SET,ads,🚫AdBlock
  - RULE-SET,china,🇨🇳China
  - RULE-SET,gfw,🌍Proxy
  - GEOIP,CN,🇨🇳China
  - MATCH,🌍Proxy
```

* Ads → 🚫AdBlock (REJECT by default)
* China domains → 🇨🇳China group
* GFW sites → 🌍Proxy
* China IPs → direct
* Everything else → 🌍Proxy

---

## 🔹 4. Summary

* ✅ Uses **rule-providers** for modular rulesets
* ✅ Keeps rules updated automatically
* ✅ Works with your **custom adblock.yaml** and ACL4SSR defaults
* ✅ Cleaner than the old `.ini` `ruleset=` method

---

# 🔗 Using `clash_rule_base=` to Connect INI + YAML

## 🔹 What it does

* In ACL4SSR `.ini`, `clash_rule_base=` tells the generator which **base YAML file** to use.
* The generator loads that YAML as the foundation, then **inserts your `ruleset=` and `custom_proxy_group=` definitions** into it.

So:

* `base.yml` = has ports, DNS, logging, basic structure.
* `custom.ini` = your rulesets, proxy groups.
* `clash_rule_base=` = points `custom.ini` → `base.yml`.
* Final = full Clash config YAML with both combined.

---

## 🔹 Example `custom.ini`

```ini
[custom]

; ===============================
; 🔹 Link to base YAML
; ===============================
clash_rule_base=https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.yml

; ===============================
; 🔹 Rulesets
; ===============================
ruleset=🚫AdBlock,https://your-repo/raw/branch/ruleset/adblock.yaml
ruleset=🇨🇳China,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ChinaDomain.yaml
ruleset=🌍Proxy,https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/ProxyGFWlist.yaml

; ===============================
; 🔹 Proxy Groups
; ===============================
custom_proxy_group=🚫AdBlock`select`[]REJECT`[]DIRECT
custom_proxy_group=🇨🇳China`select`[]DIRECT`[]🌍Proxy
custom_proxy_group=🌍Proxy`select`[]🇭🇰HongKong`[]🇸🇬Singapore`[]🇺🇸United States`[]DIRECT
```

---

## 🔹 What happens

When you run ACL4SSR (online generator or FlClash):

1. It fetches `ACL4SSR_Online_Full.yml` (the base).
2. It inserts your `ruleset=` as **rule-providers**.
3. It inserts your `custom_proxy_group=` as **proxy-groups**.
4. It generates the `rules:` section with `RULE-SET` references.

So your final `config.yaml` will look like:

```yaml
rule-providers:
  ads:
    type: http
    behavior: domain
    url: "https://your-repo/raw/branch/ruleset/adblock.yaml"
    path: ./ruleset/ads.yaml
    interval: 86400
  china:
    ...
  gfw:
    ...

proxy-groups:
  - name: 🚫AdBlock
    type: select
    proxies:
      - REJECT
      - DIRECT
  - name: 🇨🇳China
    type: select
    proxies:
      - DIRECT
      - 🌍Proxy
  - name: 🌍Proxy
    type: select
    proxies:
      - 🇭🇰HongKong
      - 🇸🇬Singapore
      - 🇺🇸United States
      - DIRECT

rules:
  - RULE-SET,ads,🚫AdBlock
  - RULE-SET,china,🇨🇳China
  - RULE-SET,gfw,🌍Proxy
  - GEOIP,CN,🇨🇳China
  - MATCH,🌍Proxy
```

---

## 🔹 Summary

* `clash_rule_base=` = tells `.ini` which YAML base to use.
* `.ini` only defines rulesets + proxy groups.
* Generator merges them → produces final Clash config YAML.

---

