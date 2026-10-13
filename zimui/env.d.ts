/// <reference types="vite/client" />

// Vuetify styles entrypoint resolves to CSS through package exports, without a .css
// extension, so it is not covered by vite/client declarations
declare module 'vuetify/styles'
