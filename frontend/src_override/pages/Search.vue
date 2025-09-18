<template>
  <div class="flex items-center justify-center h-screen">
    <p class="text-gray-500">Opening Search in a new tab...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // Build base URL dynamically
  const baseUrl = `${window.location.protocol}//${window.location.host}`

  // Open in a new tab
  window.open(`${baseUrl}/app/organization-search`, '_blank')
})
</script>

<style scoped>
p {
  font-size: 1rem;
}
</style>

