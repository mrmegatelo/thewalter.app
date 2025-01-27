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
    <div v-if="$slots['icon-left']" class="button__icon">
      <slot name="icon-left"></slot>
    </div>
    <span v-if="$slots.default"><slot></slot></span>
    <div v-if="$slots['icon-right']" class="button__right">
      <slot name="icon-right"></slot>
    </div>
  </component>
</template>

<style></style>
