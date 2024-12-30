<script setup lang="ts">
import { defineEmits } from 'vue'
import { useFeedStore } from '@/stores/feed.ts'
import IconThumbDown from '@/components/icons/IconThumbDown.vue'
import IconTaskAlt from '@/components/icons/IconTaskAlt.vue'
import IconPaid from '@/components/icons/IconPaid.vue'

const feedStore = useFeedStore()
const emit = defineEmits(['change'])

function handleFilterChange(e: Event) {
  const form = e.currentTarget as HTMLFormElement
  const formData = new FormData(form)
  emit('change', formData)
}

</script>

<template>
  <div class="feed-list-filters">
    <h4 class="heading">Hide:</h4>
    <form @change="handleFilterChange" class="button-group">
      <div class="button-wrapper">
        <input type="checkbox" class="feed-filters-item__checkbox" name="exclude" id="not_interesting"
               value="not_interesting" checked>
        <label for="not_interesting"
               class="feed-filters-item__title  button button--primary button--xs button--outline">
          <span class="button__icon">
            <IconThumbDown />
          </span>
          Not interesting
        </label>
      </div>
      <div class="button-wrapper">
        <input type="checkbox" class="feed-filters-item__checkbox" name="exclude" id="viewed" value="viewed"
               checked>
        <label for="viewed"
               class="feed-filters-item__title button button--xs button--primary button--outline">
          <span class="button__icon">
            <IconTaskAlt />
          </span>
          Viewed
        </label>
      </div>
      <div class="button-wrapper">
        <input type="checkbox" class="feed-filters-item__checkbox" name="exclude" id="paid" value="paid">
        <label for="paid" class="feed-filters-item__title button button--xs button--primary button--outline">
          <span class="button__icon">
            <IconPaid />
          </span>
          Paid content
        </label>
      </div>
    </form>
  </div>
</template>

<style scoped>
.feed-list-filters {
  display: flex;
  align-items: center;
  gap: calc(var(--grid-step) * 1);
}

.button-group {
  display: flex;

  & > .button-wrapper {
    display: flex;

    & .button {
      --border-radius: calc(var(--grid-step) * 2);
      border-radius: unset;

      &.button--sm {
        --border-radius: calc(var(--grid-step) * 1.5);
      }

      &.button--xs {
        --border-radius: calc(var(--grid-step) * 1.25);
      }

    }

    & + & {
      .button {
        border-left: none;
      }
    }

    &:first-of-type .button {
      border-bottom-left-radius: var(--border-radius);
      border-top-left-radius: var(--border-radius);
    }

    &:last-of-type .button {
      border-bottom-right-radius: var(--border-radius);
      border-top-right-radius: var(--border-radius);
    }
  }
}

.feed-filters-item__checkbox {
  display: none;

  &:checked {
    & + .button--primary {
      background-color: var(--color-orange-100);
    }
  }
}
</style>
