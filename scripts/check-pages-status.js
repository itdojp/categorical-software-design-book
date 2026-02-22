#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const configPath = path.join(process.cwd(), '_config.yml');
const configText = fs.existsSync(configPath) ? fs.readFileSync(configPath, 'utf8') : '';

function pickScalar(key) {
  const re = new RegExp(`^${key}:\\s*(.+?)\\s*$`, 'm');
  const m = configText.match(re);
  if (!m) return null;
  return m[1].replace(/^"(.*)"$/, '$1').replace(/^'(.*)'$/, '$1').trim();
}

const url = pickScalar('url') || 'https://<owner>.github.io';
const baseurl = pickScalar('baseurl') || '/<repo>';

const pagesUrl = `${url}${baseurl.endsWith('/') ? baseurl : `${baseurl}/`}`;

console.log('GitHub Pages はリポジトリ設定とデプロイ状況に依存するため、本スクリプトはネットワーク照会を行いません。');
console.log(`- 公開URL（想定）: ${pagesUrl}`);
console.log('- 確認手順: Settings > Pages で Source/Branch/Folder を確認してください。');
