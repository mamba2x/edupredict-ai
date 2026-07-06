<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'
import { store } from '../store.js'
import { Bar, Doughnut, Radar, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale,
  ArcElement, RadialLinearScale,
  PointElement, LineElement, Filler,
} from 'chart.js'

ChartJS.register(
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale,
  ArcElement, RadialLinearScale,
  PointElement, LineElement, Filler,
)

const API = 'http://localhost:8000'

const data    = ref(null)
const loading = ref(true)
const error   = ref('')
const activeFilter = ref('All')
const searchQuery = ref('')
const chartsReady = ref(false)

const filters = ['All', 'Excellent', 'Average', 'At-Risk']

async function fetchInsights() {
  try {
    const res = await api.get('/insights')
    data.value = res.data
  } catch (e) {
    error.value = 'Could not load insights. Please make sure the server is running and train.py has been executed.'
  } finally {
    loading.value = false
    // Delay rendering charts until page transition is complete
    setTimeout(() => {
      chartsReady.value = true
    }, 350)
  }
}

onMounted(fetchInsights)

// Sort models by accuracy descending and apply filters
const sortedModels = computed(() => {
  if (!data.value) return []
  let models = [...data.value.model_comparison]
  
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    models = models.filter(m => m.name.toLowerCase().includes(q))
  }
  
  return models.sort((a, b) => b.accuracy - a.accuracy)
})

// Normalise feature importances
const normalisedFeatures = computed(() => {
  if (!data.value?.feature_importance?.length) return []
  const max = data.value.feature_importance[0].importance
  return data.value.feature_importance.map(f => ({
    ...f,
    pct: max > 0 ? Math.round((f.importance / max) * 100) : 0,
  }))
})

// Class distribution computed
const classDist = computed(() => {
  if (!data.value?.class_distribution) return []
  const total = Object.values(data.value.class_distribution).reduce((a, b) => a + b, 0)
  const colors = { Excellent: '#10B981', Average: '#F59E0B', 'At-Risk': '#EF4444' }
  return Object.entries(data.value.class_distribution).map(([cls, count]) => ({
    cls,
    count,
    pct: Math.round((count / total) * 100),
    color: colors[cls] || '#6366F1',
  }))
})

// Live Store Risk Rings
const liveRiskDist = computed(() => {
  const total = store.stats.total_students || 1
  return [
    { cls: 'Excellent', count: store.stats.excellent_count, pct: Math.round((store.stats.excellent_count / total) * 100) || 0, color: '#10B981' },
    { cls: 'Average', count: store.stats.average_count, pct: Math.round((store.stats.average_count / total) * 100) || 0, color: '#F59E0B' },
    { cls: 'At-Risk', count: store.stats.at_risk_count, pct: Math.round((store.stats.at_risk_count / total) * 100) || 0, color: '#EF4444' }
  ]
})

// ── Chart.js Data ───────────────────────────────────────────────────────────

const doughnutData = computed(() => {
  const bgColors = {
    Excellent: 'rgba(16,185,129,0.8)',
    Average: 'rgba(245,158,11,0.8)',
    'At-Risk': 'rgba(239,68,68,0.8)'
  }
  const borderColors = {
    Excellent: '#10B981',
    Average: '#F59E0B',
    'At-Risk': '#EF4444'
  }
  
  return {
    labels: classDist.value.map(c => c.cls),
    datasets: [{
      data: classDist.value.map(c => c.count),
      backgroundColor: classDist.value.map(c => (activeFilter.value === 'All' || activeFilter.value === c.cls) ? bgColors[c.cls] : 'rgba(255,255,255,0.05)'),
      borderColor: classDist.value.map(c => (activeFilter.value === 'All' || activeFilter.value === c.cls) ? borderColors[c.cls] : 'transparent'),
      borderWidth: 2,
      hoverOffset: 8,
    }],
  }
})

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: '#94A3B8', font: { size: 12 }, padding: 16 },
    },
    tooltip: {
      callbacks: {
        label: ctx => ` ${ctx.label}: ${ctx.parsed} students`,
      },
    },
  },
}

const featureBarData = computed(() => ({
  labels: normalisedFeatures.value.map(f => f.feature.replace(/_/g, ' ')),
  datasets: [{
    label: 'Relative Importance',
    data: normalisedFeatures.value.map(f => f.pct),
    backgroundColor: normalisedFeatures.value.map((_, i) => `hsla(${240 + i * 20},70%,65%,0.75)`),
    borderColor: normalisedFeatures.value.map((_, i) => `hsl(${240 + i * 20},70%,65%)`),
    borderWidth: 1,
    borderRadius: 6,
    borderSkipped: false,
  }],
}))

const featureBarOptions = {
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: { label: ctx => ` ${ctx.parsed.x}% of max importance` },
    },
  },
  scales: {
    x: {
      grid: { color: 'rgba(255,255,255,0.05)' },
      ticks: { color: '#64748B', font: { size: 11 } },
      max: 100,
    },
    y: {
      grid: { display: false },
      ticks: { color: '#94A3B8', font: { size: 11 } },
    },
  },
}

const modelRadarData = computed(() => ({
  labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
  datasets: sortedModels.value.map((m, i) => {
    const colors = ['#6366F1', '#10B981', '#F59E0B', '#EF4444']
    return {
      label: m.name,
      data: [m.accuracy * 100, m.precision * 100, m.recall * 100, m.f1_score * 100],
      borderColor: colors[i],
      backgroundColor: colors[i] + '22',
      pointBackgroundColor: colors[i],
      borderWidth: 2,
      pointRadius: 4,
    }
  }),
}))

const radarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: '#94A3B8', font: { size: 11 }, padding: 12 },
    },
  },
  scales: {
    r: {
      min: 60,
      max: 100,
      grid: { color: 'rgba(255,255,255,0.07)' },
      angleLines: { color: 'rgba(255,255,255,0.07)' },
      ticks: { color: '#475569', backdropColor: 'transparent', font: { size: 10 } },
      pointLabels: { color: '#94A3B8', font: { size: 11 } },
    },
  },
}

// Live Previous CGPA vs. Outcome — pulled from store.stats (backend /stats endpoint)
const cgpaLineData = computed(() => {
  const buckets = store.stats.cgpa_vs_outcome
  if (!buckets || buckets.length === 0) {
    return { labels: ['< 1.5', '1.5–2.5', '2.5–3.5', '3.5–4.5', '≥ 4.5'], datasets: [] }
  }
  return {
    labels: buckets.map(b => b.label),
    datasets: [
      {
        label: 'Excellent %',
        data: buckets.map(b => b.excellent),
        borderColor: '#10B981',
        backgroundColor: 'rgba(16,185,129,0.1)',
        fill: true, tension: 0.4, pointRadius: 5, pointBackgroundColor: '#10B981',
      },
      {
        label: 'Average %',
        data: buckets.map(b => b.average),
        borderColor: '#F59E0B',
        backgroundColor: 'rgba(245,158,11,0.1)',
        fill: true, tension: 0.4, pointRadius: 5, pointBackgroundColor: '#F59E0B',
      },
      {
        label: 'At-Risk %',
        data: buckets.map(b => b.atRisk),
        borderColor: '#EF4444',
        backgroundColor: 'rgba(239,68,68,0.1)',
        fill: true, tension: 0.4, pointRadius: 5, pointBackgroundColor: '#EF4444',
      },
    ],
  }
})

// Live Study Hours vs. Outcome — pulled from store.stats (backend /stats endpoint)
const studyHoursLineData = computed(() => {
  const buckets = store.stats.study_hours_vs_outcome
  if (!buckets || buckets.length === 0) {
    return { labels: ['< 5 hrs', '5-10 hrs', '10-15 hrs', '15-20 hrs', '20-25 hrs', '> 25 hrs'], datasets: [] }
  }
  return {
    labels: buckets.map(b => b.label),
    datasets: [
      {
        label: 'Excellent %',
        data: buckets.map(b => b.excellent),
        borderColor: '#10B981', backgroundColor: 'rgba(16,185,129,0.1)',
        fill: true, tension: 0.4, pointRadius: 5, pointBackgroundColor: '#10B981',
        hidden: activeFilter.value !== 'All' && activeFilter.value !== 'Excellent'
      },
      {
        label: 'Average %',
        data: buckets.map(b => b.average),
        borderColor: '#F59E0B', backgroundColor: 'rgba(245,158,11,0.1)',
        fill: true, tension: 0.4, pointRadius: 5, pointBackgroundColor: '#F59E0B',
        hidden: activeFilter.value !== 'All' && activeFilter.value !== 'Average'
      },
      {
        label: 'At-Risk %',
        data: buckets.map(b => b.atRisk),
        borderColor: '#EF4444', backgroundColor: 'rgba(239,68,68,0.1)',
        fill: true, tension: 0.4, pointRadius: 5, pointBackgroundColor: '#EF4444',
        hidden: activeFilter.value !== 'All' && activeFilter.value !== 'At-Risk'
      },
    ],
  }
})

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { color: '#94A3B8', font: { size: 11 }, padding: 12 },
    },
    tooltip: {
      mode: 'index',
      intersect: false,
    },
  },
  scales: {
    x: {
      grid: { color: 'rgba(255,255,255,0.05)' },
      ticks: { color: '#64748B', font: { size: 11 } },
    },
    y: {
      grid: { color: 'rgba(255,255,255,0.05)' },
      ticks: { color: '#64748B', font: { size: 11 }, callback: v => v + '%' },
      max: 100,
    },
  },
}

// ── Export ──────────────────────────────────────────────────────────────────
function exportData() {
  if (!data.value) return
  const blob = new Blob([JSON.stringify(data.value, null, 2)], { type: 'application/json' })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href     = url
  a.download = 'edupredict_insights.json'
  a.click()
  URL.revokeObjectURL(url)
}

const metricBg    = v => v >= 0.9 ? 'rgba(16,185,129,0.15)' : v >= 0.75 ? 'rgba(99,102,241,0.15)' : 'rgba(245,158,11,0.12)'
const metricColor = v => v >= 0.9 ? '#10B981' : v >= 0.75 ? '#A5B4FC' : '#F59E0B'
</script>

<template>
  <div class="min-h-screen px-6 py-10 max-w-7xl mx-auto">

    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10 anim-fade-up">
      <div>
        <h1 class="text-4xl md:text-5xl font-black text-white mb-3">
          Model <span class="gradient-text">Insights</span>
        </h1>
        <p class="text-slate-400 max-w-lg">Compare algorithm performance and understand which factors drive predictions.</p>
      </div>
      <div class="flex gap-4">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search models..." 
          class="form-input md:w-64"
        />
        <button
          v-if="data"
          @click="exportData"
          class="btn-ghost text-sm flex items-center gap-2 shrink-0"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          Export JSON
        </button>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div v-if="data" class="flex gap-2 mb-8 flex-wrap anim-fade-up">
      <button
        v-for="f in filters" :key="f"
        @click="activeFilter = f"
        class="px-4 py-1.5 rounded-full text-sm font-semibold border transition-all duration-200"
        :class="activeFilter === f
          ? 'bg-indigo-600 text-white border-indigo-500 shadow-[0_0_12px_rgba(99,102,241,0.3)]'
          : 'text-slate-400 border-white/10 hover:text-white hover:border-white/20'"
      >{{ f }}</button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center py-24 gap-4">
      <div class="w-14 h-14 border-2 border-indigo-500/30 border-t-indigo-400 rounded-full anim-spin"></div>
      <p class="text-slate-400">Loading insights from server…</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="max-w-xl mx-auto glass-card p-8 text-center">
      <div class="text-5xl mb-4">⚠️</div>
      <p class="text-slate-300 leading-relaxed">{{ error }}</p>
    </div>

    <div v-else-if="data" class="flex flex-col gap-8">

      <!-- ── Live Risk Summary ──────────────────────────── -->
      <div v-if="store.stats.total_students > 0" class="glass-card p-6 anim-fade-up">
        <h2 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span class="w-7 h-7 rounded-lg bg-pink-600/20 border border-pink-500/30 flex items-center justify-center text-xs">🌐</span>
          Live Distribution (From Database)
          <span class="ml-auto text-xs px-2 py-0.5 rounded-full font-semibold"
                style="background:rgba(16,185,129,0.12);color:#10B981;border:1px solid rgba(16,185,129,0.25);">Live</span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="c in liveRiskDist" :key="c.cls" class="flex items-center gap-4 bg-white/5 rounded-xl p-4 border border-white/10">
            <!-- Ring -->
            <div class="relative w-16 h-16 shrink-0">
              <svg class="w-16 h-16 -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="12"/>
                <circle cx="50" cy="50" r="42" fill="none"
                        :stroke="c.color" stroke-width="12"
                        stroke-linecap="round"
                        :stroke-dasharray="264"
                        :stroke-dashoffset="264 - (264 * c.pct / 100)"
                        class="anim-ring-fill"
                        style="transition:stroke-dashoffset 1.4s cubic-bezier(0.4,0,0.2,1);"/>
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-xs font-black text-white">{{ c.pct }}%</span>
              </div>
            </div>
            <!-- Details -->
            <div>
              <div class="text-lg font-bold" :style="{ color: c.color }">{{ c.cls }}</div>
              <div class="text-sm text-slate-400">{{ c.count }} students</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state for live distribution when no DB records -->
      <div v-else class="glass-card p-10 text-center anim-fade-up"
           style="border: 1px dashed rgba(99,102,241,0.3); background: rgba(99,102,241,0.04);">
        <div class="text-4xl mb-3">🌐</div>
        <h3 class="text-lg font-bold text-white mb-2">No Live Data Yet</h3>
        <p class="text-slate-400 text-sm max-w-sm mx-auto mb-4">Model insights below are based on training data. Upload a student dataset to populate live prediction analytics.</p>
        <router-link to="/predict" class="btn-ghost text-sm">⚡ Upload Dataset →</router-link>
      </div>

      <!-- ── Dataset Summary ────────────────────────────────── -->

      <div class="glass-card p-6 anim-fade-up delay-1">
        <h2 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span class="w-7 h-7 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-xs">📋</span>
          Dataset Summary
        </h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-4 rounded-xl" style="background: rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);">
            <div class="text-2xl font-black text-white">{{ data.dataset_info?.total_records?.toLocaleString() }}</div>
            <div class="text-xs text-slate-400 mt-1">Total Records</div>
          </div>
          <div class="text-center p-4 rounded-xl" style="background: rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);">
            <div class="text-2xl font-black text-white">{{ data.dataset_info?.train_records?.toLocaleString() }}</div>
            <div class="text-xs text-slate-400 mt-1">Training Set</div>
          </div>
          <div class="text-center p-4 rounded-xl" style="background: rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);">
            <div class="text-2xl font-black text-white">{{ data.dataset_info?.test_records?.toLocaleString() }}</div>
            <div class="text-xs text-slate-400 mt-1">Test Set</div>
          </div>
          <div class="text-center p-4 rounded-xl" style="background: rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25);">
            <div class="text-2xl font-black text-emerald-400">{{ data.best_model_name?.split(' ')[0] }}</div>
            <div class="text-xs text-slate-400 mt-1">Best Algorithm</div>
          </div>
        </div>
      </div>

      <!-- ── Row 2: Charts ────────────────────── -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 anim-fade-up delay-1">

        <!-- Previous CGPA vs Performance -->
        <div class="glass-card p-6 flex flex-col">
          <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
            <span class="w-7 h-7 rounded-lg bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-xs">🎓</span>
            Previous CGPA vs. Outcome
          </h2>
          <p class="text-slate-500 text-xs mb-4">How prior CGPA bands (out of 5.0) correlate with predicted class distribution.</p>
          <div style="height:240px;" class="relative">
            <Line v-if="chartsReady" :data="cgpaLineData" :options="lineOptions" />
            <div v-else class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/20 rounded-xl border border-white/5 gap-3">
              <div class="w-8 h-8 border-2 border-indigo-500/20 border-t-indigo-500 rounded-full anim-spin"></div>
              <span class="text-xs text-slate-500">Preparing visualization...</span>
            </div>
          </div>
        </div>
        
        <!-- Study Hours vs Performance -->
        <div class="glass-card p-6 flex flex-col">
          <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
            <span class="w-7 h-7 rounded-lg bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-xs">⏰</span>
            Study Hours vs. Outcome
          </h2>
          <p class="text-slate-500 text-xs mb-4">How weekly study hours impact the predicted outcome.</p>
          <div style="height:240px;" class="relative">
            <Line v-if="chartsReady" :data="studyHoursLineData" :options="lineOptions" />
            <div v-else class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/20 rounded-xl border border-white/5 gap-3">
              <div class="w-8 h-8 border-2 border-indigo-500/20 border-t-indigo-500 rounded-full anim-spin"></div>
              <span class="text-xs text-slate-500">Preparing visualization...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Row 3: Feature Bar + Doughnut + Radar ────────────────────── -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 anim-fade-up delay-2">
        
        <!-- Model Radar Chart -->
        <div class="glass-card p-6 flex flex-col">
          <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
            <span class="w-7 h-7 rounded-lg bg-violet-600/20 border border-violet-500/30 flex items-center justify-center text-xs">🤖</span>
            Model Comparison
          </h2>
          <div style="height:260px;" class="relative">
            <Radar v-if="chartsReady" :data="modelRadarData" :options="radarOptions" />
            <div v-else class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/20 rounded-xl border border-white/5 gap-3">
              <div class="w-8 h-8 border-2 border-indigo-500/20 border-t-indigo-500 rounded-full anim-spin"></div>
              <span class="text-xs text-slate-500">Preparing model comparison...</span>
            </div>
          </div>
        </div>

        <!-- Feature Importance Bar Chart -->
        <div class="glass-card p-6 flex flex-col">
          <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
            <span class="w-7 h-7 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-xs">🔬</span>
            Feature Importance
          </h2>
          <div style="height:260px;" class="relative">
            <Bar v-if="chartsReady" :data="featureBarData" :options="featureBarOptions" />
            <div v-else class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/20 rounded-xl border border-white/5 gap-3">
              <div class="w-8 h-8 border-2 border-indigo-500/20 border-t-indigo-500 rounded-full anim-spin"></div>
              <span class="text-xs text-slate-500">Analyzing feature weights...</span>
            </div>
          </div>
        </div>

        <!-- Class Distribution Doughnut -->
        <div class="glass-card p-6 flex flex-col">
          <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
            <span class="w-7 h-7 rounded-lg bg-orange-600/20 border border-orange-500/30 flex items-center justify-center text-xs">📊</span>
            Class Distribution
          </h2>
          <div style="height:200px;" class="mb-4 relative">
            <Doughnut v-if="chartsReady" :data="doughnutData" :options="doughnutOptions" />
            <div v-else class="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/20 rounded-xl border border-white/5 gap-3">
              <div class="w-8 h-8 border-2 border-indigo-500/20 border-t-indigo-500 rounded-full anim-spin"></div>
              <span class="text-xs text-slate-500">Structuring cohort distribution...</span>
            </div>
          </div>
          <!-- Stat pills -->
          <div class="grid grid-cols-3 gap-3 mt-auto">
            <div v-for="c in classDist" :key="c.cls"
                 class="text-center p-3 rounded-xl"
                 :style="{ background: c.color + '12', border: `1px solid ${c.color}33` }">
              <div class="text-xl font-black" :style="{ color: c.color }">{{ c.pct }}%</div>
              <div class="text-xs text-slate-400 mt-0.5">{{ c.cls }}</div>
              <div class="text-xs text-slate-500">{{ c.count.toLocaleString() }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Model Metrics Detail ──────────────────────────────── -->
      <div class="glass-card p-6 anim-fade-up delay-3">
        <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
          <span class="w-7 h-7 rounded-lg bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-xs">📐</span>
          Detailed Model Metrics
        </h2>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-left border-b border-white/10">
                <th class="pb-3 text-slate-400 font-semibold">Algorithm</th>
                <th class="pb-3 text-slate-400 font-semibold text-center">Accuracy</th>
                <th class="pb-3 text-slate-400 font-semibold text-center">Precision</th>
                <th class="pb-3 text-slate-400 font-semibold text-center">Recall</th>
                <th class="pb-3 text-slate-400 font-semibold text-center">F1-Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(m, i) in sortedModels" :key="m.name"
                  class="border-b border-white/5 transition-colors hover:bg-white/3"
                  :class="i === 0 ? 'bg-emerald-500/5' : ''">
                <td class="py-3 font-semibold text-white flex items-center gap-2">
                  <span v-if="i === 0" class="text-xs px-2 py-0.5 rounded-full font-bold"
                        style="background: rgba(16,185,129,0.15); color: #10B981;">BEST</span>
                  {{ m.name }}
                </td>
                <td class="py-3 text-center">
                  <span class="font-black" :style="{ color: metricColor(m.accuracy) }">
                    {{ (m.accuracy * 100).toFixed(1) }}%
                  </span>
                </td>
                <td class="py-3 text-center">
                  <span class="text-xs px-2.5 py-1 rounded-lg font-bold"
                        :style="{ background: metricBg(m.precision), color: metricColor(m.precision) }">
                    {{ (m.precision * 100).toFixed(1) }}%
                  </span>
                </td>
                <td class="py-3 text-center">
                  <span class="text-xs px-2.5 py-1 rounded-lg font-bold"
                        :style="{ background: metricBg(m.recall), color: metricColor(m.recall) }">
                    {{ (m.recall * 100).toFixed(1) }}%
                  </span>
                </td>
                <td class="py-3 text-center">
                  <span class="text-xs px-2.5 py-1 rounded-lg font-bold"
                        :style="{ background: metricBg(m.f1_score), color: metricColor(m.f1_score) }">
                    {{ (m.f1_score * 100).toFixed(1) }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>
