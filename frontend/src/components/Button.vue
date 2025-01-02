<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  as?: string
  variant?: 'primary' | 'ghost' | 'outline' | 'text'
  size?: 'sm' | 'xs'
}

const { as = 'button', variant = 'primary', size } = defineProps<Props>()
const sizeClass = computed(() => (size ? `button--${size}` : ''))
</script>

<template>
  <component :is="as" :class="`button button--${variant} ${sizeClass}`">
    <div v-if="$slots.icon" class="button__icon">
      <slot name="icon"></slot>
    </div>
    <slot></slot>
  </component>
</template>

<style>
</style>
