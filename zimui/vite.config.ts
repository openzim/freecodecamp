import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import legacy from '@vitejs/plugin-legacy'

import { createHash } from 'crypto'
import { writeFileSync, existsSync, mkdirSync, copyFileSync, readFileSync } from 'fs'
import { join } from 'path'
import { parse } from 'node-html-parser'

const buildOutputDir = '../scraper/src/fcc2zim/zimui'

// @freecodecamp/curriculum-helpers ships its challenge test-runner as plain
// (non-bundled-by-us) JS assets meant to be served next to the app and loaded
// by runChallenge.ts into a Web Worker (new Worker(assetPath + script)), so
// Vite can't statically discover/copy them like a normal import. We only run
// "javascript" type challenges (see src/constants.ts), so we only need
// javascript-test-evaluator.js and the chunk(s) it lazily loads at runtime
// (e.g. the `Explorer` helper); the dom/python evaluators (and the
// jQuery/pyodide/enzyme they can pull in) are intentionally left out.
const testRunnerSourceDir = 'node_modules/@freecodecamp/curriculum-helpers/dist/test-runner'
const testRunnerEntryScript = 'javascript-test-evaluator.js'

// The evaluator's lazily-loaded chunk files are content-hashed by webpack, so
// their names change on every curriculum-helpers release. Rather than
// hardcoding them, read the chunk id -> filename map webpack embeds in the
// entry script itself (its `__webpack_require__.u` function), so we always
// copy exactly the chunks this version of the evaluator can actually request.
const getTestRunnerChunkAssets = (entryScript: string): string[] => {
  const publicPathFn = entryScript.match(/__webpack_require__\.u=([\s\S]*?\+"\.js")/)?.[1]
  if (!publicPathFn) return []

  const namesById = new Map<string, string>()
  for (const [, id, name] of publicPathFn.matchAll(/(\d+)===e\?"([^"]+)":e/g)) {
    namesById.set(id, name)
  }

  const hashesById = publicPathFn.match(/\{[0-9]+:"[0-9a-f]+"(?:,[0-9]+:"[0-9a-f]+")*\}/)?.[0]
  if (!hashesById) return []

  return [...hashesById.matchAll(/([0-9]+):"([0-9a-f]+)"/g)].map(
    ([, id, hash]) => `${namesById.get(id) ?? id}.${hash}.js`
  )
}

const copyTestRunnerAssets = () => {
  const destDir = join('public', 'test-runner')
  mkdirSync(destDir, { recursive: true })

  const entryScriptContents = readFileSync(
    join(testRunnerSourceDir, testRunnerEntryScript),
    'utf-8'
  )
  const assets = [
    testRunnerEntryScript,
    `${testRunnerEntryScript}.LICENSE.txt`,
    ...getTestRunnerChunkAssets(entryScriptContents)
  ]

  for (const asset of assets) {
    const sourcePath = join(testRunnerSourceDir, asset)
    if (existsSync(sourcePath)) {
      copyFileSync(sourcePath, join(destDir, asset))
    }
  }
}

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
      name: 'vite-copy-test-runner-assets',
      buildStart: copyTestRunnerAssets
    },
    {
      name: 'vite-extract-inline-js',
      apply: 'build',
      enforce: 'post',
      transformIndexHtml(html) {
        return extractInlineJS(html, buildOutputDir)
      }
    }
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    outDir: buildOutputDir,
    emptyOutDir: true
  }
})
