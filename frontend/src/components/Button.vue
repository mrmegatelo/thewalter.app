<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  as?: string
  variant?: 'primary' | 'ghost' | 'outline' | 'text'
  size?: 'sm' | 'xs'
}

const { as = 'button', variant = 'primary', size } = defineProps<Props>()
const classObj = computed(() => ({
  button: true,
  [`button--${variant}`]: true,
  ...(size && { [`button--${size}`]: true }),
}))
</script>

<template>
  <component :is="as" :class="classObj">
    <div v-if="$slots.icon" class="button__icon">
      <slot name="icon"></slot>
    </div>
    <slot></slot>
  </component>
</template>

<style></style>
