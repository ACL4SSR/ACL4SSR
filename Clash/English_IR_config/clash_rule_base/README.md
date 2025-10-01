# ⚡ Clash Rule Base (INI + YAML Method)

This repository provides a **flexible Clash rule base** that differs from the traditional **ACL4SSR** setup.  
Instead of a single large YAML with static rules, this method uses:

1. **One `.ini` file** → Defines **rulesets** and **proxy group structure** (human-friendly, modular).  
2. **One `.yaml` file** → Holds Clash **core configurations** and **rule-providers** (external lists of domains/IPs).  

Together, these files let you **generate a fully customized Clash config** that is easy to extend, share, and maintain.

---

## 🔹 How It Differs from ACL4SSR

- **ACL4SSR**:  
  - Ships a huge, prebuilt YAML with rules and groups already merged.  
  - Harder to modify or maintain if you only want to adjust one category.  

- **This Rule Base**:  
  - **Separation of logic and structure**:  
    - `.ini` = rulesets + groups (what traffic goes where).  
    - `.yaml` = core Clash settings + rule-providers (where to fetch rules from).  
  - **Rule-providers** automatically pull and update external lists (domains, ads, trackers, apps).  
  - Anyone can plug in their own rulesets without editing giant YAMLs.  
  - Much more modular, extensible, and easy to debug.

---

## 🔹 File Structure

### 1. `custom_rules.ini`
Defines:
- Rulesets (which categories of domains/IPs map to which groups).
- Proxy groups (Destinations, Proxies, LAN, Ads, Security, Apps, etc.).
- Hierarchical traffic flow (everything starts from `⚡Online`).

Example:
```ini
[custom]

; Iran websites
ruleset=🇮🇷IranWebsites,[]GEOIP,IR
ruleset=🇮🇷IranWebsites,[]GEOSITE,category-ir
ruleset=🇮🇷IranWebsites,[]RULE-SET,iran

; Ads & Trackers
ruleset=🛑Advertisements,[]RULE-SET,BanAD
ruleset=🛡️PrivacyTrackers,[]RULE-SET,BanEasyPrivacy

; Destination apps
ruleset=📺YouTube🎯,[]RULE-SET,youtube
ruleset=🔵Telegram🎯,[]RULE-SET,telegram

; Final fallback
ruleset=⚡Online,[]FINAL
````

### 2. `EN-IR-COUNTRY2.yml`

Contains:

* Core Clash/Mihomo settings (ports, DNS, tun, sniffer, etc.).
* Rule-providers with external sources (`ads.yaml`, `category-ai.yaml`, `BanAD.yaml`, etc.).
* DNS filtering, fake-ip, system integration.

Example:

```yaml
rule-providers:
  BanAD:
    type: http
    behavior: domain
    url: https://raw.githubusercontent.com/10ium/mihomo_rule/main/list/BanAD.yaml
    path: ./ruleset/BanAD.yaml
    interval: 86400
```

---

## 🔹 How It Works

1. **Clash loads the YAML (`EN-IR-COUNTRY2.yml`)**

   * Core config + rule-providers.
   * Downloads domain/IP lists automatically on interval.

2. **The `.ini` file (`custom_rules.ini`) tells the rule generator**

   * Which rulesets to map to which groups.
   * How to organize proxy selections.

3. **Final generated Clash config**

   * Is a clean YAML with modular rules + groups.
   * All traffic flows through the top-level group `⚡Online`.

---

## 🔹 Why Use This Method?

* ✅ Easier to maintain than editing ACL4SSR’s giant YAML.
* ✅ Modular: swap/add your own rulesets without breaking other parts.
* ✅ Auto-updating via `rule-providers`.
* ✅ Flexible: build country-based configs, service-based configs, or minimal configs.
* ✅ Human-friendly group names and emojis.

---

## 🔹 Usage

1. Copy both files:

   * `custom_rules.ini`
   * `EN-IR-COUNTRY2.yml`

2. In Clash/FlClash/MetaClash settings, **set your rule base**:

   ```ini
   clash_rule_base=https://raw.githubusercontent.com/<your-repo>/<branch>/EN-IR-COUNTRY2.yml
   ```

3. Load your `.ini` file as **custom rules**.

4. Reload Clash → it will generate your config using:

   * `.ini` = rules/group structure
   * `.yaml` = settings + rule-providers

---

## 🔹 Make Your Own

1. Create a new `.ini` file:

   * Define your own **rulesets** and **proxy groups**.

2. Add your rule-providers in the `.yaml` file:

   ```yaml
   my_custom_rules:
     type: http
     behavior: domain
     url: https://example.com/mylist.yaml
     path: ./ruleset/mylist.yaml
     interval: 86400
   ```

3. Reference them in `.ini`:

   ```ini
   ruleset=🆕MyRules,[]RULE-SET,my_custom_rules
   ```

That’s it — Clash will build your config with your own logic.

---

## 🔹 Example Flow

```
Traffic (Internet) → ⚡Online
   ├── 🌐Proxy → Manual / Auto-test / Countries
   ├── 🔓Direct → Skip proxy
   ├── 🚫Block → Drop traffic
   └── 🎯Destinations → Apps & Services
         ├── YouTube
         ├── Telegram
         ├── OpenAI
         ├── Steam
         └── etc.
```

---

## 🔹 Credits

* Based on **Clash.Meta** and **FlClash** rule generator system.
* Inspired by **ACL4SSR**, but refactored into modular `.ini + .yaml` structure.
* External rule-providers from community sources (Chocolate4U, 10ium, ACL, Mihomo, etc.).

---

```

In Clash.Meta, a **`rule-providers`** block defines how external rule lists (YAML files) are fetched and used.
The important field here is **`behavior`**, which tells Clash how to interpret the contents of the rule file.

There are **3 main behavior types** (plus a special case):

---

### 🔹 1. `domain`

* The ruleset contains **domain-based rules**.
* Each entry is interpreted as a `DOMAIN`, `DOMAIN-SUFFIX`, or `DOMAIN-KEYWORD`.
* Example:

  ```yaml
  behavior: domain
  ```

  Input file could look like:

  ```yaml
  payload:
    - "google.com"
    - "+.facebook.com"
    - "youtube"
  ```

---

### 🔹 2. `ipcidr`

* The ruleset contains **IP ranges** in CIDR format.
* Used for blocking/redirecting specific IP networks.
* Example:

  ```yaml
  behavior: ipcidr
  ```

  Input file could look like:

  ```yaml
  payload:
    - "8.8.8.8/32"
    - "1.1.1.0/24"
    - "203.0.113.0/16"
  ```

---

### 🔹 3. `classical`

* The ruleset contains **full Clash rules** (same as writing them manually in `rules:`).
* Supports all Clash rule types (`DOMAIN-SUFFIX`, `GEOIP`, `IP-CIDR`, `PROCESS-NAME`, etc.).
* Example:

  ```yaml
  behavior: classical
  ```

  Input file could look like:

  ```yaml
  payload:
    - "DOMAIN-SUFFIX,google.com"
    - "DOMAIN,example.com"
    - "IP-CIDR,192.168.0.0/16"
    - "GEOIP,CN"
  ```

---

### 🔹 4. (Special case) `classical` + `external-rule` (in `mihomo`)

* Some forks (like Mihomo) allow `rule-providers` to hold **mixed or advanced rules** beyond the built-in Clash types.
* Mostly used for compatibility with **Loyalsoldier** / **v2ray-rules-dat** style lists.

---

✅ So in your snippet:

```yaml
behavior: domain
```

means the downloaded file contains **domain-based rules only**.

---

