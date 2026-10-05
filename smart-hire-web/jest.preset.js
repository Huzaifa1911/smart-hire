const nxPreset = require('@nx/jest/preset').default;

module.exports = {
  ...nxPreset,
  moduleNameMapper: {
    '^@smart-hire/(api|core|components|ui|utils|types)$':
      '<rootDir>/../../packages/$1/src/index.ts',
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
};
