<script setup lang="ts">
  interface CircleProps {
    type: 'circle';
    radius?: string;
  }

  interface SquareProps {
    type: 'square'
    width?: string;
    height?: string;
  }

  type Props = SquareProps | CircleProps;

  const props = defineProps<Props>();

  const isCircle = props.type === 'circle'
  const isSquare = props.type === 'square'

  const inlineStyle = {
    ...(isCircle && { width: props.radius, height: props.radius, borderRadius: '50%' }),
    ...(isSquare && { width: props.width, height: props.height, borderRadius: 'calc(var(--grid-step) * 0.75)' })
  }

</script>

<template>
  <div class="skeleton" :style="inlineStyle"></div>
</template>

<style scoped>
  .skeleton {
    background-color: var(--color-grey-100);
    display: inline-block;
  }
</style>
