<script setup lang="ts">
import { computed, defineEmits } from 'vue'
import { useFeedStore } from '@/stores/feed.ts'
import IconThumbDown from '@/components/icons/IconThumbDown.vue'
import IconTaskAlt from '@/components/icons/IconTaskAlt.vue'
import IconPaid from '@/components/icons/IconPaid.vue'
import { useRoute } from 'vue-router'
import { filter } from 'minimatch'

const route = useRoute()
const feedStore = useFeedStore()
const emit = defineEmits(['change'])
const filtersState = computed(() => feedStore.getFilters(route.name as string))

function handleFilterChange(e: Event) {
  const form = e.currentTarget as HTMLFormElement
  const formData = new FormData(form)
  const filters: Record<string, unknown> = {}
  for (const key of formData.keys()) {
    filters[key] = formData.getAll(key)
  }

  emit('change', filters)
}
</script>

<template>
  <div class="feed-list-filters">
    <h4 class="heading">Hide:</h4>
    <form @change="handleFilterChange" class="button-group">
      <div class="button-wrapper">
        <input
          type="checkbox"
          class="feed-filters-item__checkbox"
          name="exclude"
          id="not_interesting"
          value="not_interesting"
          :checked="filtersState['exclude']?.includes('not_interesting')"
        />
        <label
          for="not_interesting"
          class="feed-filters-item__title button button--primary button--xs button--outline"
        >
          <span class="button__icon">
            <IconThumbDown />
          </span>
          Not interesting
        </label>
      </div>
      <div class="button-wrapper">
        <input
          type="checkbox"
          class="feed-filters-item__checkbox"
          name="exclude"
          id="viewed"
          value="viewed"
          :checked="filtersState['exclude']?.includes('viewed')"
        />
        <label
          for="viewed"
          class="feed-filters-item__title button button--xs button--primary button--outline"
        >
          <span class="button__icon">
            <IconTaskAlt />
          </span>
          Viewed
        </label>
      </div>
      <div class="button-wrapper">
        <input
          type="checkbox"
          class="feed-filters-item__checkbox"
          name="exclude"
          id="paid"
          value="paid"
          :checked="filtersState['exclude']?.includes('paid')"
        />
        <label
          for="paid"
          class="feed-filters-item__title button button--xs button--primary button--outline"
        >
          <span class="button__icon">
            <IconPaid />
          </span>
          Paid content
        </label>
      </div>
    </form>
  </div>
</template>

<style scoped></style>
