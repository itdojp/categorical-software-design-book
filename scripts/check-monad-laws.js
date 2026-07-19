#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const CHAPTER_PATH = path.join(ROOT, 'chapters/chapter09/index.md');
const GLOSSARY_PATH = path.join(ROOT, 'GLOSSARY.md');

const REQUIRED_CHAPTER_MARKERS = [
  ['Kleisli射fの型', '`f: A → Result<B, E>`'],
  ['Kleisli射gの型', '`g: B → Result<C, E>`'],
  ['composeの適用順', '先に `f`、次に `g`'],
  ['left identityの式', 'kleisliCompose(unit, f)(a) = f(a)'],
  ['right identityの式', 'kleisliCompose(f, unit)(a) = f(a)'],
  [
    'associativityの式',
    'kleisliCompose(kleisliCompose(f, g), k) = kleisliCompose(f, kleisliCompose(g, k))',
  ],
  ['再結合と順序交換の区別', '結合律が許すのは再結合'],
  ['成功fixture', '| `"2"` |'],
  ['前段失敗fixture', '| `"0"` |'],
  ['中段失敗fixture', '| `"4"` |'],
  ['後段失敗fixture', '| `"3"` |'],
  ['runtime対応が比喩であること', '設計上の対応づけ（比喩）'],
  ['runtime検証条件', '| law | 対応づける変更 | 検証条件 | violationで観測されるsymptom |'],
  ['left identityのruntime symptom', 'adapterがDB/toolを呼ぶ、監査が二重化する、tenant束縛が変わる'],
  ['right identityのruntime symptom', '`Err`が成功へ変換される、余分なwriteが起きる、監査やidempotency keyが失われる'],
  ['associativityのruntime symptom', 'retry範囲が変わる、toolが重複実行される、失敗後に後段が走る、traceが欠落する'],
  ['順序交換をlaw検証から除外', 'toolの順序交換はlawの検証に含めず'],
];

const REQUIRED_GLOSSARY_MARKERS = [
  'left identity、right identity、associativity',
  '形式law、agent runtimeへの比喩、観測可能な検証条件',
];

const CONTEXTUAL_CHAPTER_MARKERS = [
  [
    'ミニ例の型ブロック',
    [
      '- `f: A → Result<B, E>`',
      '- `g: B → Result<C, E>`',
      '- `h: A → Result<C, E>`（`h = kleisliCompose(f, g)`、圏論の記法では `h = g ∘ f` に相当）',
    ].join('\n'),
  ],
  [
    'law導入の型ブロック',
    '`f: A → Result<B, E>`、`g: B → Result<C, E>`、`k: C → Result<D, E>`とすると、',
  ],
  [
    'compose実装の適用順',
    '(a: A): Result<C, E> => bind(f(a), g);',
  ],
];

function ok(value) {
  return { ok: true, value };
}

function err(error) {
  return { ok: false, error };
}

function unit(value) {
  return ok(value);
}

function bind(result, next) {
  return result.ok ? next(result.value) : result;
}

function kleisliCompose(first, second) {
  return (input) => bind(first(input), second);
}

function equalResult(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function parseQuantity(input) {
  return /^[1-9]\d*$/.test(input) ? ok(Number(input)) : err('InvalidQuantity');
}

function reserveInventory(quantity) {
  return quantity <= 3 ? ok({ quantity, state: 'Reserved' }) : err('OutOfStock');
}

function authorizePayment(reservation) {
  return reservation.quantity === 3
    ? err('PaymentDeclined')
    : ok({ quantity: reservation.quantity, state: 'Authorized' });
}

function verifyResultLaws(unitFunction = unit) {
  const failures = [];
  const stages = [
    ['parseQuantity', parseQuantity, ['0', '2', '3', '4', 'not-a-number']],
    ['reserveInventory', reserveInventory, [1, 2, 3, 4]],
    [
      'authorizePayment',
      authorizePayment,
      [
        { quantity: 2, state: 'Reserved' },
        { quantity: 3, state: 'Reserved' },
      ],
    ],
  ];

  for (const [name, stage, inputs] of stages) {
    for (const input of inputs) {
      const leftIdentity = kleisliCompose(unitFunction, stage)(input);
      const direct = stage(input);
      if (!equalResult(leftIdentity, direct)) {
        failures.push(`left identity failed: ${name}(${JSON.stringify(input)})`);
      }

      const rightIdentity = kleisliCompose(stage, unitFunction)(input);
      if (!equalResult(rightIdentity, direct)) {
        failures.push(`right identity failed: ${name}(${JSON.stringify(input)})`);
      }
    }
  }

  const leftGrouped = kleisliCompose(
    kleisliCompose(parseQuantity, reserveInventory),
    authorizePayment,
  );
  const rightGrouped = kleisliCompose(
    parseQuantity,
    kleisliCompose(reserveInventory, authorizePayment),
  );
  for (const input of ['0', '2', '3', '4', 'not-a-number']) {
    if (!equalResult(leftGrouped(input), rightGrouped(input))) {
      failures.push(`associativity failed: ${JSON.stringify(input)}`);
    }
  }

  const expectedFixtures = new Map([
    ['0', err('InvalidQuantity')],
    ['2', ok({ quantity: 2, state: 'Authorized' })],
    ['3', err('PaymentDeclined')],
    ['4', err('OutOfStock')],
  ]);
  for (const [input, expected] of expectedFixtures) {
    if (!equalResult(leftGrouped(input), expected)) {
      failures.push(`fixture outcome drifted: ${JSON.stringify(input)}`);
    }
  }

  return failures;
}

function validateText(chapter, glossary) {
  const failures = [];
  for (const [description, marker] of REQUIRED_CHAPTER_MARKERS) {
    if (!chapter.includes(marker)) failures.push(`Chapter 9不足: ${description}`);
  }
  for (const [description, marker] of CONTEXTUAL_CHAPTER_MARKERS) {
    if (!chapter.includes(marker)) failures.push(`Chapter 9不整合: ${description}`);
  }
  for (const marker of REQUIRED_GLOSSARY_MARKERS) {
    if (!glossary.includes(marker)) failures.push(`Glossary不足: ${marker}`);
  }
  return failures;
}

function selfTest(chapter, glossary) {
  if (validateText(chapter, glossary).length > 0) {
    throw new Error('自己テスト失敗: 現行本文の必須契約を読み取れません');
  }

  const associativityMarker = REQUIRED_CHAPTER_MARKERS.find(([description]) =>
    description === 'associativityの式'
  );
  const withoutAssociativity = chapter.replace(associativityMarker[1], '式なし');
  if (!validateText(withoutAssociativity, glossary).some((failure) => failure.includes('associativity'))) {
    throw new Error('自己テスト失敗: associativity式の欠落を拒否できません');
  }

  const withoutRightIdentity = chapter.replace('kleisliCompose(f, unit)(a) = f(a)', '式なし');
  if (!validateText(withoutRightIdentity, glossary).some((failure) => failure.includes('right identity'))) {
    throw new Error('自己テスト失敗: right identity式の欠落を拒否できません');
  }

  const reversedComposeOrder = chapter.replace('先に `f`、次に `g`', '先に `g`、次に `f`');
  if (!validateText(reversedComposeOrder, glossary).some((failure) => failure.includes('適用順'))) {
    throw new Error('自己テスト失敗: compose順の逆転を拒否できません');
  }

  const contextualMutations = [
    ['ミニ例f型', '- `f: A → Result<B, E>`', '- `f: A → Result<C, E>`', 'ミニ例の型ブロック'],
    ['ミニ例g型', '- `g: B → Result<C, E>`', '- `g: A → Result<C, E>`', 'ミニ例の型ブロック'],
    [
      'ミニ例h型',
      '- `h: A → Result<C, E>`（`h = kleisliCompose(f, g)`、圏論の記法では `h = g ∘ f` に相当）',
      '- `h: B → Result<C, E>`（`h = kleisliCompose(f, g)`、圏論の記法では `h = g ∘ f` に相当）',
      'ミニ例の型ブロック',
    ],
    [
      'law導入k型',
      '`f: A → Result<B, E>`、`g: B → Result<C, E>`、`k: C → Result<D, E>`とすると、',
      '`f: A → Result<B, E>`、`g: B → Result<C, E>`、`k: B → Result<D, E>`とすると、',
      'law導入の型ブロック',
    ],
    [
      'compose実装順',
      '(a: A): Result<C, E> => bind(f(a), g);',
      '(a: A): Result<C, E> => bind(g(a), f);',
      'compose実装の適用順',
    ],
  ];
  for (const [name, before, after, expectedFailure] of contextualMutations) {
    const mutated = chapter.replace(before, after);
    if (mutated === chapter) throw new Error(`自己テスト失敗: ${name}のmutation対象がありません`);
    if (!validateText(mutated, glossary).some((failure) => failure.includes(expectedFailure))) {
      throw new Error(`自己テスト失敗: ${name}の局所的不整合を拒否できません`);
    }
  }

  const withoutAnalogyBoundary = chapter.replace('設計上の対応づけ（比喩）', '同一視');
  if (!validateText(withoutAnalogyBoundary, glossary).some((failure) => failure.includes('比喩'))) {
    throw new Error('自己テスト失敗: runtime比喩境界の欠落を拒否できません');
  }

  const withoutAssociativitySymptom = chapter.replace(
    'retry範囲が変わる、toolが重複実行される、失敗後に後段が走る、traceが欠落する',
    'symptomなし',
  );
  if (!validateText(withoutAssociativitySymptom, glossary).some((failure) => failure.includes('runtime symptom'))) {
    throw new Error('自己テスト失敗: law別runtime symptomの欠落を拒否できません');
  }

  const degradedGlossary = glossary.replace(
    'left identity、right identity、associativity',
    'law',
  );
  if (!validateText(chapter, degradedGlossary).some((failure) => failure.includes('Glossary不足'))) {
    throw new Error('自己テスト失敗: Glossaryのlaw欠落を拒否できません');
  }

  const unlawfulUnit = (value) => ok({ unexpectedlyWrapped: value });
  if (verifyResultLaws(unlawfulUnit).length === 0) {
    throw new Error('自己テスト失敗: 不正なunitによるlaw violationを検出できません');
  }
}

const chapter = fs.readFileSync(CHAPTER_PATH, 'utf8');
const glossary = fs.readFileSync(GLOSSARY_PATH, 'utf8');

if (process.argv.includes('--self-test')) {
  selfTest(chapter, glossary);
  console.log('Monad law checker self-test passed.');
  process.exit(0);
}

const failures = [
  ...validateText(chapter, glossary),
  ...verifyResultLaws(),
];
if (failures.length > 0) {
  console.error(failures.join('\n'));
  process.exit(1);
}

console.log('Monad laws passed: left identity, right identity, associativity, and 4 Result fixtures.');

module.exports = { validateText, verifyResultLaws };
