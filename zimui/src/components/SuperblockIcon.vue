<script setup lang="ts">
import { computed, toRef } from 'vue'
import icon_backend_dev from '../assets/icon_backend_dev.svg'
import icon_c_sharp from '../assets/icon_c_sharp.svg'
import icon_coding_interview from '../assets/icon_coding_interview.svg'
import icon_college_algebra from '../assets/icon_college_algebra.svg'
import icon_cybersecurity from '../assets/icon_cybersecurity.svg'
import icon_database from '../assets/icon_database.svg'
import icon_dataviz from '../assets/icon_dataviz.svg'
import icon_english_a2 from '../assets/icon_english_a2.svg'
import icon_english_b1 from '../assets/icon_english_b1.svg'
import icon_frontend from '../assets/icon_frontend.svg'
import icon_fullstack from '../assets/icon_fullstack.svg'
import icon_javascript from '../assets/icon_javascript.svg'
import icon_machine_learning from '../assets/icon_machine_learning.svg'
import icon_odin_project from '../assets/icon_odin_project.svg'
import icon_project_euler from '../assets/icon_project_euler.svg'
import icon_python_data_analysis from '../assets/icon_python_data_analysis.svg'
import icon_python_logo from '../assets/icon_python_logo.svg'
import icon_quality_assurance from '../assets/icon_quality_assurance.svg'
import icon_resp_web_design from '../assets/icon_resp_web_design.svg'
import icon_rosetta_code from '../assets/icon_rosetta_code.svg'

const props = defineProps<{
  superblock: string
}>()

const superblock = toRef(props, 'superblock')

const icon = computed(() => {
  if (
    superblock.value == 'responsive-web-design' ||
    superblock.value == '2022/responsive-web-design'
  ) {
    return icon_resp_web_design
  } else if (
    superblock.value == 'javascript-algorithms-and-data-structures' ||
    superblock.value == 'javascript-algorithms-and-data-structures-v8'
  ) {
    return icon_javascript
  } else if (superblock.value == 'front-end-development-libraries') {
    return icon_frontend
  } else if (superblock.value == 'data-visualization') {
    return icon_dataviz
  } else if (superblock.value == 'relational-database') {
    return icon_database
  } else if (superblock.value == 'back-end-development-and-apis') {
    return icon_backend_dev
  } else if (superblock.value == 'quality-assurance') {
    return icon_quality_assurance
  } else if (superblock.value == 'scientific-computing-with-python') {
    return icon_python_logo
  } else if (superblock.value == 'data-analysis-with-python') {
    return icon_python_data_analysis
  } else if (superblock.value == 'data-analysis-with-python') {
    return icon_python_data_analysis
  } else if (superblock.value == 'information-security') {
    return icon_cybersecurity
  } else if (superblock.value == 'machine-learning-with-python') {
    return icon_machine_learning
  } else if (superblock.value == 'college-algebra-with-python') {
    return icon_college_algebra
  } else if (superblock.value == 'python-for-everybody') {
    return icon_python_logo
  } else if (superblock.value == 'coding-interview-prep') {
    return icon_coding_interview
  } else if (superblock.value == 'the-odin-project') {
    return icon_odin_project
  } else if (superblock.value == 'project-euler') {
    return icon_project_euler
  } else if (superblock.value == 'foundational-c-sharp-with-microsoft') {
    return icon_c_sharp
  } else if (superblock.value == 'a2-english-for-developers') {
    return icon_english_a2
  } else if (superblock.value == 'b1-english-for-developers') {
    return icon_english_b1
  } else if (superblock.value == 'rosetta-code') {
    return icon_rosetta_code
  } else if (superblock.value == 'full-stack-developer') {
    return icon_fullstack
  } else {
    return icon_project_euler // fallback, just in-case
  }
})
</script>

<template>
  <img :src="icon" aria-hidden="true" />
</template>

<style scoped></style>
