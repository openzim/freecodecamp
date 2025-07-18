import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import legacy from '@vitejs/plugin-legacy'

import { createHash } from 'crypto'
import { writeFileSync, existsSync, mkdirSync } from 'fs'
import { join } from 'path'
import { parse } from 'node-html-parser'

/**
 * Rewrites HTML code by extracting inline JS code to plain files, keeping the rest
 * intact.
 * @param html HTML code to rewrite
 * @param outputDir Directory where extracted JS files will be placed
 * @returns Rewriten HTML code
 */
const extractInlineJS = function (html: string, outputDir = 'dist') {
  const root = parse(html)

  const scriptTags = root.querySelectorAll('script')

  for (const tag of scriptTags) {
    const srcAttr = tag.getAttribute('src')
    const jsContent = tag.innerHTML.trim()

    // Only handle inline JS (no src and non-empty)
    if (!srcAttr && jsContent) {
      const hash = createHash('sha256').update(jsContent).digest('hex').slice(0, 8)
      const fileName = `inline-${hash}.js`
      const filePath = join(outputDir, fileName)

      // Write JS content to file if it doesn't exist
      if (existsSync(filePath)) {
        throw new Error(`Error while extracting inline JS: ${filePath} already exist`)
      }
      mkdirSync(outputDir, { recursive: true })
      writeFileSync(filePath, jsContent, 'utf-8')

      // Replace inner HTML with empty and add src attribute
      tag.set_content('')
      tag.setAttribute('src', `./${fileName}`)
    }
  }

  return root.toString()
}

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    vue(),
    legacy({
      modernTargets: ['fully supports bigint'],
      targets: ['fully supports es6'],
      modernPolyfills: true
    }),
    {
      name: 'vite-extract-inline-js',
      apply: 'build',
      enforce: 'post',
      transformIndexHtml(html) {
        return extractInlineJS(html)
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
