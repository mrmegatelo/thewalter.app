<script setup lang="ts">
import Skeleton from '@/components/ui/Skeleton.vue'
const numRows = 25
</script>

<template>
  <div :key="num" v-for="num in numRows" class="row">
    <Skeleton type="circle" radius="20px" />
    <skeleton type="square" width="calc(100% - 24px)" height="20px" />
  </div>
</template>

<style scoped>
.row {
  display: flex;
  gap: calc(var(--grid-step) * 0.75);
  padding: calc(var(--grid-step) * 0.5) calc(var(--grid-step) * 1.25);
}
</style>
