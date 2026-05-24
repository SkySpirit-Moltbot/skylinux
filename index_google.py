#!/usr/bin/env python3
"""SkyLinux - Indexation Google Search Console + Indexing API"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

TOKEN_FILE = os.path.expanduser('~/.openclaw/credentials/google-searchconsole-token.json')
SITE = 'https://skyspirit-moltbot.github.io/skylinux'
BASE = Path('/home/aselophe/linux-debutant')
DOCS = BASE / 'docs'

def get_access_token():
    with open(TOKEN_FILE) as f:
        cfg = json.load(f)
    
    data = urllib.parse.urlencode({
        'client_id': cfg['client_id'],
        'client_secret': cfg['client_secret'],
        'refresh_token': cfg['refresh_token'],
        'grant_type': 'refresh_token',
    }).encode()
    
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())['access_token']

def api_call(url, method='GET', body=None):
    token = get_access_token()
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def submit_sitemap():
    """Soumettre le sitemap à Google"""
    sitemap_url = f'{SITE}/sitemap.xml'
    site_enc = urllib.parse.quote(SITE + '/', safe='')
    sm_enc = urllib.parse.quote(sitemap_url, safe='')
    
    url = f'https://www.googleapis.com/webmasters/v3/sites/{site_enc}/sitemaps/{sm_enc}'
    code, body = api_call(url, method='PUT')
    
    if code in (200, 204):
        # Vérifier le statut
        check_url = f'https://www.googleapis.com/webmasters/v3/sites/{site_enc}/sitemaps'
        _, body = api_call(check_url)
        data = json.loads(body)
        for sm in data.get('sitemap', []):
            if sm['path'] == sitemap_url:
                print(f"✅ Sitemap: {sm.get('lastSubmitted','?')} | errors:{sm['errors']} warnings:{sm['warnings']} pending:{sm['isPending']}")
        return True
    else:
        print(f'❌ Sitemap error HTTP {code}: {body[:200]}')
        return False

def notify_urls(urls):
    """Notifier Google Indexing API pour des URLs spécifiques"""
    token = get_access_token()
    count = 0
    for url in urls:
        data = json.dumps({'url': url, 'type': 'URL_UPDATED'}).encode()
        req = urllib.request.Request(
            'https://indexing.googleapis.com/v3/urlNotifications:publish',
            data=data,
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status == 200:
                    count += 1
        except urllib.error.HTTPError:
            pass
    print(f'📤 {count}/{len(urls)} URLs notifiées à Google Indexing')

def index_all():
    """Indexer toutes les leçons"""
    # 1. Soumettre le sitemap
    print('🗺️  Sitemap...')
    submit_sitemap()
    
    # 2. Notifier les pages principales + accueil
    html_files = sorted(f for f in os.listdir(DOCS) if f.endswith('.html') and f[0].isdigit())
    urls = [f'{SITE}/', f'{SITE}/index.html']
    urls += [f'{SITE}/{f}' for f in html_files]
    
    print(f'\n📤 Notification de {len(urls)} URLs...')
    # Par lots de 20 pour éviter les rate limits
    batch_size = 20
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        notify_urls(batch)
    
    print(f'\n✅ Indexation terminée: {len(urls)} URLs')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'sitemap':
        submit_sitemap()
    else:
        index_all()
