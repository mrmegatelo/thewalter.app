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
    </Button>
    <div class="openable-body">
      <slot></slot>
    </div>
  </details>
</template>

<style>
.openable {
  &[open] {
    & .openable-control__indicator svg {
      transform: rotate(90deg);
    }
  }
}

.openable-body {
  padding-left: 16px;
  padding-top: 8px;
}

.openable-control {
  display: flex;
  width: 100%;
  position: relative;

  &:hover {
    & .openable-control__icon {
      opacity: 1;
      color: var(--color-grey-400);
    }
  }
}

.openable-control__icon {
  z-index: 1;
  width: 20px;
  height: 20px;
  border-radius: 6px;
  opacity: 0;
  transition:
    opacity 0.05s,
    color 0.15s ease 0.05s,
    background-color 0.15s;

  background-color: var(--color-grey-100);
  color: var(--color-grey-100);

  &:hover {
    background-color: var(--color-grey-200);
  }
}

.openable-control__indicator {
  position: absolute;
  left: 10px;
  top: 6px;

  & > svg {
    transition: transform 0.15s;
  }
}

.openable__link {
  display: block;
  text-decoration: none;
  color: inherit;
  flex: 1;
  text-align: left;
}
</style>
