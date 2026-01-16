<template>
  <FrappeUIProvider>
    <Layout
      class="isolate"
      v-if="session().isLoggedIn"
    >
      <router-view :key="$route.fullPath" />
    </Layout>
    <Dialogs />
  </FrappeUIProvider>
</template>

<script setup>
import { Dialogs } from '@/utils/dialogs';
import { sessionStore as session } from '@/stores/session';
import { FrappeUIProvider, setConfig } from 'frappe-ui';
import { computed, defineAsyncComponent, onMounted } from 'vue';

const MobileLayout = defineAsyncComponent(() =>
  import('./components/Layouts/MobileLayout.vue')
);

const DesktopLayout = defineAsyncComponent(() =>
  import('./components/Layouts/DesktopLayout.vue')
);

const Layout = computed(() => {
  if (window.innerWidth < 640) {
    return MobileLayout;
  } else {
    return DesktopLayout;
  }
});

setConfig('systemTimezone', window.timezone?.system || null);
setConfig('localTimezone', window.timezone?.user || null);

//Force logout implementation when API fails
async function forceClearAll() {
  console.log('Before clear:')
  console.log('Cookies:', document.cookie)
  console.log('localStorage:', { ...localStorage })
  console.log('sessionStorage:', { ...sessionStorage })

  // Clear cookies
  document.cookie.split(';').forEach(cookie => {
    const eqPos = cookie.indexOf('=')
    const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'
    document.cookie =
      name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=' + location.hostname
  })

  // Clear storage
  localStorage.clear()
  sessionStorage.clear()

  console.log('After clear:')
  console.log('Cookies:', document.cookie)
  console.log('localStorage:', { ...localStorage })
  console.log('sessionStorage:', { ...sessionStorage })

  try {
    const base = window.location.origin

    // Fetch CSRF token explicitly
    const csrfResp = await fetch(`${base}/api/method/crm_override.api.get_csrf_token`, {
      method: 'GET',
      credentials: 'include',
      headers: { Accept: 'application/json' },
    })

    if (csrfResp.ok) {
      const csrfData = await csrfResp.json()
      const csrf_token = csrfData.message?.csrf_token

      if (csrf_token) {
        // Call logout with token
        const params = new URLSearchParams({ csrf_token })
        await fetch(
          `${base}/api/method/crm_override.api.force_logout?${params.toString()}`,
          {
            method: 'GET',
            credentials: 'include',
            headers: { Accept: 'application/json' },
          },
        )
      }
    }
  } catch (err) {
    console.warn('Force logout failed', err)
  }

  sessionStorage.setItem('logout_performed', '1')
  location.reload()
}

// Test CSRF token by making a POST request to an API endpoint
async function testCSRFToken() {
  try {
    const base = window.location.origin
    
    // Use the same endpoint that's causing the error in your app
    const endpoint = '/api/method/crm.api.views.get_views';
    
    console.log('Testing CSRF token with POST request to:', endpoint)
    
    const response = await fetch(`${base}${endpoint}`, {
      method: 'POST',
      credentials: 'include',
      headers: { 
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ doctype: {} })
    })

    console.log('Response status:', response.status)
    console.log('Response ok:', response.ok)
    
    if (response.ok) {
      const data = await response.json()
      console.log('CSRF test passed - API is okay:', data)
      return true
    } else {
      const errorText = await response.text()
      console.log('Response text:', errorText)
      
      try {
        const errorData = JSON.parse(errorText)
        console.log('Parsed error data:', errorData)
        
        // Check if it's a CSRF error specifically
        if (errorData.exc_type === 'CSRFTokenError') {
          console.warn('✅ CSRF error detected - token is invalid')
          return false
        } else {
          console.warn('Other error detected (not CSRF):', errorData.exc_type)
          return false // Also fail for other errors
        }
      } catch (parseError) {
        console.log('Could not parse error response:', parseError)
        return false
      }
    }
  } catch (error) {
    console.error('CSRF test failed with network error:', error)
    return false
  }
}

onMounted(async () => {
  if (sessionStorage.getItem('logout_performed') === '1') {
    console.log('Logout already performed, skipping check')
    sessionStorage.removeItem('logout_performed')
    return
  }

  console.log('Starting CSRF token check with POST request...')
  
  // Test CSRF token with a POST request
  const csrfValid = await testCSRFToken()
  
  console.log('CSRF check result:', csrfValid)
  
  if (!csrfValid) {
    console.warn('CSRF token is invalid, forcing logout...')
    await forceClearAll()
  } else {
    console.log('CSRF token is valid, no action needed.')
  }
})
</script>