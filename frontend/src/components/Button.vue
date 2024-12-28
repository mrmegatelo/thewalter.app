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

<style scoped>
.button {
  position: relative;
  display: inline-flex;
  align-items: center;
  overflow: hidden;
  white-space: nowrap;
  border-radius: calc(var(--grid-step) * 2);
  padding: calc(var(--grid-step) * 1) calc(var(--grid-step) * 2);
  border: none;
  font-weight: 500;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.15s;
  gap: 8px;
  flex-shrink: 0;

  .button__icon {
    width: 1.5rem;
  }

  &.button--sm {
    padding: calc(var(--grid-step) * 0.5) calc(var(--grid-step) * 1.25);
    border-radius: calc(var(--grid-step) * 1.5);
    gap: calc(var(--grid-step) * 0.75);

    & .button__icon {
      width: 1.25rem;
      /*margin-left: calc(var(--grid-step) * -0.5);*/
    }
  }

  &.button--xs {
    padding: calc(var(--grid-step) * 0.5) calc(var(--grid-step) * 1);
    border-radius: calc(var(--grid-step) * 1.25);
    gap: calc(var(--grid-step) * 0.5);
    font-size: 0.833rem;
    line-height: 1rem;

    & .button__icon {
      /*margin-left: calc(var(--grid-step) * -0.5);*/
      width: 1rem;
    }
  }

  &.button--text {
    padding: 0;
    border-radius: 0;
  }

  .loader {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;

    svg {
      width: 20px;
      height: 20px;
    }
  }

  & span {
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
}

.button--primary {
  background-color: var(--color-orange-500);
  border: 1px solid var(--color-orange-500);
  color: var(--color-white);

  &:hover {
    background-color: var(--color-orange-700);
  }

  .loader {
    background-color: var(--color-orange-500);

    svg path,
    svg rect {
      fill: var(--color-grey-100);
    }
  }

  &.button--outline {
    background: transparent;
    color: var(--color-orange-500);
    border: 1px solid var(--color-orange-200);
    box-shadow: none;

    &.active {
      background-color: var(--color-orange-100);
    }

    &:hover {
      background-color: var(--color-orange-100);
      border-color: var(--color-orange-500);
    }
  }
}

.button--ghost {
  background: transparent;
  color: var(--color-grey-1000);
  box-shadow: none;

  &:hover {
    background: var(--color-grey-100);
  }

  &.active {
    border: 1px solid var(--color-grey-200);
    background-color: var(--color-grey-100);
  }

  &.button--outline {
    background: transparent;
    border: 1px solid var(--color-grey-200);
    color: var(--color-grey-600);

    &:hover {
      border-color: var(--color-grey-600);
    }
  }
}

.button--outline {
  transition: border-color 0.15s;
}

.button--text {
  background: transparent;
  color: inherit;
  box-shadow: none;
  border: none;
}
</style>
