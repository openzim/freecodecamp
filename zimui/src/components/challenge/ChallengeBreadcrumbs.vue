<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { singlePathParam } from '@/utils/pathParams'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const main = useMainStore()
const route = useRoute()

const superblock = computed(() => singlePathParam(route.params.superblock))
const course = computed(() => singlePathParam(route.params.course))
</script>

<template>
  <div class="breadcrumbs">
    <nav>
      <ol>
        <li class="breadcrumb-left">
          <RouterLink to="/">{{ main.localesIntro?.[superblock].title }} </RouterLink>
        </li>
        <li class="breadcrumb-right">
          <RouterLink :to="`/${superblock}/${course}`">
            {{ main.localesIntro?.[superblock].blocks[course].title }}
          </RouterLink>
        </li>
      </ol>
    </nav>
  </div>
</template>

<style scoped>
.breadcrumbs {
  padding: 10px;
  margin: 0;
  font-size: 16px;
}

nav {
  border: 1px solid #d0d0d5;
}

ol {
  display: flex;
  justify-content: space-around;
}

.breadcrumb-left {
  background-color: #d0d0d5;
  margin-inline-end: 0.57rem;
  min-width: 3rem;
}

.breadcrumb-right {
  min-width: 50px;
}

.breadcrumb-left::after {
  background-color: #f5f6f7;
  border-bottom: 0.6rem solid transparent;
  border-inline-start: 0.55rem solid #d0d0d5;
  border-top: 0.6875rem solid transparent;
  content: '';
  height: 100%;
  margin-left: 3px;
}

.breadcrumb-left,
.breadcrumb-right {
  align-items: center;
  display: inline-flex;
  flex-grow: 1;
  justify-content: center;
}

a {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: inherit;
  width: 100%;
  text-align: center;
}
</style>
