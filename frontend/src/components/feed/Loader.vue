<script setup lang="ts">
import Skeleton from '@/components/ui/Skeleton.vue'

const loadersCount = 5;
</script>
<template>
  <div :key="n" v-for="n in loadersCount" class="feed-loader">
    <div class="feed-loader-header">
      <div class="feed-loader-title">
        <Skeleton type="circle" radius="20px"></Skeleton>
        <Skeleton type="square" width="100px" height="16px"></Skeleton>
      </div>
      <Skeleton type="square" width="100px" height="16px"></Skeleton>
    </div>
    <Skeleton type="square" width="80%" height="24px"></Skeleton>
    <div class="feed-loader-content">
      <Skeleton type="square" width="100%" height="14px"></Skeleton>
      <Skeleton type="square" width="100%" height="14px"></Skeleton>
      <Skeleton type="square" width="100%" height="14px"></Skeleton>
    </div>
    <Skeleton type="square" width="100%" height="226px"></Skeleton>
  </div>
</template>
<style scoped>
.feed-loader {
  padding: calc(var(--grid-step) * 2) calc(var(--grid-step) * 3) calc(var(--grid-step) * 3);
  display: flex;
  flex-direction: column;
  gap: calc(var(--grid-step) * 0.5);
}

.feed-loader-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.feed-loader-title {
  display: flex;
  gap: calc(var(--grid-step) * 0.5);
  align-items: center;
}

.feed-loader-content {
  display: flex;
  flex-direction: column;
  gap: calc(var(--grid-step) * 0.75);
}
</style>
