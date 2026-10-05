import nx from '@nx/eslint-plugin';
import importPlugin from 'eslint-plugin-import';
import jsxA11y from 'eslint-plugin-jsx-a11y';

export default [
  ...nx.configs['flat/base'],
  ...nx.configs['flat/typescript'],
  ...nx.configs['flat/javascript'],
  {
    ignores: ['**/dist', '**/out-tsc', '**/vite.config.*.timestamp*'],
  },
  {
    files: ['**/*.tsx', '**/*.jsx'],
    plugins: { 'jsx-a11y': jsxA11y },
    rules: {
      ...jsxA11y.configs.recommended.rules,
      'jsx-a11y/heading-has-content': ['error', { components: ['CardTitle'] }],
    },
  },
  {
    files: [
      '**/*.ts',
      '**/*.tsx',
      '**/*.mts',
      '**/*.cts',
      '**/*.js',
      '**/*.jsx',
      '**/*.mjs',
      '**/*.cjs',
    ],
    rules: {
      '@nx/enforce-module-boundaries': [
        'error',
        {
          enforceBuildableLibDependency: true,
          allow: ['^.*/eslint(\\.base)?\\.config\\.[cm]?[jt]s$'],
          depConstraints: [
            {
              sourceTag: 'scope:web',
              onlyDependOnLibsWithTags: [
                'scope:core',
                'scope:types',
                'scope:ui',
                'scope:utils',
                'scope:components',
                'scope:api',
              ],
            },
            {
              sourceTag: 'scope:admin',
              onlyDependOnLibsWithTags: [
                'scope:core',
                'scope:types',
                'scope:ui',
                'scope:utils',
                'scope:components',
                'scope:api',
              ],
            },
            {
              sourceTag: 'scope:core',
              onlyDependOnLibsWithTags: [
                'scope:types',
                'scope:utils',
                'scope:api',
              ],
            },
            {
              sourceTag: 'scope:components',
              onlyDependOnLibsWithTags: [
                'scope:types',
                'scope:ui',
                'scope:utils',
                'scope:core',
              ],
            },
            {
              sourceTag: 'scope:ui',
              onlyDependOnLibsWithTags: ['scope:types', 'scope:utils'],
            },
            {
              sourceTag: 'scope:utils',
              onlyDependOnLibsWithTags: ['scope:types'],
            },
            {
              sourceTag: 'scope:api',
              onlyDependOnLibsWithTags: ['scope:types', 'scope:utils'],
            },
            {
              sourceTag: 'scope:types',
              onlyDependOnLibsWithTags: [],
            },
          ],
        },
      ],
    },
  },
  {
    files: [
      '**/*.ts',
      '**/*.tsx',
      '**/*.cts',
      '**/*.mts',
      '**/*.js',
      '**/*.jsx',
      '**/*.cjs',
      '**/*.mjs',
    ],
    plugins: { import: importPlugin },
    rules: {
      'import/newline-after-import': [
        'error',
        { count: 1, exactCount: true, considerComments: true },
      ],
      'import/order': [
        'error',
        {
          groups: [
            ['builtin', 'external'],
            'internal',
            ['parent', 'sibling', 'index'],
          ],
          pathGroups: [{ pattern: '@smart-hire/**', group: 'internal' }],
          pathGroupsExcludedImportTypes: ['builtin'],
          'newlines-between': 'always',
        },
      ],
      'padding-line-between-statements': [
        'error',
        {
          blankLine: 'always',
          prev: '*',
          next: ['export', 'class', 'function'],
        },
        { blankLine: 'any', prev: 'export', next: 'export' },
        { blankLine: 'always', prev: '*', next: 'return' },
        { blankLine: 'always', prev: ['const', 'let'], next: '*' },
        { blankLine: 'any', prev: ['const', 'let'], next: ['const', 'let'] },
      ],
      'lines-between-class-members': ['error', 'always'],
    },
  },
];
