<script setup lang="ts">
import Dialog from '@/components/Dialog.vue'
import Button from '@/components/Button.vue'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { getCookie } from '@/utils/helpers.ts'
import { type Collection, useCollectionsStore } from '@/stores/collections.ts'
import { inject, ref, defineExpose } from 'vue'
import { Injection } from '@/utils/constants'

const DIALOG_NAME = 'collection-dialog'
const dialogsController = inject(Injection.DialogController)
const subscriptions = useSubscriptionsStore()
const collections = useCollectionsStore()
const currentCollection = ref<Collection>()

function setCollection(collection: Collection) {
  currentCollection.value = collection
}

defineExpose({ setCollection })

function handleSubmit(e: Event) {
  e.preventDefault()
  const formData = new FormData(e.target as HTMLFormElement)
  const request = new Request('/api/v1/collections/', {
    method: 'POST',
    body: formData,
  })

  request.headers.append('X-CSRFToken', getCookie('csrftoken'))

  fetch(request)
    .then((res) => res.json())
    .then((res) => {
      collections.addCollection(res)
      dialogsController?.hideDialog(DIALOG_NAME)
    })
}
</script>

<template>
  <Dialog :name="DIALOG_NAME">
    <form @submit="handleSubmit" class="form flex-column-button-container">
      <div class="form-inline-row">
        <div class="form-row">
          <input
            type="text"
            name="title"
            maxlength="200"
            required
            id="id_title"
            class="input"
            placeholder="Collection title"
            :value="currentCollection?.title"
          />
        </div>

        <div class="form-row">
          <fieldset>
            <legend class="form-label">Choose feeds:</legend>

            <div id="id_feeds">
              <div v-for="subscription in subscriptions.list" :key="subscription.id">
                <label>
                  <input
                    type="checkbox"
                    name="feeds"
                    :value="subscription.id"
                    :checked="currentCollection?.feeds.includes(subscription.id)"
                    class="input"
                  />
                  {{ subscription.title }}
                </label>
              </div>
            </div>
          </fieldset>
        </div>
        <Button size="sm" type="submit">Create</Button>
      </div>
    </form>
  </Dialog>
</template>

<style scoped></style>
