import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
install_sh = (root / 'install.sh').read_text(encoding='utf-8')
install_ps1 = (root / 'install.ps1').read_text(encoding='utf-8')

failures = []

# install.sh: keep v0.1.11 shape and expose upload api parameters
if '--domains-api-url URL' in install_sh:
    failures.append('install.sh still exposes --domains-api-url')
if '"enabled_email_domains":' in install_sh or '"mail_domain_options":' in install_sh:
    failures.append('install.sh still writes domains lists into web_config.json')
if '--upload-api-url URL' not in install_sh:
    failures.append('install.sh is missing --upload-api-url flag')
if '--upload-api-token TOKEN' not in install_sh:
    failures.append('install.sh is missing --upload-api-token flag')
if '"upload_api_url": "$(json_escape "$UPLOAD_API_URL")"' not in install_sh:
    failures.append('install.sh does not write upload_api_url from UPLOAD_API_URL')
if '"upload_api_token": "$(json_escape "$UPLOAD_API_TOKEN")"' not in install_sh:
    failures.append('install.sh does not write upload_api_token from UPLOAD_API_TOKEN')
if '"upload_api_url": "https://example.com/v0/management/auth-files"' in install_sh:
    failures.append('install.sh still hardcodes upload_api_url placeholder')
if '"upload_api_token": "replace-me"' in install_sh:
    failures.append('install.sh still hardcodes upload_api_token placeholder')
if '"runtime_logs": false' not in install_sh:
    failures.append('install.sh lost upstream runtime_logs field')

# install.ps1: keep v0.1.11 shape and expose upload api parameters
if '[string]$DomainsApiUrl' in install_ps1:
    failures.append('install.ps1 still exposes DomainsApiUrl')
if 'enabled_email_domains = $domains' in install_ps1 or 'mail_domain_options = $domains' in install_ps1:
    failures.append('install.ps1 still writes domains lists into web_config.json')
if '[string]$UploadApiUrl' not in install_ps1:
    failures.append('install.ps1 is missing UploadApiUrl parameter')
if '[string]$UploadApiToken' not in install_ps1:
    failures.append('install.ps1 is missing UploadApiToken parameter')
if "upload_api_url = $UploadApiUrl" not in install_ps1:
    failures.append('install.ps1 does not write upload_api_url from UploadApiUrl')
if "upload_api_token = $UploadApiToken" not in install_ps1:
    failures.append('install.ps1 does not write upload_api_token from UploadApiToken')
if "upload_api_url = 'https://example.com/v0/management/auth-files'" in install_ps1:
    failures.append('install.ps1 still hardcodes upload_api_url placeholder')
if "upload_api_token = 'replace-me'" in install_ps1:
    failures.append('install.ps1 still hardcodes upload_api_token placeholder')
if "'otp-retry-count' = 10" not in install_ps1:
    failures.append('install.ps1 lost upstream otp retry field names')

if failures:
    for item in failures:
        print(f'FAIL: {item}')
    sys.exit(1)

print('PASS: installer keeps v0.1.11 schema and upload api stays parameter-driven')
