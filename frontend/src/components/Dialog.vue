<script setup lang="ts">
import { onMounted, onUnmounted, useTemplateRef } from 'vue'

const dialogRef = useTemplateRef('dialogRef')

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
