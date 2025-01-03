<script setup lang="ts">

import TextInput from '@/components/TextInput.vue'
import { debounce } from '@/utils/helpers.ts'

const MIN_SEARCH_TERM_LENGTH = 2
const emit = defineEmits(['change'])


function handleChange(e: Event) {
  const searchTerm = (e.target as HTMLInputElement).value.trim()

  if (searchTerm.length < MIN_SEARCH_TERM_LENGTH && searchTerm !== '') {
    return
  }

  emit('change', {
    ...(searchTerm !== '' && { search: searchTerm })
  })
}

const handleChangeDebounced = debounce(handleChange, 500)

</script>

<template>
  <TextInput @keyup="handleChangeDebounced" name="search" placeholder="Search in feed..." size="sm" />
</template>

<style scoped>

</style>
