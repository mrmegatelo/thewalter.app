<script setup lang="ts">
import Dialog from '@/components/Dialog.vue'
import { useSubscriptionsStore } from '@/stores/subscriptions.ts'
import { getCookie } from '@/utils/helpers.ts'
import { useCollectionsStore } from '@/stores/collections.ts'
import { inject } from 'vue'

const dialogsController = inject('dialogsController')
const subscriptions = useSubscriptionsStore()
const collections = useCollectionsStore()

function handleSubmit(e: Event) {
  e.preventDefault()
  const formData = new FormData(e.target as HTMLFormElement)
  const request = new Request('/api/v1/collections/', {
    method: 'POST',
    body: formData
  })

  request.headers.append('X-CSRFToken', getCookie('csrftoken'))

  fetch(request).then((res) => res.json()).then((res) => {
    collections.addCollection(res)
    dialogsController.hideDialog("collection-dialog")
  })
}

</script>

<template>
  <Dialog name="collection-dialog">
    <form
      @submit="handleSubmit"
      class="form flex-column-button-container"
    >
      <div class="form-inline-row">
        <div class="form-row">
          <input type="text" name="title" maxlength="200" required id="id_title" class="input"
                 placeholder="Collection title" />
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
                    :label="subscription.title"
                    class="input"
                  />
                  {{ subscription.title }}
                </label>
              </div>
            </div>
          </fieldset>
        </div>
        <button class="button button--primary button--sm" type="submit">Create</button>
      </div>
    </form>
  </Dialog>
</template>

<style scoped></style>
