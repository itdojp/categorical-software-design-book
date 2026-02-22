#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

function readText(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function pickScalar(yamlText, key) {
  const re = new RegExp(`^${key}:\\s*(.+?)\\s*$`, 'm');
  const m = yamlText.match(re);
  if (!m) return null;
  return m[1].replace(/^"(.*)"$/, '$1').replace(/^'(.*)'$/, '$1').trim();
}

function fail(message) {
  console.error(`❌ ${message}`);
  process.exitCode = 1;
}

const repoRoot = process.cwd();
const configPath = path.join(repoRoot, '_config.yml');

if (!fs.existsSync(configPath)) {
  fail(`_config.yml が見つかりません: ${configPath}`);
  process.exit(1);
}

const configText = readText(configPath);
const url = pickScalar(configText, 'url');
const baseurl = pickScalar(configText, 'baseurl');
const repository = pickScalar(configText, 'repository');
const repositoryBranch = pickScalar(configText, 'repository_branch');

if (!url) fail('`url:` が未設定です（GitHub Pages向け）');
if (!baseurl) fail('`baseurl:` が未設定です（Project Pages向け）');
if (!repository) fail('`repository:` が未設定です（Edit on GitHubリンク向け）');
if (!repositoryBranch) fail('`repository_branch:` が未設定です（Edit on GitHubリンク向け）');

const expectedBaseurl = '/categorical-software-design-book';
if (baseurl && baseurl !== expectedBaseurl) {
  fail(`baseurl が想定と異なります: ${baseurl}（期待値: ${expectedBaseurl}）`);
}

const bookLayout = path.join(repoRoot, '_layouts', 'book.html');
if (!fs.existsSync(bookLayout)) {
  fail(`_layouts/book.html が見つかりません: ${bookLayout}`);
}

if (process.exitCode === 1) {
  process.exit(1);
}

const pagesUrl = `${url}${baseurl.endsWith('/') ? baseurl : `${baseurl}/`}`;
console.log('✅ GitHub Pages設定の最低限チェックに成功しました');
console.log(`- Pages URL（想定）: ${pagesUrl}`);
console.log('- 設定: Settings > Pages > Deploy from a branch > main / (root)');
