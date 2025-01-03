<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'sm' | 'xs'
}

const { size } = defineProps<Props>()

const classObj = computed(() => ({
  input: true,
   ...(size && ({ [`input--${size}`]: true })),
}))
</script>

<template>
  <input :class="classObj" />
</template>

<style scoped>
</style>
