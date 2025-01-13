<script setup lang="ts">
import Button from '@/components/Button.vue'
import { computed } from 'vue'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { getCookie } from '@/utils/helpers.ts'

const { feedId } = defineProps({ feedId: Number })
const subscriptions = useSubscriptionsStore()

const isSubscribed = computed(() => feedId && subscriptions.getFeedById(feedId)?.is_subscribed)

function handleSubmit(e: Event) {
  if (!feedId) {
    return;
  }

  e.preventDefault()
  const method = isSubscribed.value ? 'DELETE' : 'POST'
  const request = new Request(`/api/v1/subscriptions/${feedId}/subscription/`, {
    method
  })
  request.headers.append('X-CSRFToken', getCookie('csrftoken'))

  fetch(request)
    .then(res => res.json())
    .then((res) => {
      if (isSubscribed.value) {
        subscriptions.unsubscribe(feedId)
      } else {
        subscriptions.subscribe(res)
      }
    })
}
</script>

<template>
  <form @submit="handleSubmit">
    <Button v-if="isSubscribed" size="sm" type="submit">Unsubscribe</Button>
    <Button v-else size="sm" type="submit">Subscribe</Button>
  </form>
</template>

<style scoped>

</style>
