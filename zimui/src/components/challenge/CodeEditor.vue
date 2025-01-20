<script setup lang="ts">
import { shallowRef } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { javascript } from '@codemirror/lang-javascript'
import { EditorView } from '@codemirror/view'
import { useMainStore } from '@/stores/main'

const main = useMainStore()

const extensions = [javascript()]

// Codemirror EditorView instance ref
const view = shallowRef()
const handleReady = ({ view: editorView }: { view: EditorView }) => {
  view.value = editorView
}

// Status is available at all times via Codemirror EditorView
// const getCodemirrorStates = () => {
//   const state = view.value.state
//   const ranges = state.selection.ranges
//   // const selected = ranges.reduce((r, range) => r + range.to - range.from, 0)
//   // const cursor = ranges[0].anchor
//   // const length = state.doc.length
//   // const lines = state.doc.lines
//   // more state info ...
//   // return ...
// }
</script>

<template>
  <div>
    <codemirror
      v-model="main.solution"
      placeholder="Code goes here..."
      :style="{ height: '100%' }"
      :autofocus="true"
      :indent-with-tab="true"
      :tab-size="2"
      :extensions="extensions"
      @ready="handleReady"
      @change="(event: any) => (main.solution = event)"
    />
  </div>
</template>

<style scoped></style>
