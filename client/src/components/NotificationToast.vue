<script setup>
import { store } from '../store.js'

const typeColors = {
  success: { bg: 'rgba(16,185,129,0.15)', border: 'rgba(16,185,129,0.4)', text: '#10B981', icon: '✅' },
  error:   { bg: 'rgba(239,68,68,0.15)',  border: 'rgba(239,68,68,0.4)',  text: '#EF4444', icon: '⚠️' },
  warning: { bg: 'rgba(245,158,11,0.15)', border: 'rgba(245,158,11,0.4)', text: '#F59E0B', icon: '🔔' },
  info:    { bg: 'rgba(99,102,241,0.15)', border: 'rgba(99,102,241,0.4)', text: '#A5B4FC', icon: 'ℹ️' }
}
</script>

<template>
  <div class="fixed top-24 right-6 z-[100] flex flex-col gap-3 pointer-events-none w-80">
    <TransitionGroup name="toast">
      <div 
        v-for="notification in store.notifications" 
        :key="notification.id"
        class="pointer-events-auto flex items-start gap-3 p-4 rounded-xl shadow-lg backdrop-blur-md transition-all duration-300"
        :style="`background: ${typeColors[notification.type].bg}; border: 1px solid ${typeColors[notification.type].border};`"
      >
        <span class="text-lg shrink-0 mt-0.5">{{ typeColors[notification.type].icon }}</span>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-white leading-snug">{{ notification.message }}</p>
        </div>
        <button 
          @click="store.removeNotification(notification.id)" 
          class="shrink-0 text-slate-400 hover:text-white transition-colors p-1 -m-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(50px) scale(0.95);
}
.toast-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
