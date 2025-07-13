# 🚫 SSR Ad-Blocking Rules / GFWList Rules / Clash Rule Fragments

> **Project License**: Released under the [CC-BY-SA-4.0 License](https://creativecommons.org/licenses/by-sa/4.0/deed.en)
> ![CC-BY-SA-4.0](https://licensebuttons.net/l/by-sa/4.0/88x31.png)

> 📱 **Recommended Usage**: Optimized for non-rooted Android devices.

> 📢 **Telegram Channel**: [https://t.me/ACL4SSR](https://t.me/ACL4SSR)

> 🌐 [Understanding the Internet in China](https://github.com/ACL4SSR/ACL4SSR/wiki/关于中国的互联网)

---

## 📱 Android SSR Ad-Blocking ACL Rules

These ACL rules are specifically designed to block ads and enhance privacy on Android devices using SSR (ShadowsocksR):

* Block ads from Xiaomi and Meizu Flyme ROM systems.
* Direct connection for all domestic (Chinese) websites.
* Block ads from popular Chinese video platforms.
* Block ads from major websites and streaming platforms.
* Block splash screen ads from certain apps.
* Prevent pop-up floating ads from ISP hijacks and network monitoring scripts.
* Block privacy tracking, behavioral analytics, and data collection from common apps.

---

## 📌 SSR Rules Overview

| Rule File                                                                                           | Default Routing | Ad-Blocking | LAN Access | China IPs     | China Domains       | International Access                    |
| --------------------------------------------------------------------------------------------------- | --------------- | ----------- | ---------- | ------------- | ------------------- | --------------------------------------- |
| [banAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Acl/banAD.acl)                 | Proxy           | ✅ Yes       | Direct     | ✅ Yes         | ✅ Common CN domains | Proxy + enhanced foreign domain support |
| [onlybanAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Acl/onlybanAD.acl)         | Proxy           | ✅ Yes       | Direct     | ❌ No          | ❌ No                | Proxy + enhanced foreign domain support |
| [nobanAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Acl/nobanAD.acl)             | Proxy           | ❌ No        | Direct     | ✅ Yes         | ✅ Common CN domains | Global proxy                            |
| [backcn-banAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Acl/backcn-banAD.acl)   | Proxy           | ✅ Yes       | Direct     | Proxy (China) | ❌ No                | Direct using GFWList                    |
| [gfwlist-banAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Acl/gfwlist-banAD.acl) | Direct          | ✅ Yes       | Direct     | ❌ No          | ❌ No                | Proxy using GFWList                     |
| [fullgfwlist.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Acl/fullgfwlist.acl)     | Direct          | ❌ No        | Direct     | ❌ No          | ❌ No                | Proxy using GFWList                     |
| [gfwlist-user.rule](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Acl/gfwlist-user.rule) | Direct          | ✅ Yes       | Direct     | ❌ No          | ❌ No                | Proxy using GFWList                     |

---

## 🔄 Rule Converters for Clash, Quantumult, Surge, Surfboard, Trojan

This project supports self-hosted, open-source conversion from SSR/SS rules to formats supported by modern clients.

### 🧩 Components:

* **Frontend:** [`sub-web`](https://github.com/CareyWang/sub-web)
* **Backend:** [`subconverter`](https://github.com/tindy2013/subconverter/blob/master/README-cn.md)

### ✅ Supported Protocol Types

| Format                  | Source | Target | Parameter Example    |
| ----------------------- | :----: | :----: | -------------------- |
| Clash                   |    ✅   |    ✅   | `clash`              |
| ClashR                  |    ✅   |    ✅   | `clashr`             |
| Quantumult (Full)       |    ✅   |    ✅   | `quan`               |
| Quantumult X (Full)     |    ✅   |    ✅   | `quanx`              |
| Loon                    |    ✅   |    ✅   | `loon`               |
| Mellow                  |    ✅   |    ✅   | `mellow`             |
| Shadowsocks SIP002      |    ✅   |    ✅   | `ss`                 |
| Shadowsocks (app sub)   |    ✅   |    ✅   | `sssub`              |
| SSD                     |    ✅   |    ✅   | `ssd`                |
| ShadowsocksR (SSR)      |    ✅   |    ✅   | `ssr`                |
| Surfboard               |    ✅   |    ✅   | `surfboard`          |
| Surge 2                 |    ✅   |    ✅   | `surge&ver=2`        |
| Surge 3                 |    ✅   |    ✅   | `surge&ver=3`        |
| Surge 4                 |    ✅   |    ✅   | `surge&ver=4`        |
| Trojan                  |    ✅   |    ✅   | `trojan`             |
| V2Ray                   |    ✅   |    ✅   | `v2ray`              |
| TG-like HTTP/Socks URLs |    ✅   |    ❌   | Use via `&url=` only |

---

## 📚 Clash Rule Fragments

Located in the `clash/` directory, these are modular rule lists meant to be combined using tools like `subconverter`.

> For usage instructions, consult your proxy client’s documentation or refer to [subconverter config examples](https://github.com/tindy2013/subconverter/blob/master/README-cn.md#外部配置).

| File Name                | Type                | Description                                                                     |
| ------------------------ | ------------------- | ------------------------------------------------------------------------------- |
| `BanAD.list`             | Ad-blocking         | Basic ad keywords and networks, minimal side effects.                           |
| `BanProgramAD.list`      | App Ad-blocking     | Advanced app ad-blocking, may slightly affect app functionality.                |
| `BanEasyListChina.list`  | Ad-blocking         | All ad-blocking domains from EasyList China (AdblockPlus).                      |
| `LocalAreaNetwork.list`  | Direct              | Local network and router-related domains.                                       |
| `ChinaDomain.list`       | Direct              | Extensive list of domestic domains and CDNs.                                    |
| `ChinaCompanyIp.list`    | Direct              | IP ranges of major Chinese companies and cloud providers (e.g., Alibaba Cloud). |
| `ChinaIp.list`           | Direct              | Domestic IP ranges based on IPIP.net (more accurate than GeoIP).                |
| `Download.list`          | Direct              | Domains used for file downloads.                                                |
| `Apple.list`             | Neutral             | All Apple-related domains.                                                      |
| `Microsoft.list`         | Neutral             | All Microsoft domains.                                                          |
| `OneDrive.list`          | Neutral             | Domains related to OneDrive.                                                    |
| `GoogleCN.list`          | Direct              | Google services accessible in China.                                            |
| `Telegram.list`          | Proxy               | All Telegram-related domains.                                                   |
| `Netflix.list`           | Proxy               | All Netflix-related domains.                                                    |
| `ProxyGFWlist.list`      | Proxy               | Full GFW list of blocked domains.                                               |
| `ProxyLite.list`         | Proxy               | Lightweight proxy list (frequently used + polluted domains).                    |
| `GeneralClashConfig.yml` | Clash config        | Comprehensive Clash configuration with Chinese comments.                        |
| `pref.ini`               | Subconverter config | Basic configuration to convert rules into ACL4SSR style.                        |

---

## 🔗 SS/SSR ACL File Download Links

| Type                               | Link                                                                                            |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| Whitelist (with Ad-Block)          | [banAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/banAD.acl)                 |
| Blacklist (GFWList)                | [gfwlist-banAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/gfwlist-banAD.acl) |
| Global                             | [onlybanAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/onlybanAD.acl)         |
| GFWList Only (Official SS Support) | [fullgfwlist.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/fullgfwlist.acl)     |
| Domestic Proxy                     | [backcn-banAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/backcn-banAD.acl)   |
| Whitelist (No Ad-Block)            | [nobanAD.acl](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/nobanAD.acl)             |
| SSR C# GFWList (user.rule)         | [gfwlist-user.rule](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/gfwlist-user.rule) |

---

## 📱 Rooted Android Device Recommendations

1. **VIA Browser (Built-in Ad-blocker)**: [Download](http://www.coolapk.com/apk/mark.via)
2. **HOSTS AdAway China Version**: [Download](http://www.coolapk.com/apk/mark.via)
3. **AdAway (Open-source Ad Blocker)**: [Download](http://www.coolapk.com/apk/org.adaway)
4. **NeoHosts Project**: [https://github.com/neko-dev/neohosts](https://github.com/neko-dev/neohosts)
5. **Google Hosts**: [https://github.com/googlehosts/hosts](https://github.com/googlehosts/hosts)

---

## ⚠️ Notes

* Due to the complexity of in-app advertisements (especially in browsers), not all ads may be blocked. Some may slip through.
* If you encounter issues, please [submit an issue](https://github.com/ACL4SSR/ACL4SSR/issues) with details and the rule used.

---

## 📄 License

[![CC-BY-SA-4.0](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-sa/4.0/deed.en)
This project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).
