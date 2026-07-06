<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import NotificationToast from './components/NotificationToast.vue'
import { store } from './store.js'

const route = useRoute()
const menuOpen = ref(false)

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function closeMenu() {
  menuOpen.value = false
}

// Close menu on route change
watch(() => route.path, () => {
  menuOpen.value = false
})

// Close menu when clicking outside
function handleOutsideClick(e) {
  if (menuOpen.value && !e.target.closest('.nav-container')) {
    menuOpen.value = false
  }
}

onMounted(() => {
  store.fetchStats()
  document.addEventListener('click', handleOutsideClick)
})

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
})
</script>

<template>
  <div class="min-h-screen w-full">
    <!-- Nav -->
    <nav class="nav-container fixed top-0 left-0 right-0 z-50"
         style="background: rgba(6,11,24,0.92); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(99,102,241,0.15);">

      <!-- Top bar -->
      <div class="flex items-center justify-between px-6 py-4">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2 no-underline" @click="closeMenu">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white font-black text-sm"
               style="background: linear-gradient(135deg, #4F46E5, #7C3AED);">E</div>
          <span class="font-bold text-lg text-white tracking-tight">EduPredict <span class="gradient-text">AI</span></span>
        </router-link>

        <!-- Desktop links -->
        <div class="desktop-links hidden lg:flex items-center gap-1">
          <router-link to="/"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/' ? 'text-white bg-indigo-600/20 border border-indigo-500/30' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >Home</router-link>
          <router-link to="/predict"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/predict' ? 'text-white bg-indigo-600/20 border border-indigo-500/30' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >Predictor</router-link>
          <router-link to="/database"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/database' ? 'text-white bg-indigo-600/20 border border-indigo-500/30' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >Database</router-link>
          <router-link to="/insights"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/insights' ? 'text-white bg-indigo-600/20 border border-indigo-500/30' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >Insights</router-link>
          <router-link to="/interventions"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/interventions' ? 'text-white bg-indigo-600/20 border border-indigo-500/30' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >Interventions</router-link>
          <router-link to="/about"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
            :class="$route.path === '/about' ? 'text-white bg-indigo-600/20 border border-indigo-500/30' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >About</router-link>
        </div>

        <!-- Hamburger button (mobile + tablet) -->
        <div class="flex items-center gap-2 shrink-0">
          <button
            id="hamburger-btn"
            class="hamburger-btn lg:hidden flex flex-col justify-center items-center w-10 h-10 rounded-lg transition-all duration-200"
            :class="menuOpen ? 'bg-indigo-600/20' : 'hover:bg-white/5'"
            @click.stop="toggleMenu"
            aria-label="Toggle navigation menu"
            :aria-expanded="menuOpen"
          >
            <span class="ham-bar" :class="{ 'rotate-45 translate-y-2': menuOpen }"></span>
            <span class="ham-bar my-1" :class="{ 'opacity-0 scale-x-0': menuOpen }"></span>
            <span class="ham-bar" :class="{ '-rotate-45 -translate-y-2': menuOpen }"></span>
          </button>
        </div>
      </div>

      <!-- Mobile / Tablet drawer -->
      <div
        class="mobile-menu lg:hidden overflow-hidden transition-all duration-300 ease-in-out"
        :style="menuOpen ? 'max-height: 500px; opacity: 1;' : 'max-height: 0; opacity: 0;'"
      >
        <div class="px-4 pb-4 flex flex-col gap-1 border-t"
             style="border-color: rgba(99,102,241,0.12);">

          <!-- Nav links -->
          <router-link to="/"
            class="mobile-link"
            :class="$route.path === '/' ? 'mobile-link--active' : ''"
            @click="closeMenu"
          >
            <svg class="w-4 h-4 mr-2 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            Home
          </router-link>
          <router-link to="/predict"
            class="mobile-link"
            :class="$route.path === '/predict' ? 'mobile-link--active' : ''"
            @click="closeMenu"
          >
            <svg class="w-4 h-4 mr-2 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
            Predictor
          </router-link>
          <router-link to="/database"
            class="mobile-link"
            :class="$route.path === '/database' ? 'mobile-link--active' : ''"
            @click="closeMenu"
          >
            <svg class="w-4 h-4 mr-2 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/></svg>
            Database
          </router-link>
          <router-link to="/insights"
            class="mobile-link"
            :class="$route.path === '/insights' ? 'mobile-link--active' : ''"
            @click="closeMenu"
          >
            <svg class="w-4 h-4 mr-2 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            Insights
          </router-link>
          <router-link to="/interventions"
            class="mobile-link"
            :class="$route.path === '/interventions' ? 'mobile-link--active' : ''"
            @click="closeMenu"
          >
            <svg class="w-4 h-4 mr-2 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
            Interventions
          </router-link>
          <router-link to="/about"
            class="mobile-link"
            :class="$route.path === '/about' ? 'mobile-link--active' : ''"
            @click="closeMenu"
          >
            <svg class="w-4 h-4 mr-2 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            About
          </router-link>

        </div>
      </div>
    </nav>

    <!-- Page content -->
    <main class="pt-20">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Global Notifications -->
    <NotificationToast />
  </div>
</template>

<style>
/* Page transitions */
.page-enter-active, .page-leave-active { transition: opacity 0.25s ease, transform 0.25s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to   { opacity: 0; transform: translateY(-10px); }

/* Hamburger bars */
.ham-bar {
  display: block;
  width: 22px;
  height: 2px;
  background: #cbd5e1;
  border-radius: 2px;
  transition: transform 0.3s ease, opacity 0.3s ease;
  transform-origin: center;
}

/* Mobile nav links */
.mobile-link {
  display: flex;
  align-items: center;
  padding: 0.65rem 0.875rem;
  margin-top: 0.25rem;
  border-radius: 0.625rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #94a3b8;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}

.mobile-link:hover {
  background: rgba(255,255,255,0.06);
  color: #fff;
}

.mobile-link--active {
  color: #fff !important;
  background: rgba(99,102,241,0.18) !important;
  border: 1px solid rgba(99,102,241,0.3);
}
</style>
