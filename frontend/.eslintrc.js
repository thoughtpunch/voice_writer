module.exports = {
    parserOptions: {
        parser: '@typescript-eslint/parser',
        ecmaVersion: 2020,
        sourceType: 'module'
    },
    extends: [
        'plugin:@typescript-eslint/recommended',
        'plugin:vue/vue3-recommended',
        'eslint:recommended'
    ],
    rules: {
        // Your rules here
    }
}