import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[1]
install_sh = (root / 'install.sh').read_text(encoding='utf-8')
install_ps1 = (root / 'install.ps1').read_text(encoding='utf-8')

failures = []

# install.sh: default domains resolver must ignore CPA_BASE_URL and prefer explicit DOMAINS_API_URL
if 'base="$(trim "${CPA_BASE_URL:-}")"' in install_sh:
    failures.append('install.sh still reads CPA_BASE_URL inside resolve_domains_api_url')
if 'printf \'%s/v0/management/domains\' "$base"' in install_sh or 'printf \'%s/domains\' "$base"' in install_sh:
    failures.append('install.sh still derives domains url from CPA_BASE_URL')
if not re.search(r'resolve_domains_api_url\(\) \{[\s\S]*?explicit="\$\(trim "\$\{DOMAINS_API_URL:-\}"\)"[\s\S]*?printf \'%s\' "\$DEFAULT_DOMAINS_API_URL"', install_sh):
    failures.append('install.sh resolve_domains_api_url does not clearly prefer explicit override then default fallback')

# install.ps1: should expose DomainsApiUrl param and ignore CpaBaseUrl for domain resolution
if '[string]$DomainsApiUrl' not in install_ps1:
    failures.append('install.ps1 is missing DomainsApiUrl parameter')
if re.search(r'function Resolve-DomainsApiUrl\s*\{[\s\S]*\$BaseUrl', install_ps1):
    failures.append('install.ps1 Resolve-DomainsApiUrl still accepts BaseUrl-based resolution')
if '$domainsApiUrl = Resolve-DomainsApiUrl $CpaBaseUrl' in install_ps1:
    failures.append('install.ps1 still resolves domains url from CpaBaseUrl')
if not re.search(r'function Resolve-DomainsApiUrl\s*\{[\s\S]*param\(\[string\]\$ExplicitUrl\)[\s\S]*return \$defaultDomainsApiUrl', install_ps1):
    failures.append('install.ps1 Resolve-DomainsApiUrl does not clearly prefer explicit override then default fallback')

if failures:
    for item in failures:
        print(f'FAIL: {item}')
    sys.exit(1)

print('PASS: domains api resolution matches the fixed design')
