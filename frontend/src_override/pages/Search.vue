<template>
  <div class="flex items-center justify-center h-screen">
    <p class="text-gray-500">Redirecting to Search...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // Redirect to your external search page
  window.location.href = 'https://crm-demo.fr8labs.co/app/organization-search'
})
</script>

<style scoped>
p {
  font-size: 1rem;
}
</style>

