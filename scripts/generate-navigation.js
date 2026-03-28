#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function yamlQuote(value) {
  const s = String(value ?? '');
  return `"${s.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

function appendixLabel(index) {
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if (index >= 0 && index < letters.length) return letters[index];
  return String(index + 1);
}

const repoRoot = process.cwd();
const configPath = path.join(repoRoot, 'book-config.json');
const outPath = path.join(repoRoot, '_data', 'navigation.yml');
const checkMode = process.argv.includes('--check');

if (!fs.existsSync(configPath)) {
  console.error(`❌ book-config.json が見つかりません: ${configPath}`);
  process.exit(1);
}

const config = readJson(configPath);
const chapters = config?.structure?.chapters ?? [];
const resources = config?.structure?.resources ?? [];
const appendices = config?.structure?.appendices ?? [];

if (!Array.isArray(chapters) || !Array.isArray(resources) || !Array.isArray(appendices)) {
  console.error('❌ structure.chapters / structure.resources / structure.appendices は配列である必要があります');
  process.exit(1);
}

const lines = [];
lines.push('# AUTO-GENERATED: scripts/generate-navigation.js');
lines.push('# - Sidebar + Previous/Next navigation');
lines.push('# - Edit book-config.json and re-run `npm run gen:navigation`');
lines.push('');

lines.push('chapters:');
chapters.forEach((chapter, index) => {
  const id = String(chapter?.id ?? '').trim();
  const title = String(chapter?.title ?? '').trim();
  if (!id || !title) return;
  lines.push(`  - title: ${yamlQuote(`第${index + 1}章 ${title}`)}`);
  lines.push(`    path: ${yamlQuote(`/chapters/${id}/`)}`);
});

lines.push('');
if (resources.length > 0) {
  lines.push('resources:');
  resources.forEach((resource) => {
    const id = String(resource?.id ?? '').trim();
    const title = String(resource?.title ?? '').trim();
    const resourcePath = String(resource?.path ?? `/${id}/`).trim();
    if (!id || !title) return;
    lines.push(`  - title: ${yamlQuote(title)}`);
    lines.push(`    path: ${yamlQuote(resourcePath)}`);
  });
}

lines.push('');
lines.push('appendices:');
appendices.forEach((appendix, index) => {
  const id = String(appendix?.id ?? '').trim();
  const title = String(appendix?.title ?? '').trim();
  if (!id || !title) return;
  const label = appendixLabel(index);
  lines.push(`  - title: ${yamlQuote(`付録${label} ${title}`)}`);
  lines.push(`    path: ${yamlQuote(`/appendices/${id}/`)}`);
});

const output = `${lines.join('\n')}\n`;
fs.mkdirSync(path.dirname(outPath), { recursive: true });
if (checkMode) {
  const current = fs.existsSync(outPath) ? fs.readFileSync(outPath, 'utf8') : '';
  if (current !== output) {
    console.error(`❌ navigation.yml is out of sync: ${path.relative(repoRoot, outPath)}`);
    process.exit(1);
  }
  console.log(`✅ navigation.yml is up to date: ${path.relative(repoRoot, outPath)}`);
  process.exit(0);
}
fs.writeFileSync(outPath, output, 'utf8');
console.log(`✅ Wrote ${path.relative(repoRoot, outPath)}`);
