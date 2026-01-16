<template>
  <TransitionRoot :show="sidebarOpened">
    <Dialog as="div" @close="closeSidebar" class="fixed inset-0 z-40">
      <TransitionChild
        as="template"
        enter="transition ease-in-out duration-200 transform"
        enter-from="-translate-x-full"
        enter-to="translate-x-0"
        leave="transition ease-in-out duration-200 transform"
        leave-from="translate-x-0"
        leave-to="-translate-x-full"
      >
        <div
          class="relative z-10 flex h-full w-[260px] flex-col justify-between border-r bg-surface-menu-bar transition-all duration-300 ease-in-out"
        >
          <div>
            <UserDropdown class="p-2" :isCollapsed="isCollapsed" />
          </div>
          <div class="flex-1 overflow-y-auto">
            <div class="mb-3 flex flex-col">
              <SidebarLink
                id="notifications-btn"
                :label="__('Notifications')"
                :icon="NotificationsIcon"
                :to="{ name: 'Notifications' }"
                :isCollapsed="isCollapsed"
                class="relative mx-2 my-0.5"
                @click="closeSidebar"
              >
                <template #right>
                  <Badge
                    v-if="unreadNotificationsCount"
                    :label="unreadNotificationsCount"
                    variant="subtle"
                  />
                </template>
              </SidebarLink>
            </div>
            <div v-for="view in allViews" :key="view.label">
              <Section
                :label="view.name"
                :hideLabel="view.hideLabel"
                :opened="view.opened"
              >
                <template #header="{ opened, hide, toggle }">
                  <div
                    v-if="!hide"
                    class="ml-2 mt-4 flex h-7 w-auto cursor-pointer gap-1.5 px-1 text-base font-medium text-ink-gray-5 opacity-100 transition-all duration-300 ease-in-out"
                    @click="toggle"
                  >
                    <FeatherIcon
                      name="chevron-right"
                      class="h-4 text-ink-gray-9 transition-all duration-300 ease-in-out"
                      :class="{ 'rotate-90': opened }"
                    />
                    <span>{{ __(view.name) }}</span>
                  </div>
                </template>
                <nav class="flex flex-col">
                  <SidebarLink
                    v-for="link in view.views"
                    :key="link.label"
                    :icon="link.icon"
                    :label="__(link.label)"
                    :to="link.to"
                    :isCollapsed="isCollapsed"
                    class="mx-2 my-0.5"
                    @click="closeSidebar"
                  />
                </nav>
              </Section>
            </div>
          </div>
          <div class="m-2 flex flex-col gap-1">
            <SidebarLink
              :label="__('Clear cookies & Logout')"
              :isCollapsed="isCollapsed"
              @click="handleLogout"
              class="mx-2 my-0.5"
            >
              <template #icon>
                <span class="grid h-4 w-4 flex-shrink-0 place-items-center">
                  <FeatherIcon
                    name="trash-2"
                    class="h-4 w-4 text-ink-gray-7"
                  />
                </span>
              </template>
            </SidebarLink>
          </div>
        </div>
      </TransitionChild>
      <TransitionChild
        as="template"
        enter="transition-opacity ease-linear duration-200"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity ease-linear duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <DialogOverlay class="fixed inset-0 bg-gray-600 bg-opacity-50" />
      </TransitionChild>
    </Dialog>
  </TransitionRoot>
  <TransitionRoot :show="showConfirmClearCookies">
    <Dialog
      as="div"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      @close="showConfirmClearCookies = false"
    >
      <div class="w-full max-w-sm rounded-lg bg-white p-6 shadow-lg">
        <h2 class="mb-4 text-lg font-semibold">{{ __('Confirm Clear Cookies') }}</h2>
        <p class="mb-6">{{ __('Are you sure you want to clear all cookies? This will refresh the page.') }}</p>
        <div class="flex justify-end gap-4">
          <button
            class="rounded bg-gray-200 px-4 py-2 hover:bg-gray-300"
            @click="showConfirmClearCookies = false"
          >
            {{ __('Cancel') }}
          </button>
          <button
            class="rounded bg-red-600 px-4 py-2 text-white hover:bg-red-700"
            @click="forceClearAll"
          >
            {{ __('Confirm') }}
          </button>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogOverlay,
} from '@headlessui/vue'
import Section from '@/components/Section.vue'
import Email2Icon from '@/components/Icons/Email2Icon.vue'
import PinIcon from '@/components/Icons/PinIcon.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import DealsIcon from '@/components/Icons/DealsIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import HelpIcon from '@/components/Icons/TaskIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import NotificationsIcon from '@/components/Icons/NotificationsIcon.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import { viewsStore } from '@/stores/views'
import { unreadNotificationsCount } from '@/stores/notifications'
import { TrialBanner } from 'frappe-ui/frappe'
import { mobileSidebarOpened as sidebarOpened } from '@/composables/settings'

const { getPinnedViews, getPublicViews } = viewsStore()
const showConfirmClearCookies = ref(false)
const isCollapsed = computed(() => !sidebarOpened.value)

const links = [
  { label: 'Leads', icon: LeadsIcon, to: 'Leads' },
  { label: 'Deals', icon: DealsIcon, to: 'Deals' },
  { label: 'Contacts', icon: ContactsIcon, to: 'Contacts' },
  { label: 'Organizations', icon: OrganizationsIcon, to: 'Organizations' },
  { label: 'Notes', icon: NoteIcon, to: 'Notes' },
  { label: 'Tasks', icon: TaskIcon, to: 'Tasks' },
  { label: 'Email Templates', icon: Email2Icon, to: 'Email Templates' },
  { label: 'Organization Search', icon: HelpIcon, to: 'Search' },
]

const allViews = computed(() => {
  const views = [
    {
      name: 'All Views',
      hideLabel: true,
      opened: true,
      views: links,
    },
  ]
  if (getPublicViews().length) {
    views.push({
      name: 'Public views',
      opened: true,
      views: parseView(getPublicViews()),
    })
  }
  if (getPinnedViews().length) {
    views.push({
      name: 'Pinned views',
      opened: true,
      views: parseView(getPinnedViews()),
    })
  }
  return views
})

function parseView(views) {
  return views.map((view) => ({
    label: view.label,
    icon: getIcon(view.route_name, view.icon),
    to: {
      name: view.route_name,
      params: { viewType: view.type || 'list' },
      query: { view: view.name },
    },
  }))
}

function getIcon(routeName, icon) {
  if (icon) return h('div', { class: 'size-auto' }, icon)
  switch (routeName) {
    case 'Leads':
      return LeadsIcon
    case 'Deals':
      return DealsIcon
    case 'Contacts':
      return ContactsIcon
    case 'Organizations':
      return OrganizationsIcon
    case 'Notes':
      return NoteIcon
    case 'Call Logs':
      return PhoneIcon
    default:
      return PinIcon
  }
}

function closeSidebar() {
  sidebarOpened.value = false
}

function handleLogout() {
  showConfirmClearCookies.value = true
}

async function forceClearAll() {
  try {
    // Clear cookies
    document.cookie.split(';').forEach((cookie) => {
      const name = cookie.split('=')[0].trim()
      document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`
      document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=${location.hostname}`
    })

    // Clear storages
    localStorage.clear()
    sessionStorage.clear()

    const base = window.location.origin

    // Fetch CSRF token
    const csrfResp = await fetch(`${base}/api/method/crm_override.api.get_csrf_token`, {
      method: 'GET',
      credentials: 'include',
      headers: { Accept: 'application/json' },
    })
    if (!csrfResp.ok) throw new Error(`CSRF fetch failed: ${csrfResp.status}`)
    const csrfData = await csrfResp.json()
    const csrf_token = csrfData.message?.csrf_token

    if (csrf_token) {
      // Call force logout API
      const params = new URLSearchParams({ csrf_token })
      const logoutResp = await fetch(`${base}/api/method/crm_override.api.force_logout?${params.toString()}`, {
        method: 'GET',
        credentials: 'include',
        headers: { Accept: 'application/json' },
      })
      if (!logoutResp.ok) throw new Error(`Logout failed: ${logoutResp.status}`)
    }
  } catch (err) {
    console.warn('Logout error:', err)
  } finally {
    showConfirmClearCookies.value = false
    closeSidebar()
    location.reload()
  }
}
</script>
