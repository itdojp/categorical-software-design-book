#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const CHAPTER = 'chapters/chapter02/index.md';

const REQUIRED = [
  ['結合律を括弧の付け替えとして説明していること', '括弧の付け替え（再結合）'],
  [
    '有効な再結合の等式があること',
    '(authorizePayment ∘ reserveInventory) ∘ validate = authorizePayment ∘ (reserveInventory ∘ validate)',
  ],
  ['射の順序交換が一般にはできないと明記していること', '射の順序交換は一般にはできない'],
  ['順序交換した合成が型として未定義であること', 'そもそも定義できない'],
  ['型制約を失った実装境界と副作用の反例を分離していること', '型制約を失った実装境界'],
  ['副作用を持つ反例に在庫確保前の決済があること', '在庫を確保できない注文へ決済する'],
  ['副作用を持つ反例に監査記録があること', '監査記録も変わり'],
];

const FORBIDDEN = [
  [
    '結合律による合成順序の入替を許す旧表現',
    /結合律が成立(?:していれ|すれ)ば、?\s*2つの合成順序を入れ替えられる/,
  ],
];

function validate(text) {
  const errors = [];
  const normalized = text.replace(/\s+/g, ' ').trim();

  for (const [description, marker] of REQUIRED) {
    if (!normalized.includes(marker)) errors.push(`不足: ${description}`);
  }
  for (const [description, pattern] of FORBIDDEN) {
    if (pattern.test(normalized)) errors.push(`禁止: ${description}`);
  }

  return errors;
}

function selfTest() {
  const validFixture = REQUIRED.map(([, marker]) => marker).join('\n');
  if (validate(validFixture).length > 0) {
    throw new Error('自己テスト失敗: 正しい最小fixtureを受理できません');
  }

  const stale = `${validFixture}\n結合律が成立していれば、\n2つの合成順序を入れ替えられる。`;
  if (!validate(stale).some((error) => error.includes('合成順序の入替'))) {
    throw new Error('自己テスト失敗: 改行された旧い順序入替表現を拒否できません');
  }

  const staleVariant = `${validFixture}\n結合律が成立すれば、2つの合成順序を入れ替えられる。`;
  if (!validate(staleVariant).some((error) => error.includes('合成順序の入替'))) {
    throw new Error('自己テスト失敗: 旧表現の語形差を拒否できません');
  }

  const correctlyNegated = [
    '結合律から射の順序を交換できるとは限らない。',
    '結合律から射の順序を交換できるとは言えない。',
    '結合律では射の順序を交換できるわけではない。',
  ];
  for (const sentence of correctlyNegated) {
    if (validate(`${validFixture}\n${sentence}`).length > 0) {
      throw new Error(`自己テスト失敗: 正しい否定表現を受理できません: ${sentence}`);
    }
  }

  const missingEquation = validFixture.replace(REQUIRED[1][1], '等式なし');
  if (!validate(missingEquation).some((error) => error.includes('有効な再結合の等式'))) {
    throw new Error('自己テスト失敗: 再結合の等式欠落を拒否できません');
  }
}

if (process.argv.includes('--self-test')) {
  selfTest();
  console.log('Associativity wording checker self-test passed.');
  process.exit(0);
}

const repositoryRoot = path.resolve(__dirname, '..');
const chapterPath = path.join(repositoryRoot, CHAPTER);
const text = fs.readFileSync(chapterPath, 'utf8');

const errors = validate(text);
if (errors.length > 0) {
  console.error(errors.join('\n'));
  process.exit(1);
}

console.log('Associativity wording check passed.');

module.exports = { validate };
