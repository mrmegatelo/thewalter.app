<script setup lang="ts">
import { onMounted, onUnmounted, useTemplateRef, defineProps, inject } from 'vue'

interface Props {
  name: string
}

const { name } = defineProps<Props>()
const dialogRef = useTemplateRef('dialogRef')
const dialogsController = inject('dialogsController')

function open() {
  dialogRef.value?.showModal()
}

function handleClick(e: Event) {
  const target = e.target as HTMLElement
  if (target === dialogRef.value) {
    dialogRef.value?.close()
  }
}

defineExpose({
  open
})

onMounted(() => {
  console.log({ dialogsController })
  dialogsController.addDialog(name, dialogRef.value)
})

onUnmounted(() => {
  dialogsController.removeDialog(name)
})

</script>

<template>
  <dialog @click="handleClick" class="dialog dialog_top" ref="dialogRef">
    <div class="dialog-content">
      <slot></slot>
    </div>
  </dialog>
</template>

<style scoped>

</style>
