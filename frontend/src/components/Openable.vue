<script setup lang="ts">
import Button from '@/components/Button.vue'
import IconChevronRight from '@/components/icons/IconChevronRight.vue'
import IconFolder from '@/components/icons/IconFolder.vue'
</script>

<template>
  <details class="openable">
    <Button as="summary" class="openable-control" variant="ghost" size="sm">
      <span class="button__icon openable-control__icon openable-control__indicator">
        <IconChevronRight />
      </span>
      <span v-if="$slots.icon" class="button__icon">
        <slot name="icon"></slot>
      </span>
      <slot name="trigger"></slot>
      <slot name="right"></slot>
    </Button>
    <div class="openable-body">
      <slot></slot>
    </div>
  </details>
</template>

<style></style>
