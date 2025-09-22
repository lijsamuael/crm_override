<template>
  <div class="min-h-screen bg-white">
    <div class="mx-auto w-full max-w-3xl pt-24 px-4">
      <div class="rounded-lg border border-gray-200 bg-white shadow-sm">
        <div class="px-6 py-5">
          <h1 class="text-center text-lg font-semibold text-gray-800 mb-3">
            Organization Search
          </h1>

          <!-- Search input -->
          <div class="flex items-center gap-3">
            <input
              v-model="query"
              @keydown.enter="searchNow"
              type="text"
              placeholder="Search CRM organizations..."
              class="flex-1 rounded-md border border-gray-200 px-4 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-slate-300"
            />
            <button
              @click="searchNow"
              class="inline-flex items-center gap-2 rounded-md bg-black px-3 py-2 text-sm font-medium text-white hover:opacity-95"
            >
              Search
            </button>
          </div>

          <!-- Results -->
          <div class="mt-4">
            <div v-if="loading" class="text-center text-gray-500">Searching...</div>

            <div v-else-if="!loading && searched && results.length === 0"
              class="mt-3 rounded-md bg-amber-50 p-4 text-amber-800">
              <div class="font-medium mb-2">No organizations found. Try:</div>
              <ul class="list-disc pl-5 space-y-1 text-sm">
                <li>Check spelling</li>
                <li>Use fewer words</li>
                <li>Try a different search term</li>
              </ul>
            </div>

            <div v-else-if="results.length" class="mt-3 space-y-3">
              <div
                v-for="org in results"
                :key="org.name"
                class="rounded-md border border-gray-100 bg-white px-4 py-3 hover:bg-slate-50"
              >
                <div class="text-sm font-bold text-gray-800">
                  {{ org.organization_name || org.name }}
                </div>
                <div class="text-xs text-gray-500 mt-0.5">ID: {{ org.name }}</div>
                <div class="text-xs text-gray-500 mt-0.5">
                  Owner: {{ org.custom_organization_owner || "Not Assigned" }}
                </div>
              </div>
            </div>
          </div>
        </div> <!-- inner -->
      </div> <!-- card -->
    </div> <!-- container -->
  </div>
</template>


<script setup>
import { ref, watch } from 'vue'

const query = ref('')
const results = ref([])
const loading = ref(false)
const searched = ref(false)
const error = ref(null)

let debounceTimer = null
const DEBOUNCE_MS = 300

// Link helper
function orgLink(org) {
  const base = window.location.origin
  const orgName = encodeURIComponent(org.organization_name || org.name)
  return `${base}/crm/organizations/${orgName}`
}

async function searchNow() {
  const q = (query.value || '').trim()
  searched.value = true
  results.value = []
  error.value = null

  if (!q) return

  loading.value = true
  try {
    const base = window.location.origin
    const params = new URLSearchParams()
    params.append('search_query', q)

    // Call your API: crm_override.app
    const url = `${base}/api/method/crm_override.api.search_organizations_external?${params.toString()}`
    const resp = await fetch(url, {
      method: 'GET',
      credentials: 'include',
      headers: { Accept: 'application/json' },
    })

    if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`)

    const json = await resp.json()
    // ✅ Adjusted: results are under json.message.data
    results.value = (json.message?.data || []).map(org => ({
      name: org.name,
      organization_name: org.organization_name,
      custom_organization_owner: org.custom_organization_owner || 'N/A'
    }))
  } catch (err) {
    console.error('Search error:', err)
    error.value = err.message || String(err)
  } finally {
    loading.value = false
  }
}

// Debounced search while typing
watch(
  () => query.value,
  (val) => {
    if (debounceTimer) clearTimeout(debounceTimer)
    if (!val || !val.trim()) {
      results.value = []
      searched.value = false
      return
    }
    debounceTimer = setTimeout(() => {
      searchNow()
    }, DEBOUNCE_MS)
  }
)
</script>


<style scoped>
input::placeholder {
  color: #9aa0a6;
}
</style>
