<script setup lang="ts">
import Button from '@/components/Button.vue'
import IconChevronRight from '@/components/icons/IconChevronRight.vue'
</script>

<template>
  <details class="openable">
    <Button as="summary" class="openable-control" variant="ghost" size="sm">
      <span class="button__icon openable-control__icon openable-control__indicator">
        <IconChevronRight width="20" height="20" />
      </span>
      <template v-if="$slots.icon" #icon-left>
        <slot name="icon"></slot>
      </template>
      <slot name="trigger"></slot>
      <template #icon-right>
        <slot name="right"></slot>
      </template>
    </Button>
    <div class="openable-body">
      <slot></slot>
    </div>
  </details>
</template>

<style></style>
