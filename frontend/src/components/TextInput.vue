<script setup lang="ts">

</script>

<template>
<input class="input input--sm">
</template>

<style scoped>
.input {
    border: 1px solid var(--color-grey-200);
    padding: calc(var(--grid-step) * 1) calc(var(--grid-step) * 2);
    border-radius: calc(var(--grid-step) * 2);

    &.error {
        border-color: var(--color-error);
    }

    &.input--sm {
        padding: calc(var(--grid-step) * 0.5) calc(var(--grid-step) * 1.25);
        border-radius: calc(var(--grid-step) * 1.5);
    }
}
</style>
