<script setup>
import { computed } from 'vue'
import { store } from '../store.js'

const formatTimeAgo = (timestamp) => {
  if (!timestamp) return 'Just now'
  
  // Try to parse SQLite timestamp
  const date = new Date(timestamp.replace(' ', 'T') + 'Z') // Basic UTC assumption
  const now = new Date()
  const diffInMinutes = Math.floor((now - date) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes} min ago`
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)} hr ago`
  return `${Math.floor(diffInMinutes / 1440)} d ago`
}

const statusMap = {
  'Excellent': { risk: 'low', icon: '🌟' },
  'Average': { risk: 'medium', icon: '📘' },
  'At-Risk': { risk: 'high', icon: '⚠️' }
}

const activities = computed(() => {
  if (!store.stats.recent_predictions || store.stats.recent_predictions.length === 0) {
    return []
  }
  return store.stats.recent_predictions.map((p, i) => {
    const s = statusMap[p.predicted_status] || { risk: 'medium', icon: '❓' }
    return {
      id: p.id,
      name: `Student #${p.id} (${p.age}y ${p.gender.charAt(0)})`,
      outcome: p.predicted_status,
      time: formatTimeAgo(p.timestamp),
      risk: s.risk,
      icon: s.icon,
      index: i
    }
  })
})

const riskColor = (r) =>
  r === 'low' ? '#10B981' : r === 'high' ? '#EF4444' : '#F59E0B'
</script>

<template>
  <div class="flex flex-col gap-2">
    <div
      v-for="a in activities"
      :key="a.id"
      class="flex items-center gap-3 p-3 rounded-xl transition-all duration-200 hover:bg-white/[0.03] group anim-fade-up"
      :class="`delay-${Math.min(a.index + 1, 5)}`"
      style="border: 1px solid transparent;"
    >
      <!-- Avatar -->
      <div
        class="w-9 h-9 rounded-full flex items-center justify-center text-sm font-black shrink-0"
        :style="`background: ${riskColor(a.risk)}18; border: 1px solid ${riskColor(a.risk)}33; color: ${riskColor(a.risk)};`"
      >
        {{ a.name.split(' ').map(n => n[0]).join('') }}
      </div>

      <!-- Info -->
      <div class="flex-1 min-w-0">
        <div class="text-sm font-semibold text-white truncate">{{ a.name }}</div>
        <div class="text-xs text-slate-500">{{ a.time }}</div>
      </div>

      <!-- Outcome badge -->
      <span
        class="text-xs font-bold px-2 py-0.5 rounded-full shrink-0"
        :style="`background:${riskColor(a.risk)}15; color:${riskColor(a.risk)}; border:1px solid ${riskColor(a.risk)}33;`"
      >
        {{ a.icon }} {{ a.outcome }}
      </span>
    </div>
    <div v-if="activities.length === 0" class="text-sm text-slate-500 text-center py-4">
      No recent predictions found.
    </div>
  </div>
</template>
