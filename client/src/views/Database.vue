<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../services/api'
import { store } from '../store.js'

const records = ref([])
const totalRecords = ref(0)
const loading = ref(true)
const error = ref('')

const searchQuery = ref('')
const filterStatus = ref('All')

// Reset modal state
const showResetModal = ref(false)
const resetLoading = ref(false)

// Pagination state
const currentPage = ref(1)
const pageSize = ref(15)

// Watch filters and search queries to reset page to 1
watch([searchQuery, filterStatus], () => {
  currentPage.value = 1
})

async function fetchRecords() {
  try {
    const res = await api.get(`/records?t=${new Date().getTime()}`)
    records.value = res.data.records
    totalRecords.value = res.data.total || res.data.records.length
  } catch (err) {
    error.value = 'Failed to load historical records. Is the backend running?'
  } finally {
    loading.value = false
  }
}

async function confirmReset() {
  resetLoading.value = true
  const success = await store.resetSystem()
  if (success) {
    records.value = []
    totalRecords.value = 0
  }
  resetLoading.value = false
  showResetModal.value = false
}

onMounted(fetchRecords)

const filteredRecords = computed(() => {
  return records.value.filter(r => {
    if (filterStatus.value !== 'All' && r.predicted_status !== filterStatus.value) {
      return false
    }
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase()
      const searchStr = `${r.id} ${r.student_id || ''} ${r.gender} ${r.socioeconomic_status} ${r.level || ''} ${r.semester || ''}`.toLowerCase()
      if (!searchStr.includes(q)) return false
    }
    return true
  })
})

const totalPages = computed(() => {
  return Math.ceil(filteredRecords.value.length / pageSize.value) || 1
})

const paginatedRecords = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredRecords.value.slice(start, end)
})

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const statusColor = (status) => {
  if (status === 'Excellent') return '#10B981'
  if (status === 'Average') return '#F59E0B'
  return '#EF4444'
}
</script>

<template>
  <div class="min-h-screen px-6 py-10 max-w-7xl mx-auto">

    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10 anim-fade-up">
      <div>
        <h1 class="text-4xl md:text-5xl font-black text-white mb-3">Student <span class="gradient-text">Database</span></h1>
        <p class="text-slate-400 max-w-xl">View historical prediction records. Filter by outcome to identify students who need immediate academic assistance.</p>
      </div>

      <!-- System Reset Button -->
      <button
        @click="showResetModal = true"
        class="flex items-center gap-2 px-5 py-3 rounded-xl font-semibold text-sm transition-all duration-200 hover:scale-[1.02] shrink-0"
        style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);color:#FCA5A5;"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
        Reset Academic System
      </button>
    </div>

    <!-- Stats Summary Bar -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 anim-fade-up delay-1">
      <div class="glass-card p-4 text-center">
        <div class="text-2xl font-black text-white">{{ totalRecords.toLocaleString() }}</div>
        <div class="text-xs text-slate-400 mt-1">Total Records</div>
      </div>
      <div class="glass-card p-4 text-center">
        <div class="text-2xl font-black text-emerald-400">{{ store.stats.excellent_count }}</div>
        <div class="text-xs text-slate-400 mt-1">Excellent</div>
      </div>
      <div class="glass-card p-4 text-center">
        <div class="text-2xl font-black text-amber-400">{{ store.stats.average_count }}</div>
        <div class="text-xs text-slate-400 mt-1">Average</div>
      </div>
      <div class="glass-card p-4 text-center">
        <div class="text-2xl font-black text-red-400">{{ store.stats.at_risk_count }}</div>
        <div class="text-xs text-slate-400 mt-1">At-Risk</div>
      </div>
    </div>

    <div class="glass-card p-6 anim-fade-up delay-2">
      <div class="flex flex-col md:flex-row gap-4 mb-6 justify-between items-center">
        <div class="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
          <input type="text" v-model="searchQuery" placeholder="Search ID, Level, Gender, SES..." class="form-input md:w-64" />
          <select v-model="filterStatus" class="form-input md:w-48">
            <option value="All">All Predictions</option>
            <option value="Excellent">Excellent</option>
            <option value="Average">Average</option>
            <option value="At-Risk">At-Risk</option>
          </select>
        </div>
        <div class="text-sm text-slate-400">
          Showing <span class="font-bold text-white">{{ filteredRecords.length }}</span> of <span class="font-bold text-white">{{ totalRecords }}</span> total records
        </div>
      </div>

      <div v-if="loading" class="flex flex-col items-center py-12 gap-4">
        <div class="w-12 h-12 border-2 border-indigo-500/30 border-t-indigo-400 rounded-full anim-spin"></div>
      </div>
      
      <div v-else-if="error" class="p-6 text-center text-red-400 bg-red-500/10 rounded-xl border border-red-500/20">
        {{ error }}
      </div>

      <!-- Empty state for 0 records -->
      <div v-else-if="records.length === 0" class="py-16 text-center">
        <div class="text-5xl mb-4">🗄️</div>
        <h3 class="text-xl font-bold text-white mb-2">No Records Found</h3>
        <p class="text-slate-400 text-sm mb-6">The database is empty. Run predictions to populate it.</p>
        <router-link to="/predict" class="btn-primary px-8 py-3">⚡ Run Predictions</router-link>
      </div>

      <div v-else class="overflow-x-auto rounded-xl border border-indigo-500/20">
        <table class="w-full text-left border-collapse min-w-[800px]">
          <thead>
            <tr class="bg-indigo-900/40 text-xs uppercase tracking-wider text-slate-400 border-b border-indigo-500/20">
              <th class="p-4 font-semibold">ID</th>
              <th class="p-4 font-semibold">Age / Gender</th>
              <th class="p-4 font-semibold">SES</th>
              <th class="p-4 font-semibold">Level / Semester</th>
              <th class="p-4 font-semibold">Study Hrs</th>
              <th class="p-4 font-semibold">Prev CGPA / Avg CA</th>
              <th class="p-4 font-semibold text-right">Prediction</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-indigo-500/10">
            <tr v-if="filteredRecords.length === 0">
              <td colspan="7" class="p-8 text-center text-slate-400">No records match your filters.</td>
            </tr>
            <tr v-for="r in paginatedRecords" :key="r.id" class="hover:bg-indigo-500/5 transition-colors">
              <td class="p-4 text-slate-300 font-mono text-sm">#{{ r.student_id || r.id }}</td>
              <td class="p-4 text-slate-300 text-sm">{{ r.age }} y/o {{ r.gender }}</td>
              <td class="p-4 text-slate-300 text-sm">{{ r.socioeconomic_status }}</td>
              <td class="p-4 text-slate-300 text-sm">Lvl {{ r.level || '—' }} / Sem {{ r.semester || '—' }}</td>
              <td class="p-4 text-slate-300 text-sm">{{ r.study_hours_per_week }}h</td>
              <td class="p-4 text-slate-300 text-sm">{{ r.previous_cgpa != null ? r.previous_cgpa.toFixed(2) : '—' }} / {{ r.course_ca_average != null ? r.course_ca_average.toFixed(1) : '—' }}</td>
              <td class="p-4 text-right">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold"
                      :style="{ backgroundColor: statusColor(r.predicted_status) + '22', color: statusColor(r.predicted_status), border: '1px solid ' + statusColor(r.predicted_status) + '44' }">
                  {{ r.predicted_status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Controls -->
      <div v-if="filteredRecords.length > 0" class="flex flex-col sm:flex-row items-center justify-between gap-4 mt-6 pt-6 border-t border-indigo-500/10">
        <div class="flex items-center gap-2 text-sm text-slate-400">
          <span>Rows per page:</span>
          <select v-model="pageSize" class="bg-indigo-950 border border-indigo-500/30 text-white rounded-lg px-2 py-1 text-xs outline-none">
            <option :value="15">15</option>
            <option :value="30">30</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
        </div>
        <div class="flex items-center gap-4">
          <button 
            @click="prevPage" 
            :disabled="currentPage === 1" 
            class="px-3 py-1.5 rounded-lg text-xs font-semibold border border-white/10 text-slate-400 hover:text-white hover:border-white/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          >
            ← Previous
          </button>
          <span class="text-xs text-slate-400 font-medium">
            Page <span class="text-white font-bold">{{ currentPage }}</span> of <span class="text-white font-bold">{{ totalPages }}</span>
          </span>
          <button 
            @click="nextPage" 
            :disabled="currentPage === totalPages" 
            class="px-3 py-1.5 rounded-lg text-xs font-semibold border border-white/10 text-slate-400 hover:text-white hover:border-white/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Next →
          </button>
        </div>
      </div>
    </div>

    <!-- ── System Reset Confirmation Modal ──────────────────────────── -->
    <Teleport to="body">
    <transition name="modal">
      <div v-if="showResetModal"
           class="fixed inset-0 z-50 flex items-center justify-center p-4"
           style="background:rgba(0,0,0,0.8);backdrop-filter:blur(10px);"
           @click.self="showResetModal = false">
        <div class="glass-card p-10 max-w-lg w-full anim-scale-in"
             style="border-color:rgba(239,68,68,0.45);background:rgba(10,15,40,0.99);">

          <!-- Icon -->
          <div class="w-20 h-20 rounded-2xl flex items-center justify-center text-4xl mx-auto mb-6"
               style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.35);">⚠️</div>

          <h2 class="text-3xl font-black text-white text-center mb-2">Reset Academic System</h2>
          <p class="text-slate-400 text-sm text-center leading-relaxed mb-6">
            This is a <strong class="text-red-400">destructive action</strong>. Please read carefully before proceeding.
          </p>

          <!-- Warning list -->
          <div class="p-4 rounded-xl mb-6" style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.2);">
            <div class="text-xs font-bold text-red-300 uppercase tracking-wider mb-3">What will be deleted:</div>
            <ul class="text-sm text-slate-400 space-y-2">
              <li class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0"></span>
                All {{ totalRecords.toLocaleString() }} prediction records from the database
              </li>
              <li class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0"></span>
                All dashboard analytics, charts, and live statistics
              </li>
              <li class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0"></span>
                All intervention progress and activity logs
              </li>
            </ul>
          </div>

          <p class="text-xs text-slate-500 text-center mb-8">
            The trained ML models and insights will be preserved. Only prediction records are removed.
          </p>

          <div class="flex gap-3">
            <button
              class="flex-1 btn-ghost"
              @click="showResetModal = false"
              :disabled="resetLoading">
              Cancel
            </button>
            <button
              class="flex-1 py-3.5 rounded-xl font-bold text-white flex items-center justify-center gap-2 transition-all"
              style="background:linear-gradient(135deg,#dc2626,#991b1b);border:1px solid rgba(239,68,68,0.5);"
              @click="confirmReset"
              :disabled="resetLoading">
              <span v-if="resetLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full anim-spin"></span>
              <span>{{ resetLoading ? 'Resetting...' : '🗑️ Reset Everything' }}</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
    </Teleport>
  </div>
</template>
