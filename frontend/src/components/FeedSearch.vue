<script setup lang="ts">
import TextInput from '@/components/TextInput.vue'
import { debounce } from '@/utils/helpers.ts'
import IconClose from '@/components/icons/IconClose.vue'
import { ref, watch } from 'vue'

const MIN_SEARCH_TERM_LENGTH = 2
const emit = defineEmits(['change'])
const search = ref("")

function handleChange(e: Event) {
  const searchTerm = (e.target as HTMLInputElement).value.trim()

  if (searchTerm.length < MIN_SEARCH_TERM_LENGTH && searchTerm !== '') {
    return
  }

  search.value = searchTerm
}

function cleanSearch() {
  search.value = ''
}

watch(search, (searchTerm) => {
  emit('change', {
    search: searchTerm || null,
  })
})

const handleChangeDebounced = debounce(handleChange, 500)
</script>

<template>
  <TextInput
    @keyup="handleChangeDebounced"
    :on-clear="cleanSearch"
    name="search"
    placeholder="Search in feed..."
    size="sm"
    :value="search"
  >
    <template v-if="search" #right-button>
      <IconClose />
    </template>
  </TextInput>
</template>

<style scoped></style>
