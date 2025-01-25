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
  const url = currentCollection.value ? `/api/v1/collections/${currentCollection.value.id}/` : '/api/v1/collections/'
  const method = currentCollection.value ? 'PATCH' : 'POST'
  const request = new Request(url, {
    method,
    body: formData,
  })

  request.headers.append('X-CSRFToken', getCookie('csrftoken'))

  fetch(request)
    .then((res) => res.json())
    .then((res) => {
      // eslint-disable-next-line @typescript-eslint/no-unused-expressions
      currentCollection.value ? collections.update(res) : collections.add(res)
      dialogsController?.hideDialog(DIALOG_NAME)
    })
}

function resetCollection() {
  currentCollection.value = undefined
}
</script>

<template>
  <Dialog @close="resetCollection" :name="DIALOG_NAME">
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
        <Button size="sm" type="submit">{{currentCollection ? "Update" : "Create"}}</Button>
      </div>
    </form>
  </Dialog>
</template>

<style scoped></style>
