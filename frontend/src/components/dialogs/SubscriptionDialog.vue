<script setup lang="ts">
import { reactive, ref } from 'vue'
import Dialog from '@/components/Dialog.vue'
import Button from '@/components/Button.vue'
import { getCookie } from '@/utils/helpers.ts'
import type { Subscription } from '@/stores/subscriptions.ts'
import FeedSubscription from '@/components/FeedSubscription.vue'

const url = ref('')

const results = reactive({
  list: [] as Subscription[],
})

function handleFormSubmit(e: Event) {
  e.preventDefault()
  const formData = new FormData(e.target as HTMLFormElement)

  const request = new Request('/api/v1/subscriptions/', {
    body: formData,
    method: 'POST',
  })

  request.headers.append('X-CSRFToken', getCookie('csrftoken'))

  fetch(request)
    .then((res) => res.json())
    .then((res) => {
      results.list = res
    })
}

function handleClose() {
  results.list = [] as Subscription[]
  url.value = ''
}
</script>

<template>
  <Dialog @close="handleClose" name="subscription-dialog">
    <form @submit="handleFormSubmit" class="form flex-column-button-container">
      <div class="form-inline-row">
        <div class="form-row">
          <input
            v-model="url"
            type="url"
            name="url"
            placeholder="Feed or Site URL"
            required
            class="input"
          />
        </div>
        <Button size="sm" type="submit">Add feed</Button>
      </div>
    </form>
    <ul class="feeds-list" v-for="feed in results.list" :key="feed.id">
      <li class="feed-description">
        <h4 class="heading">
          <a class="feed-links-list-item-link" href="#">
            {{ feed.title }}
          </a>
        </h4>
        <p v-if="feed.description" class="paragraph feed-description__text">
          {{ feed.description }}
        </p>
        <FeedSubscription :feed-id="feed.id" />
      </li>
    </ul>
  </Dialog>
</template>

<style scoped></style>
