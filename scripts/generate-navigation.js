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

if (!fs.existsSync(configPath)) {
  console.error(`❌ book-config.json が見つかりません: ${configPath}`);
  process.exit(1);
}

const config = readJson(configPath);
const chapters = config?.structure?.chapters ?? [];
const appendices = config?.structure?.appendices ?? [];

if (!Array.isArray(chapters) || !Array.isArray(appendices)) {
  console.error('❌ structure.chapters / structure.appendices は配列である必要があります');
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
  lines.push(`    path: ${yamlQuote(`/src/chapters/${id}/`)}`);
});

lines.push('');
lines.push('appendices:');
appendices.forEach((appendix, index) => {
  const id = String(appendix?.id ?? '').trim();
  const title = String(appendix?.title ?? '').trim();
  if (!id || !title) return;
  const label = appendixLabel(index);
  lines.push(`  - title: ${yamlQuote(`付録${label} ${title}`)}`);
  lines.push(`    path: ${yamlQuote(`/src/appendices/${id}/`)}`);
});

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, `${lines.join('\n')}\n`, 'utf8');
console.log(`✅ Wrote ${path.relative(repoRoot, outPath)}`);
