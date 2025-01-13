<script setup lang="ts">
import { onMounted, onUnmounted, useTemplateRef, defineProps, defineEmits, inject } from 'vue'
import { Injection } from '@/utils/constants.ts'

interface Props {
  name: string
}

const { name } = defineProps<Props>()
const emit = defineEmits(['close'])
const dialogRef = useTemplateRef('dialogRef')
const dialogsController = inject(Injection.DialogController)

function open() {
  dialogRef.value?.showModal()
}

function handleClick(e: Event) {
  const target = e.target as HTMLElement
  if (target === dialogRef.value) {
    dialogRef.value?.close()
  }
}

function handleDialogClose(e: Event) {
  emit('close')
}

defineExpose({
  open,
})

onMounted(() => {
  dialogsController?.addDialog(name, dialogRef.value as HTMLDialogElement)
  dialogRef.value?.addEventListener('close', handleDialogClose)
})

onUnmounted(() => {
  dialogsController?.removeDialog(name)
  dialogRef.value?.removeEventListener('close', handleDialogClose)
})
</script>

<template>
  <dialog @click="handleClick" class="dialog dialog_top" ref="dialogRef" :name="name">
    <div class="dialog-content">
      <slot></slot>
    </div>
  </dialog>
</template>

<style scoped></style>
