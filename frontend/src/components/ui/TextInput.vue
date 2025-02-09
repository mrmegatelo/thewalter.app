<script setup lang="ts">
import { computed } from 'vue'
import Button from '@/components/ui/Button.vue'

interface Props {
  size?: 'sm' | 'xs'
  value?: string
  placeholder?: string
  onClear?: () => void
}

const { size, placeholder, value, onClear } = defineProps<Props>()

const classObj = computed(() => ({
  input: true,
  ...(size && { [`input--${size}`]: true })
}))
</script>

<template>
  <div class="form-inline-row">
    <div class="form-row">
      <input :class="classObj" :placeholder="placeholder" type="text" :value="value" />
    </div>
    <Button @click="onClear" v-if="$slots['right-button']" variant="ghost" size="xs">
      <template #icon-left>
        <slot name="right-button"></slot>
      </template>
    </Button>
  </div>
</template>

<style scoped></style>
