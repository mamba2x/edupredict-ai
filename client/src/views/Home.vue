<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store.js'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  BarElement, CategoryScale, LinearScale,
  Tooltip, Legend
} from 'chart.js'
import StatCard from '../components/StatCard.vue'
import RecentActivity from '../components/RecentActivity.vue'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const router = useRouter()

const stats = computed(() => [
  { value: store.stats.total_students || 0,                          label: 'Total Prediction Records', icon: '👥', color: '#6366F1', trend: '', trendUp: true  },
  { value: (store.stats.avg_cgpa || 0).toFixed(2) + ' / 5.00',       label: 'Avg Previous CGPA',        icon: '🎓', color: '#8B5CF6', trend: '', trendUp: true  },
  { value: store.stats.at_risk_count || 0,                          label: 'At-Risk Students',         icon: '⚠️', color: '#EF4444', trend: '', trendUp: false },
  { value: (store.stats.avg_ca || 0).toFixed(1) + ' / 30',         label: 'Avg CA Score',             icon: '📝', color: '#10B981', trend: '', trendUp: true  },
])

const quickActions = [
  { label: 'Run Prediction',    icon: '⚡', route: '/predict',       color: '#6366F1' },
  { label: 'View Insights',     icon: '📊', route: '/insights',      color: '#8B5CF6' },
  { label: 'Interventions',     icon: '🎯', route: '/interventions', color: '#10B981' },
  { label: 'Student Database',  icon: '🗃️', route: '/database',      color: '#06B6D4' },
]

const chartData = computed(() => {
  const vol = store.stats.weekly_volume || { "Excellent": [0,0,0,0,0,0,0], "Average": [0,0,0,0,0,0,0], "At-Risk": [0,0,0,0,0,0,0] }
  return {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Excellent',
        data: vol['Excellent'],
        backgroundColor: 'rgba(16,185,129,0.7)',
        borderRadius: 6,
      },
      {
        label: 'Average',
        data: vol['Average'],
        backgroundColor: 'rgba(99,102,241,0.7)',
        borderRadius: 6,
      },
      {
        label: 'At-Risk',
        data: vol['At-Risk'],
        backgroundColor: 'rgba(239,68,68,0.6)',
        borderRadius: 6,
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: { color: '#94A3B8', font: { family: 'Inter', size: 12 }, boxWidth: 12, padding: 16 },
    },
    tooltip: {
      backgroundColor: 'rgba(13,20,45,0.95)',
      borderColor: 'rgba(99,102,241,0.3)',
      borderWidth: 1,
      titleColor: '#E2E8F0',
      bodyColor: '#94A3B8',
    },
  },
  scales: {
    x: {
      ticks: { color: '#64748B', font: { family: 'Inter', size: 11 } },
      grid:  { color: 'rgba(255,255,255,0.04)' },
    },
    y: {
      ticks: { color: '#64748B', font: { family: 'Inter', size: 11 } },
      grid:  { color: 'rgba(255,255,255,0.04)' },
      beginAtZero: true,
    },
  },
}

const aiInsights = [
  { text: 'Weak CA Count is the strongest predictor of academic performance — accounting for 100% of relative feature importance in the trained Random Forest model.',  color: '#10B981' },
  { text: 'Core Course CA Average is the second most influential factor, contributing 91.8% of relative importance, confirming that performance in compulsory CS courses drives outcomes.',        color: '#6366F1' },
  { text: '14.1% of students in the training dataset are classified as At-Risk, with Average being the dominant group at 57.6% and Excellent at 28.3%.',                   color: '#F59E0B' },
  { text: 'Random Forest is the best-performing model, achieving 100% accuracy and 1.000 F1-Score on the 224-record test set — outperforming Logistic Regression, Gradient Boosting, and SVM.',       color: '#8B5CF6' },
]

const visible = ref(false)
onMounted(() => setTimeout(() => (visible.value = true), 80))
</script>

<template>
  <div class="min-h-screen">

    <!-- ── Hero ──────────────────────────────────────────────────── -->
    <section class="relative flex flex-col items-center justify-center text-center px-6 pt-24 pb-16 overflow-hidden">
      <!-- Decorative orbs -->
      <div class="absolute top-16 left-1/4 w-80 h-80 rounded-full pointer-events-none"
           style="background:radial-gradient(circle,rgba(99,102,241,0.18) 0%,transparent 70%);filter:blur(50px);"
           :class="visible ? 'anim-float' : 'opacity-0'"></div>
      <div class="absolute bottom-10 right-1/4 w-64 h-64 rounded-full pointer-events-none"
           style="background:radial-gradient(circle,rgba(139,92,246,0.14) 0%,transparent 70%);filter:blur(40px);"
           :class="visible ? 'anim-float delay-3' : 'opacity-0'"></div>
      <div class="absolute inset-0 pointer-events-none"
           style="background:radial-gradient(ellipse 60% 50% at 50% 0%,rgba(99,102,241,0.08) 0%,transparent 70%);"></div>

      <!-- Badge -->
      <div class="anim-fade-up inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold mb-6"
           style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.3);color:#A5B4FC;">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 anim-pulse inline-block"></span>
        AI-Powered · Academic Intelligence Platform
      </div>

      <!-- Headline -->
      <h1 class="anim-fade-up delay-1 text-5xl md:text-7xl font-black tracking-tight leading-tight text-white mb-4">
        Intelligent Academic<br/>
        <span class="gradient-text">Performance Analytics</span>
      </h1>

      <p class="anim-fade-up delay-2 text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
        A university-grade AI platform that predicts student outcomes, identifies at-risk learners, and recommends personalised interventions — powered by 4 ML algorithms trained on real academic data.
      </p>

      <!-- CTAs -->
      <div class="anim-fade-up delay-3 flex flex-wrap gap-4 justify-center">
        <button class="btn-primary text-base px-8 py-3.5" @click="router.push('/predict')">
          ⚡ Run a Prediction
        </button>
        <button class="btn-ghost" @click="router.push('/insights')">
          📊 View Analytics
        </button>
        <button class="btn-ghost" @click="router.push('/database')">
          🗃️ Student Database
        </button>
      </div>
    </section>

    <!-- ── Stat Cards ────────────────────────────────────────────── -->
    <section class="px-6 pb-10 max-w-6xl mx-auto">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          v-for="(s, i) in stats" :key="s.label"
          :value="s.value" :label="s.label" :icon="s.icon"
          :color="s.color" :trend="s.trend" :trendUp="s.trendUp"
          class="anim-fade-up"
          :class="`delay-${i + 1}`"
        />
      </div>
    </section>

    <!-- ── Main Content Grid ─────────────────────────────────────── -->
    <template v-if="store.stats.total_students > 0">
      <section class="px-6 pb-12 max-w-6xl mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Weekly Performance Chart (spans 2 cols) -->
        <div class="glass-card p-6 lg:col-span-2 anim-slide-left">
          <div class="flex items-center justify-between mb-5">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-base">📊</div>
              <div>
                <h3 class="font-bold text-white">Weekly Prediction Volume</h3>
                <p class="text-slate-400 text-xs">Outcomes classified per day this week</p>
              </div>
            </div>
            <span class="text-xs px-2 py-1 rounded-lg text-indigo-300" style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.2);">Live</span>
          </div>
          <div style="height:220px;">
            <Bar :data="chartData" :options="chartOptions" />
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="glass-card p-6 anim-slide-right">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-9 h-9 rounded-lg bg-violet-600/20 border border-violet-500/30 flex items-center justify-center text-base">🚀</div>
            <h3 class="font-bold text-white">Quick Actions</h3>
          </div>
          <div class="flex flex-col gap-3">
            <button
              v-for="qa in quickActions" :key="qa.label"
              class="flex items-center gap-3 p-3.5 rounded-xl text-left transition-all duration-200 hover:scale-[1.02] group"
              :style="`background:${qa.color}10;border:1px solid ${qa.color}28;`"
              @click="router.push(qa.route)"
            >
              <span class="text-xl">{{ qa.icon }}</span>
              <span class="text-sm font-semibold text-slate-200 group-hover:text-white transition-colors">{{ qa.label }}</span>
              <span class="ml-auto text-slate-500 group-hover:text-slate-300 transition-colors text-sm">→</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Recent Activity + AI Insights ────────────────────────── -->
    <section class="px-6 pb-16 max-w-6xl mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Recent Activity -->
        <div class="glass-card p-6 anim-fade-up">
          <div class="flex items-center justify-between mb-5">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-base">🕐</div>
              <div>
                <h3 class="font-bold text-white">Recent Predictions</h3>
                <p class="text-slate-400 text-xs">Latest student analyses</p>
              </div>
            </div>
            <button class="btn-ghost text-xs py-1.5 px-3" @click="router.push('/database')">View All</button>
          </div>
          <RecentActivity />
        </div>

        <!-- AI Insights Panel -->
        <div class="glass-card p-6 anim-fade-up delay-2">
          <div class="flex items-center gap-3 mb-5">
            <div class="w-9 h-9 rounded-lg bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-base">🧠</div>
            <div>
              <h3 class="font-bold text-white">AI System Insights</h3>
              <p class="text-slate-400 text-xs">Patterns detected across the dataset</p>
            </div>
          </div>
          <div class="flex flex-col gap-3">
            <div
              v-for="(ins, i) in aiInsights" :key="i"
              class="flex gap-3 p-4 rounded-xl text-sm leading-relaxed anim-fade-up"
              :class="`delay-${i + 1}`"
              :style="`background:${ins.color}0d;border:1px solid ${ins.color}22;`"
            >
              <span class="shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center text-xs font-black"
                    :style="`background:${ins.color}22;color:${ins.color};`">{{ i + 1 }}</span>
              <span class="text-slate-300">{{ ins.text }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

  </template>

  <!-- ── Empty State (No Dataset) ─────────────────────────────────── -->
  <template v-else>
    <section class="px-6 pb-12 max-w-6xl mx-auto">
      <div class="glass-card p-16 text-center anim-fade-up"
           style="border: 1px dashed rgba(99,102,241,0.35); background: rgba(99,102,241,0.04);">
        <!-- Animated icon -->
        <div class="w-24 h-24 rounded-2xl flex items-center justify-center text-5xl mx-auto mb-6 anim-float"
             style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.25);">📊</div>

        <h2 class="text-2xl font-black text-white mb-3">No Dataset Loaded Yet</h2>
        <p class="text-slate-400 max-w-md mx-auto mb-8 leading-relaxed">
          Upload a student dataset or run a single prediction to generate live analytics,
          charts, and AI-driven academic insights.
        </p>

        <!-- Steps -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto mb-10 text-left">
          <div class="p-4 rounded-xl" style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);">
            <div class="text-2xl mb-2">1️⃣</div>
            <div class="text-sm font-semibold text-white mb-1">Run a Prediction</div>
            <div class="text-xs text-slate-500">Enter student metrics and get an instant AI result.</div>
          </div>
          <div class="p-4 rounded-xl" style="background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.2);">
            <div class="text-2xl mb-2">2️⃣</div>
            <div class="text-sm font-semibold text-white mb-1">Upload CSV Batch</div>
            <div class="text-xs text-slate-500">Bulk-predict an entire class from a CSV file.</div>
          </div>
          <div class="p-4 rounded-xl" style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);">
            <div class="text-2xl mb-2">3️⃣</div>
            <div class="text-sm font-semibold text-white mb-1">View Analytics</div>
            <div class="text-xs text-slate-500">Dashboard populates automatically from your data.</div>
          </div>
        </div>

        <div class="flex flex-wrap gap-4 justify-center">
          <button class="btn-primary text-base px-10 py-4" @click="router.push('/predict')">
            ⚡ Get Started
          </button>
          <button class="btn-ghost" @click="router.push('/insights')">
            📈 View Model Insights
          </button>
        </div>
      </div>
    </section>
  </template>

    <!-- ── System Activity Feed ──────────────────────────────────── -->
    <section class="px-6 pb-16 max-w-6xl mx-auto">
      <div class="glass-card p-6 anim-slide-left">
        <div class="flex items-center gap-3 mb-5">
          <div class="w-9 h-9 rounded-lg bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-base">🌐</div>
          <div>
            <h3 class="font-bold text-white">System Activity Feed</h3>
            <p class="text-slate-400 text-xs">Live platform events</p>
          </div>
        </div>
        <div class="flex flex-col gap-3 max-h-[200px] overflow-y-auto pr-2" style="scrollbar-width: thin;">
          <transition-group name="toast">
            <div 
              v-for="log in store.activityLogs" 
              :key="log.id"
              class="flex items-start gap-3 p-3 rounded-lg bg-white/[0.02] border border-white/5"
            >
              <span class="text-lg mt-0.5" v-if="log.type === 'success'">✅</span>
              <span class="text-lg mt-0.5" v-else-if="log.type === 'error'">⚠️</span>
              <span class="text-lg mt-0.5" v-else-if="log.type === 'warning'">🔔</span>
              <span class="text-lg mt-0.5" v-else>ℹ️</span>
              <div class="flex-1">
                <p class="text-sm text-slate-300">{{ log.message }}</p>
                <p class="text-xs text-slate-500 mt-1">
                  {{ log.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) }}
                </p>
              </div>
            </div>
          </transition-group>
          <div v-if="store.activityLogs.length === 0" class="text-slate-500 text-sm text-center py-6 border border-dashed border-white/10 rounded-lg">
            Waiting for new system events...
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA Banner ──────────────────────────────────────────── -->
    <section class="px-6 pb-24 max-w-4xl mx-auto">
      <div class="glass-card p-10 text-center anim-border-glow"
           style="background:linear-gradient(135deg,rgba(79,70,229,0.15),rgba(124,58,237,0.1));border-color:rgba(99,102,241,0.35);">
        <div class="text-4xl mb-4">🎓</div>
        <h2 class="text-3xl font-black text-white mb-3">Ready to Analyse a Student?</h2>
        <p class="text-slate-400 mb-7 max-w-lg mx-auto">Select a Level and Semester, enter the student's course-specific CA scores and academic profile, and receive an instant AI-powered performance prediction with detailed factor explanations.</p>
        <div class="flex flex-wrap gap-4 justify-center">
          <button class="btn-primary text-base px-10 py-4" @click="router.push('/predict')">Get Started →</button>
          <button class="btn-ghost" @click="router.push('/interventions')">View Interventions</button>
        </div>
      </div>
    </section>

  </div>
</template>
