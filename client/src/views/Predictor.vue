<script setup>
import { reactive, ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import RiskBadge from '../components/RiskBadge.vue'
import { store } from '../store.js'
import { predictionService } from '../services/predictionService'
import { useStatusColors } from '../composables/useStatusColors'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement, PointElement, LinearScale, CategoryScale,
  Filler, Tooltip as ChartTooltip,
} from 'chart.js'
import {
  getCourseSet, is100Alpha, isSIWES,
} from '../constants/courseStructure.js'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Filler, ChartTooltip)

const router = useRouter()

// ── Tabs ──────────────────────────────────────────────────────────────────────
const activeTab = ref('single')

// ── Student Info Form ─────────────────────────────────────────────────────────
const form = reactive({
  Student_ID:           '',
  Gender:               'Male',
  Age:                  20,
  Socioeconomic_Status: 'Medium',
  Level:                200,
  Semester:             'First',
  Study_Hours_Per_Week: 10,
  Previous_CGPA:        2.5,
  Entry_Academic_Score: 70,
})

// ── Dynamic Course State ───────────────────────────────────────────────────────
// courseScores: { [code]: { ca: null|number, prev: null|number } }
const courseScores     = reactive({})
const electiveOptions  = ref([])    // available elective courses for this semester
const selectedElectives = ref([])   // codes of electives the user has added
const addElectiveCode  = ref('')    // currently highlighted in the "add elective" dropdown

// ── Computed: is this the 100 Alpha special case? ─────────────────────────────
const show100AlphaEntry = computed(() => is100Alpha(form.Level, form.Semester))
const showSIWESWarning  = computed(() => isSIWES(form.Level, form.Semester))

// ── Loaded courses for current Level+Semester ─────────────────────────────────
const courseSet = computed(() => getCourseSet(form.Level, form.Semester))

const coreCourses       = computed(() => courseSet.value?.core       ?? [])
const universityCourses = computed(() => courseSet.value?.university ?? [])
const nucCourses        = computed(() => courseSet.value?.nuc        ?? [])

// All elective courses the user has selected
const selectedElectiveCourses = computed(() =>
  (courseSet.value?.electiveOptions ?? []).filter(c => selectedElectives.value.includes(c.code))
)

// Remaining elective options not yet added
const remainingElectiveOptions = computed(() =>
  (courseSet.value?.electiveOptions ?? []).filter(c => !selectedElectives.value.includes(c.code))
)

// ── Load Courses when Level or Semester changes ───────────────────────────────
function loadCourses() {
  // Clear current state
  Object.keys(courseScores).forEach(k => delete courseScores[k])
  selectedElectives.value = []
  addElectiveCode.value   = ''

  const set = getCourseSet(form.Level, form.Semester)
  if (!set) return

  // Initialize score objects for all course types
  const allCodes = [
    ...(set.core             ?? []),
    ...(set.electiveOptions  ?? []),
    ...(set.university       ?? []),
    ...(set.nuc              ?? []),
  ]
  allCodes.forEach(c => {
    courseScores[c.code] = { ca: null, prev: null }
  })

  // Pre-select electives if only one option exists (auto-select)
  if ((set.electiveOptions ?? []).length === 1) {
    selectedElectives.value = [set.electiveOptions[0].code]
  }

  electiveOptions.value = set.electiveOptions ?? []
}

watch(
  () => [form.Level, form.Semester],
  () => loadCourses(),
  { immediate: true }
)

// ── Elective management ───────────────────────────────────────────────────────
function addElective() {
  const code = addElectiveCode.value
  if (code && !selectedElectives.value.includes(code)) {
    selectedElectives.value.push(code)
  }
  addElectiveCode.value = ''
}

function removeElective(code) {
  selectedElectives.value = selectedElectives.value.filter(c => c !== code)
}

// ── Live Summary Calculations ─────────────────────────────────────────────────
function activeCourses() {
  return [
    ...coreCourses.value,
    ...selectedElectiveCourses.value,
    ...universityCourses.value,
    ...nucCourses.value,
  ]
}

const liveCAScores = computed(() =>
  activeCourses()
    .map(c => courseScores[c.code]?.ca)
    .filter(v => v !== null && v !== undefined && v !== '')
    .map(Number)
)

const livePrevScores = computed(() => {
  if (show100AlphaEntry.value) return []
  return activeCourses()
    .map(c => courseScores[c.code]?.prev)
    .filter(v => v !== null && v !== undefined && v !== '')
    .map(Number)
})

const liveCAAvg = computed(() => {
  const arr = liveCAScores.value
  return arr.length ? (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(1) : '—'
})

const livePrevAvg = computed(() => {
  if (show100AlphaEntry.value) {
    const s = Number(form.Entry_Academic_Score)
    return isNaN(s) ? '—' : s.toFixed(1)
  }
  const arr = livePrevScores.value
  return arr.length ? (arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(1) : '—'
})

const liveTotalUnits = computed(() => activeCourses().reduce((s, c) => s + (c.units || 0), 0))

const liveWeakCA = computed(() =>
  liveCAScores.value.filter(s => s < 15).length
)

// ── Validation ────────────────────────────────────────────────────────────────
const fieldErrors = reactive({})

function clearErrors() {
  Object.keys(fieldErrors).forEach(k => delete fieldErrors[k])
}

function validateForm() {
  clearErrors()
  let valid = true

  if (!['Male', 'Female'].includes(form.Gender)) {
    fieldErrors.Gender = 'Gender must be Male or Female'
    valid = false
  }
  if (form.Age < 15 || form.Age > 60) {
    fieldErrors.Age = 'Age must be between 15 and 60'
    valid = false
  }
  if (!['Low', 'Medium', 'High'].includes(form.Socioeconomic_Status)) {
    fieldErrors.Socioeconomic_Status = 'Must be Low, Medium, or High'
    valid = false
  }
  if (![100, 200, 300, 400].includes(Number(form.Level))) {
    fieldErrors.Level = 'Level must be 100, 200, 300, or 400'
    valid = false
  }
  if (!['First', 'Second'].includes(form.Semester)) {
    fieldErrors.Semester = 'Semester must be First or Second'
    valid = false
  }
  if (showSIWESWarning.value) {
    fieldErrors.Semester = '300 Level Second Semester is SIWES — not available in the prediction model'
    return false
  }
  if (form.Study_Hours_Per_Week < 0 || form.Study_Hours_Per_Week > 80) {
    fieldErrors.Study_Hours_Per_Week = 'Study hours must be between 0 and 80'
    valid = false
  }
  if (form.Previous_CGPA < 0 || form.Previous_CGPA > 5) {
    fieldErrors.Previous_CGPA = 'CGPA must be between 0.00 and 5.00'
    valid = false
  }

  // 100 Alpha: validate Entry_Academic_Score
  if (show100AlphaEntry.value) {
    const eas = Number(form.Entry_Academic_Score)
    if (isNaN(eas) || eas < 0 || eas > 100) {
      fieldErrors.Entry_Academic_Score = 'Entry Academic Score must be between 0 and 100'
      valid = false
    }
  }

  // Validate per-course scores
  const courses = activeCourses()
  courses.forEach(c => {
    const s = courseScores[c.code]
    if (!s) return

    // CA score validation
    const ca = Number(s.ca)
    if (s.ca === null || s.ca === '' || s.ca === undefined) {
      fieldErrors[`ca_${c.code}`] = 'Required'
      valid = false
    } else if (isNaN(ca) || ca < 0 || ca > 30) {
      fieldErrors[`ca_${c.code}`] = '0–30'
      valid = false
    }

    // Prev score validation (not for 100 Alpha)
    if (!show100AlphaEntry.value) {
      const prev = Number(s.prev)
      if (s.prev === null || s.prev === '' || s.prev === undefined) {
        fieldErrors[`prev_${c.code}`] = 'Required'
        valid = false
      } else if (isNaN(prev) || prev < 0 || prev > 100) {
        fieldErrors[`prev_${c.code}`] = '0–100'
        valid = false
      }
    }
  })

  if (coreCourses.value.length === 0) {
    fieldErrors.courses = 'No courses loaded — please select a valid Level and Semester'
    valid = false
  }

  return valid
}

// ── Prediction ────────────────────────────────────────────────────────────────
const result   = ref(null)
const loading  = ref(false)
const errorMsg = ref('')

async function predict() {
  if (!validateForm()) return
  loading.value  = true
  errorMsg.value = ''
  result.value   = null

  try {
    const courses = activeCourses()

    // Build typed score arrays in dataset column order
    const core_ca_scores       = coreCourses.value.map(c => Number(courseScores[c.code]?.ca))
    const elective_ca_scores   = selectedElectiveCourses.value.map(c => Number(courseScores[c.code]?.ca))
    const university_ca_scores = universityCourses.value.map(c => Number(courseScores[c.code]?.ca))
    const nuc_ca_scores        = nucCourses.value.map(c => Number(courseScores[c.code]?.ca))
    const previous_scores      = show100AlphaEntry.value
      ? []
      : courses.map(c => Number(courseScores[c.code]?.prev))

    const payload = {
      Student_ID:           form.Student_ID || null,
      Gender:               form.Gender,
      Age:                  form.Age,
      Socioeconomic_Status: form.Socioeconomic_Status,
      Level:                Number(form.Level),
      Semester:             form.Semester,
      Study_Hours_Per_Week: form.Study_Hours_Per_Week,
      Previous_CGPA:        form.Previous_CGPA,
      ...(show100AlphaEntry.value ? { Entry_Academic_Score: Number(form.Entry_Academic_Score) } : {}),
      previous_scores,
      core_ca_scores,
      elective_ca_scores,
      university_ca_scores,
      nuc_ca_scores,
    }

    result.value = await predictionService.predictSingle(payload)
    store.fetchStats()
    store.addNotification(`Prediction completed — ${result.value.prediction}`, 'success')
  } catch (err) {
    errorMsg.value = err.message || 'An error occurred during prediction.'
  } finally {
    loading.value = false
  }
}

// ── Result Presentation ───────────────────────────────────────────────────────
const { predictionColor, predictionIcon, riskLevel } = useStatusColors(
  computed(() => result.value?.prediction)
)

const confidenceScore = computed(() => {
  if (!result.value?.probabilities) return 0
  return result.value.probabilities[result.value.prediction] ?? 0
})

const gpaScore = computed(() => {
  const p = result.value?.prediction
  if (p === 'Excellent') return Math.round(65 + (confidenceScore.value / 100) * 35)
  if (p === 'Average')   return Math.round(45 + (confidenceScore.value / 100) * 20)
  return Math.round(20 + (confidenceScore.value / 100) * 25)
})

const ringOffset = computed(() => {
  const pct = gpaScore.value / 100
  return Math.round(283 - 283 * pct)
})

const aiNarrative = computed(() => {
  if (!result.value) return ''
  const derived = result.value.derived || {}
  const ca  = derived.Course_CA_Average || 0
  const hrs = form.Study_Hours_Per_Week
  const cgpa = form.Previous_CGPA
  const weakCa = derived.Weak_CA_Count || 0
  const parts = []
  if (cgpa >= 3.5)     parts.push('strong prior GPA')
  else if (cgpa < 2.0) parts.push('low previous CGPA')
  if (hrs >= 20)       parts.push('high study commitment')
  else if (hrs < 8)    parts.push('insufficient study hours')
  if (ca >= 22)        parts.push('excellent CA performance')
  else if (ca < 14)    parts.push('weak CA scores')
  if (weakCa >= 3)     parts.push(`${weakCa} weak CA courses`)
  const factors = parts.length ? parts.join(', ') : 'mixed academic indicators'
  return `This student is predicted to perform at the ${result.value.prediction} level due to ${factors}. ${
    riskLevel.value === 'high'
      ? 'Immediate academic intervention is recommended.'
      : riskLevel.value === 'medium'
      ? 'Monitoring and targeted support may be beneficial.'
      : 'Continue current study habits for sustained success.'
  }`
})

// ── Sparkline ─────────────────────────────────────────────────────────────────
const sparklineData = computed(() => {
  if (!result.value) return null
  const p = result.value.prediction
  const base = p === 'Excellent' ? [58, 62, 67, 70, 74, gpaScore.value]
             : p === 'Average'   ? [48, 52, 50, 55, 57, gpaScore.value]
             :                     [55, 50, 45, 42, 38, gpaScore.value]
  const color = predictionColor.value.text
  return {
    labels: ['Wk 1', 'Wk 2', 'Wk 3', 'Wk 4', 'Wk 5', 'Now'],
    datasets: [{
      data: base,
      borderColor: color,
      backgroundColor: color + '18',
      fill: true, tension: 0.45,
      pointRadius: [2,2,2,2,2,5],
      pointBackgroundColor: color,
      borderWidth: 2,
    }],
  }
})

const sparklineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y}%` } } },
  scales: {
    x: { grid: { display: false }, ticks: { color: '#475569', font: { size: 9 } } },
    y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#475569', font: { size: 9 }, callback: v => v + '%' }, min: 20, max: 100 },
  },
}

const impactColor = (impact) => impact === 'positive' ? '#10B981' : impact === 'negative' ? '#EF4444' : '#F59E0B'
const impactIcon  = (impact) => impact === 'positive' ? '↑' : impact === 'negative' ? '↓' : '~'

// ── Batch Upload ───────────────────────────────────────────────────────────────
const fileInput      = ref(null)
const selectedFile   = ref(null)
const batchLoading   = ref(false)
const batchError     = ref('')
const batchSuccess   = ref(false)
const isDragging     = ref(false)
const filePreview    = ref(null)
const replaceDataset = ref(false)
const showReplaceModal = ref(false)

const BATCH_REQUIRED = [
  'Gender', 'Age', 'Socioeconomic_Status', 'Level', 'Semester',
  'Study_Hours_Per_Week', 'Previous_CGPA',
  'Previous_Course_Average', 'Lowest_Previous_Score', 'Weak_Previous_Count',
  'Course_CA_Average', 'Lowest_CA_Score', 'Weak_CA_Count',
  'Core_CA_Average', 'Elective_CA_Average', 'University_CA_Average', 'Total_Units',
]

function parseCSVForPreview(file) {
  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target.result
    const lines = text.split('\n').filter(l => l.trim())
    if (lines.length > 0) {
      const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''))
      const rows = lines.slice(1, 4).map(l => l.split(',').map(c => c.trim().replace(/^"|"$/g, '')))
      filePreview.value = { rowCount: lines.length - 1, headers, previewRows: rows }
      const missing = BATCH_REQUIRED.filter(r => !headers.includes(r))
      if (missing.length > 0) {
        batchError.value = `Missing required columns: ${missing.join(', ')}`
      }
    }
  }
  reader.readAsText(file)
}

function handleFileChange(e) {
  const file = e.target.files[0]
  if (file && (file.name.endsWith('.csv') || file.name.endsWith('.xlsx'))) {
    selectedFile.value = file
    batchError.value   = ''
    batchSuccess.value = false
    if (file.name.endsWith('.csv')) parseCSVForPreview(file)
    else filePreview.value = { rowCount: '?', headers: [], previewRows: [] }
  } else {
    batchError.value   = 'Please select a valid .csv or .xlsx file'
    selectedFile.value = null
    filePreview.value  = null
  }
}

function handleFileDrop(e) {
  isDragging.value = false
  const files = e.dataTransfer.files
  if (files.length) handleFileChange({ target: { files } })
}

function handlePaste(e) {
  if (activeTab.value !== 'batch') return
  const items = e.clipboardData?.items
  if (!items) return
  for (let i = 0; i < items.length; i++) {
    if (items[i].kind === 'file') {
      const file = items[i].getAsFile()
      if (file && file.name.endsWith('.csv')) {
        selectedFile.value = file
        batchError.value   = ''
        batchSuccess.value = false
        parseCSVForPreview(file)
        return
      }
    }
    if (items[i].kind === 'string' && items[i].type === 'text/plain') {
      items[i].getAsString((text) => {
        if (text.includes(',') && text.split('\n').length > 1) {
          const blob = new Blob([text], { type: 'text/csv' })
          const file = new File([blob], 'pasted_data.csv', { type: 'text/csv' })
          selectedFile.value = file
          batchError.value   = ''
          batchSuccess.value = false
          parseCSVForPreview(file)
        }
      })
      return
    }
  }
}

onMounted(() => window.addEventListener('paste', handlePaste))
onUnmounted(() => window.removeEventListener('paste', handlePaste))

async function uploadBatch() {
  if (!selectedFile.value) return
  if (replaceDataset.value) { showReplaceModal.value = true; return }
  await runBatchUpload(false)
}

async function runBatchUpload(replace) {
  showReplaceModal.value = false
  batchLoading.value = true
  batchError.value   = ''
  batchSuccess.value = false
  try {
    const blob = await predictionService.predictBatch(selectedFile.value, replace)
    const url  = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href  = url
    link.setAttribute('download', `predictions_${selectedFile.value.name}`)
    document.body.appendChild(link)
    link.click()
    link.parentNode.removeChild(link)
    batchSuccess.value = true
    store.fetchStats()
    store.addNotification(
      replace
        ? `Dataset replaced! ${filePreview.value?.rowCount || 'Multiple'} student records loaded.`
        : `Batch prediction completed for ${filePreview.value?.rowCount || 'multiple'} students`,
      'success'
    )
  } catch (err) {
    batchError.value = err.message || 'An error occurred during batch prediction.'
  } finally {
    batchLoading.value = false
  }
}

const classOrder = ['Excellent', 'Average', 'At-Risk']
const probColor  = (cls) => cls === 'Excellent' ? '#10B981' : cls === 'Average' ? '#F59E0B' : '#EF4444'
</script>

<template>
  <div class="min-h-screen px-6 py-10 max-w-7xl mx-auto">

    <!-- Header -->
    <div class="text-center mb-6 anim-fade-up">
      <h1 class="text-4xl md:text-5xl font-black text-white mb-3">
        Performance <span class="gradient-text">Predictor</span>
      </h1>
      <p class="text-slate-400 max-w-lg mx-auto">
        Select a CS level and semester to load the correct courses, enter CA and previous scores, then get an instant AI prediction.
      </p>
    </div>

    <!-- Tabs -->
    <div class="flex justify-center mb-8 anim-fade-up">
      <div class="glass-card p-1 flex gap-2 rounded-xl inline-flex">
        <button
          class="px-6 py-2 rounded-lg text-sm font-semibold transition-all"
          :class="activeTab === 'single' ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          @click="activeTab = 'single'">
          👤 Single Student
        </button>
        <button
          class="px-6 py-2 rounded-lg text-sm font-semibold transition-all"
          :class="activeTab === 'batch' ? 'bg-indigo-600 text-white shadow-lg' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          @click="activeTab = 'batch'">
          📁 Batch Upload
        </button>
      </div>
    </div>

    <!-- ── Single Student Tab ──────────────────────────────────────────────── -->
    <div v-if="activeTab === 'single'" class="flex flex-col xl:flex-row gap-6">

      <!-- ── Form Panel ───────────────────────────────────────────────────── -->
      <div class="glass-card p-7 flex-1 min-w-0 anim-fade-up delay-1">

        <!-- Section: Student Info -->
        <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2">
          <span class="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-sm">👤</span>
          Student Information
        </h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-7">
          <!-- Student ID -->
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Student ID <span class="text-slate-600 normal-case">(optional)</span>
            </label>
            <input type="text" v-model="form.Student_ID" placeholder="e.g. CS/2021/001"
              class="form-input" maxlength="30" />
          </div>

          <!-- Gender -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Gender</label>
            <select v-model="form.Gender" class="form-input" :class="fieldErrors.Gender ? 'border-red-500/60' : ''">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
            <p v-if="fieldErrors.Gender" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Gender }}</p>
          </div>

          <!-- Age -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Age — <span class="text-indigo-400">{{ form.Age }}</span>
            </label>
            <input type="range" min="15" max="40" v-model.number="form.Age" class="w-full" />
            <p v-if="fieldErrors.Age" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Age }}</p>
          </div>

          <!-- Socioeconomic Status -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Socioeconomic Status</label>
            <select v-model="form.Socioeconomic_Status" class="form-input" :class="fieldErrors.Socioeconomic_Status ? 'border-red-500/60' : ''">
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
            <p v-if="fieldErrors.Socioeconomic_Status" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Socioeconomic_Status }}</p>
          </div>

          <!-- Level -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Level</label>
            <select v-model.number="form.Level" class="form-input" :class="fieldErrors.Level ? 'border-red-500/60' : ''">
              <option :value="100">100 Level</option>
              <option :value="200">200 Level</option>
              <option :value="300">300 Level</option>
              <option :value="400">400 Level</option>
            </select>
            <p v-if="fieldErrors.Level" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Level }}</p>
          </div>

          <!-- Semester -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Semester</label>
            <select v-model="form.Semester" class="form-input" :class="fieldErrors.Semester ? 'border-red-500/60' : ''">
              <option value="First">First Semester (Alpha)</option>
              <option value="Second">Second Semester (Omega)</option>
            </select>
            <p v-if="fieldErrors.Semester" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Semester }}</p>
          </div>

          <!-- Study Hours -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Study Hours/Week — <span class="text-indigo-400">{{ form.Study_Hours_Per_Week.toFixed(1) }} hrs</span>
            </label>
            <input type="range" min="0" max="60" step="0.5" v-model.number="form.Study_Hours_Per_Week" class="w-full" />
            <p v-if="fieldErrors.Study_Hours_Per_Week" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Study_Hours_Per_Week }}</p>
          </div>

          <!-- Previous CGPA -->
          <div>
            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
              Previous CGPA — <span class="text-indigo-400">{{ form.Previous_CGPA.toFixed(2) }} / 5.00</span>
            </label>
            <input type="range" min="0" max="5" step="0.01" v-model.number="form.Previous_CGPA" class="w-full" />
            <p v-if="fieldErrors.Previous_CGPA" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Previous_CGPA }}</p>
          </div>

          <!-- Entry Academic Score (100 Alpha only) -->
          <div v-if="show100AlphaEntry" class="sm:col-span-2">
            <label class="block text-xs font-semibold text-amber-400 uppercase tracking-wider mb-2">
              🎓 Entry Academic Score / 100
              <span class="text-slate-500 normal-case font-normal ml-1">(100 Level – no previous university scores yet)</span>
            </label>
            <input type="number" min="0" max="100" step="0.1"
              v-model.number="form.Entry_Academic_Score"
              placeholder="Enter WAEC/NECO admission score (0–100)"
              class="form-input"
              :class="fieldErrors.Entry_Academic_Score ? 'border-red-500/60' : 'border-amber-500/30'" />
            <p v-if="fieldErrors.Entry_Academic_Score" class="text-red-400 text-xs mt-1">⚠ {{ fieldErrors.Entry_Academic_Score }}</p>
          </div>
        </div>

        <!-- ── SIWES Warning ──────────────────────────────────────────────── -->
        <div v-if="showSIWESWarning" class="mb-6 p-5 rounded-2xl flex items-start gap-4"
             style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.35);">
          <span class="text-2xl shrink-0">🏭</span>
          <div>
            <p class="text-amber-300 font-bold mb-1">300 Level Second Semester — SIWES</p>
            <p class="text-slate-400 text-sm leading-relaxed">
              This semester corresponds to the Students' Industrial Work Experience Scheme (SIWES).
              It is not part of the academic prediction model. Please select a different level or semester.
            </p>
          </div>
        </div>

        <!-- ── Live Summary Bar ───────────────────────────────────────────── -->
        <div v-if="!showSIWESWarning"
             class="grid grid-cols-4 gap-3 mb-6 p-4 rounded-xl"
             style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.15);">
          <div class="text-center">
            <div class="text-xs text-slate-500 uppercase tracking-wider mb-1">CA Avg</div>
            <div class="text-lg font-black text-indigo-300">{{ liveCAAvg }}<span class="text-xs text-slate-500">/30</span></div>
          </div>
          <div class="text-center border-x border-white/8">
            <div class="text-xs text-slate-500 uppercase tracking-wider mb-1">Prev Avg</div>
            <div class="text-lg font-black text-indigo-300">{{ livePrevAvg }}<span class="text-xs text-slate-500">/100</span></div>
          </div>
          <div class="text-center border-r border-white/8">
            <div class="text-xs text-slate-500 uppercase tracking-wider mb-1">Total Units</div>
            <div class="text-lg font-black text-indigo-300">{{ liveTotalUnits }}</div>
          </div>
          <div class="text-center">
            <div class="text-xs text-slate-500 uppercase tracking-wider mb-1">Weak CA</div>
            <div class="text-lg font-black" :class="liveWeakCA > 2 ? 'text-red-400' : 'text-emerald-400'">{{ liveWeakCA }}</div>
          </div>
        </div>

        <!-- ── Course Tables ───────────────────────────────────────────────── -->
        <div v-if="!showSIWESWarning" class="space-y-5">

          <!-- Column header legend -->
          <div class="hidden sm:grid grid-cols-[auto_1fr_auto_auto_auto] gap-3 px-3 pb-1 border-b border-white/6">
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider w-20">Code</div>
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider">Course Title</div>
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider w-12 text-center">Units</div>
            <div v-if="!show100AlphaEntry" class="text-xs font-bold text-slate-500 uppercase tracking-wider w-24 text-center">Prev /100</div>
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider w-20 text-center">CA /30</div>
          </div>

          <!-- ── Core Courses ──────────────────────────────────────────────── -->
          <div class="rounded-xl overflow-hidden" style="border:1px solid rgba(16,185,129,0.2);">
            <div class="px-4 py-2.5 flex items-center gap-2" style="background:rgba(16,185,129,0.08);">
              <span class="w-5 h-5 rounded bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-xs">📚</span>
              <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Core Courses</span>
              <span class="ml-auto text-xs text-slate-600">Auto-loaded · Cannot be removed</span>
            </div>
            <div v-for="(course, idx) in coreCourses" :key="course.code"
                 class="grid grid-cols-[auto_1fr] sm:grid-cols-[auto_1fr_auto_auto_auto] gap-3 items-center px-4 py-3 transition-colors"
                 :class="idx % 2 === 0 ? 'bg-white/[0.015]' : ''">
              <!-- Code -->
              <div class="w-20">
                <span class="text-xs font-mono font-bold text-emerald-300 bg-emerald-500/10 px-2 py-0.5 rounded">
                  {{ course.code }}
                </span>
              </div>
              <!-- Title -->
              <div class="text-sm text-slate-300 leading-tight min-w-0">{{ course.title }}</div>
              <!-- Units -->
              <div class="hidden sm:flex w-12 justify-center">
                <span class="text-xs text-slate-500 bg-white/5 px-2 py-0.5 rounded">{{ course.units }}u</span>
              </div>
              <!-- Prev Score -->
              <div v-if="!show100AlphaEntry" class="hidden sm:flex w-24 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="100" step="0.1"
                    v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`prev_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–100" />
                  <span v-if="fieldErrors[`prev_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`prev_${course.code}`] }}
                  </span>
                </div>
              </div>
              <!-- CA Score -->
              <div class="hidden sm:flex w-20 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="30" step="0.1"
                    v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`ca_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–30" />
                  <span v-if="fieldErrors[`ca_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`ca_${course.code}`] }}
                  </span>
                </div>
              </div>

              <!-- Mobile row: inputs below title -->
              <div class="sm:hidden col-span-2 flex gap-3 mt-1">
                <div v-if="!show100AlphaEntry" class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">Prev /100</label>
                  <input type="number" min="0" max="100" step="0.1"
                    v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5"
                    :class="fieldErrors[`prev_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–100" />
                  <p v-if="fieldErrors[`prev_${course.code}`]" class="text-red-400 text-[10px] mt-0.5">{{ fieldErrors[`prev_${course.code}`] }}</p>
                </div>
                <div class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">CA /30</label>
                  <input type="number" min="0" max="30" step="0.1"
                    v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5"
                    :class="fieldErrors[`ca_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–30" />
                  <p v-if="fieldErrors[`ca_${course.code}`]" class="text-red-400 text-[10px] mt-0.5">{{ fieldErrors[`ca_${course.code}`] }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- ── Elective Courses ──────────────────────────────────────────── -->
          <div v-if="electiveOptions.length > 0" class="rounded-xl overflow-hidden" style="border:1px solid rgba(99,102,241,0.2);">
            <div class="px-4 py-2.5 flex items-center gap-2 flex-wrap" style="background:rgba(99,102,241,0.08);">
              <span class="w-5 h-5 rounded bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-xs">✏️</span>
              <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">Elective Courses</span>
              <span class="ml-auto text-xs text-slate-600">Select from available options</span>
            </div>

            <!-- Add Elective control -->
            <div class="px-4 py-3 flex gap-2 items-center border-b border-white/6" style="background:rgba(99,102,241,0.04);">
              <select v-model="addElectiveCode" class="form-input flex-1 text-sm py-2"
                      :disabled="remainingElectiveOptions.length === 0">
                <option value="">
                  {{ remainingElectiveOptions.length === 0 ? '— All electives added —' : '— Select an elective to add —' }}
                </option>
                <option v-for="opt in remainingElectiveOptions" :key="opt.code" :value="opt.code">
                  {{ opt.code }} — {{ opt.title }}
                </option>
              </select>
              <button @click="addElective"
                      :disabled="!addElectiveCode"
                      class="px-4 py-2 rounded-lg text-sm font-semibold transition-all shrink-0"
                      style="background:rgba(99,102,241,0.2);color:#a5b4fc;border:1px solid rgba(99,102,241,0.3);"
                      :class="!addElectiveCode ? 'opacity-40 cursor-not-allowed' : 'hover:bg-indigo-500/30'">
                + Add
              </button>
            </div>

            <!-- No electives yet -->
            <div v-if="selectedElectiveCourses.length === 0" class="px-4 py-6 text-center text-sm text-slate-600 italic">
              No elective courses added yet. Use the dropdown above to add one.
            </div>

            <!-- Selected elective rows -->
            <div v-for="(course, idx) in selectedElectiveCourses" :key="course.code"
                 class="grid grid-cols-[auto_1fr] sm:grid-cols-[auto_1fr_auto_auto_auto_auto] gap-3 items-center px-4 py-3 transition-colors"
                 :class="idx % 2 === 0 ? 'bg-white/[0.015]' : ''">
              <div class="w-20">
                <span class="text-xs font-mono font-bold text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded">
                  {{ course.code }}
                </span>
              </div>
              <div class="text-sm text-slate-300 leading-tight min-w-0">{{ course.title }}</div>
              <div class="hidden sm:flex w-12 justify-center">
                <span class="text-xs text-slate-500 bg-white/5 px-2 py-0.5 rounded">{{ course.units }}u</span>
              </div>
              <div v-if="!show100AlphaEntry" class="hidden sm:flex w-24 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="100" step="0.1"
                    v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`prev_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–100" />
                  <span v-if="fieldErrors[`prev_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`prev_${course.code}`] }}
                  </span>
                </div>
              </div>
              <div class="hidden sm:flex w-20 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="30" step="0.1"
                    v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`ca_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–30" />
                  <span v-if="fieldErrors[`ca_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`ca_${course.code}`] }}
                  </span>
                </div>
              </div>
              <!-- Remove button -->
              <div class="hidden sm:flex w-7 justify-center">
                <button @click="removeElective(course.code)"
                  class="w-6 h-6 rounded flex items-center justify-center text-slate-600 hover:text-red-400 hover:bg-red-500/10 transition-all text-xs">✕</button>
              </div>

              <!-- Mobile -->
              <div class="sm:hidden col-span-2 flex gap-3 mt-1">
                <div v-if="!show100AlphaEntry" class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">Prev /100</label>
                  <input type="number" min="0" max="100" step="0.1"
                    v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5"
                    :class="fieldErrors[`prev_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–100" />
                </div>
                <div class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">CA /30</label>
                  <input type="number" min="0" max="30" step="0.1"
                    v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5"
                    :class="fieldErrors[`ca_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–30" />
                </div>
                <div class="flex items-end pb-1">
                  <button @click="removeElective(course.code)"
                    class="w-7 h-7 rounded flex items-center justify-center text-slate-600 hover:text-red-400 hover:bg-red-500/10 transition-all text-xs">✕</button>
                </div>
              </div>
            </div>
          </div>

          <!-- ── University Courses ─────────────────────────────────────────── -->
          <div v-if="universityCourses.length > 0" class="rounded-xl overflow-hidden" style="border:1px solid rgba(245,158,11,0.2);">
            <div class="px-4 py-2.5 flex items-center gap-2" style="background:rgba(245,158,11,0.06);">
              <span class="w-5 h-5 rounded bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-xs">🏛️</span>
              <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">University Courses</span>
              <span class="ml-auto text-xs text-slate-600">Auto-loaded · Cannot be removed</span>
            </div>
            <div v-for="(course, idx) in universityCourses" :key="course.code"
                 class="grid grid-cols-[auto_1fr] sm:grid-cols-[auto_1fr_auto_auto_auto] gap-3 items-center px-4 py-3 transition-colors"
                 :class="idx % 2 === 0 ? 'bg-white/[0.015]' : ''">
              <div class="w-20">
                <span class="text-xs font-mono font-bold text-amber-300 bg-amber-500/10 px-2 py-0.5 rounded">
                  {{ course.code }}
                </span>
              </div>
              <div class="text-sm text-slate-300 leading-tight min-w-0">{{ course.title }}</div>
              <div class="hidden sm:flex w-12 justify-center">
                <span class="text-xs text-slate-500 bg-white/5 px-2 py-0.5 rounded">{{ course.units }}u</span>
              </div>
              <div v-if="!show100AlphaEntry" class="hidden sm:flex w-24 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="100" step="0.1"
                    v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`prev_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–100" />
                  <span v-if="fieldErrors[`prev_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`prev_${course.code}`] }}
                  </span>
                </div>
              </div>
              <div class="hidden sm:flex w-20 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="30" step="0.1"
                    v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`ca_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–30" />
                  <span v-if="fieldErrors[`ca_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`ca_${course.code}`] }}
                  </span>
                </div>
              </div>
              <!-- Mobile -->
              <div class="sm:hidden col-span-2 flex gap-3 mt-1">
                <div v-if="!show100AlphaEntry" class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">Prev /100</label>
                  <input type="number" min="0" max="100" step="0.1" v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5" placeholder="0–100" />
                </div>
                <div class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">CA /30</label>
                  <input type="number" min="0" max="30" step="0.1" v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5" placeholder="0–30" />
                </div>
              </div>
            </div>
          </div>

          <!-- ── NUC / Vocational Courses ──────────────────────────────────── -->
          <div v-if="nucCourses.length > 0" class="rounded-xl overflow-hidden" style="border:1px solid rgba(168,85,247,0.2);">
            <div class="px-4 py-2.5 flex items-center gap-2" style="background:rgba(168,85,247,0.06);">
              <span class="w-5 h-5 rounded bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-xs">🎯</span>
              <span class="text-xs font-bold text-purple-400 uppercase tracking-wider">NUC / Vocational Courses</span>
              <span class="ml-auto text-xs text-slate-600">Auto-loaded · Cannot be removed</span>
            </div>
            <div v-for="(course, idx) in nucCourses" :key="course.code"
                 class="grid grid-cols-[auto_1fr] sm:grid-cols-[auto_1fr_auto_auto_auto] gap-3 items-center px-4 py-3 transition-colors"
                 :class="idx % 2 === 0 ? 'bg-white/[0.015]' : ''">
              <div class="w-20">
                <span class="text-xs font-mono font-bold text-purple-300 bg-purple-500/10 px-2 py-0.5 rounded">
                  {{ course.code }}
                </span>
              </div>
              <div class="text-sm text-slate-300 leading-tight min-w-0">{{ course.title }}</div>
              <div class="hidden sm:flex w-12 justify-center">
                <span class="text-xs text-slate-500 bg-white/5 px-2 py-0.5 rounded">{{ course.units }}u</span>
              </div>
              <div v-if="!show100AlphaEntry" class="hidden sm:flex w-24 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="100" step="0.1"
                    v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`prev_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–100" />
                  <span v-if="fieldErrors[`prev_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`prev_${course.code}`] }}
                  </span>
                </div>
              </div>
              <div class="hidden sm:flex w-20 justify-center">
                <div class="relative w-full">
                  <input type="number" min="0" max="30" step="0.1"
                    v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 text-center w-full"
                    :class="fieldErrors[`ca_${course.code}`] ? 'border-red-500/70' : ''"
                    placeholder="0–30" />
                  <span v-if="fieldErrors[`ca_${course.code}`]"
                    class="absolute -bottom-4 left-0 text-[10px] text-red-400 whitespace-nowrap">
                    {{ fieldErrors[`ca_${course.code}`] }}
                  </span>
                </div>
              </div>
              <!-- Mobile -->
              <div class="sm:hidden col-span-2 flex gap-3 mt-1">
                <div v-if="!show100AlphaEntry" class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">Prev /100</label>
                  <input type="number" min="0" max="100" step="0.1" v-model.number="courseScores[course.code].prev"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5" placeholder="0–100" />
                </div>
                <div class="flex-1">
                  <label class="text-[10px] text-slate-600 uppercase tracking-wider">CA /30</label>
                  <input type="number" min="0" max="30" step="0.1" v-model.number="courseScores[course.code].ca"
                    class="form-input text-xs py-1.5 px-2 w-full mt-0.5" placeholder="0–30" />
                </div>
              </div>
            </div>
          </div>

          <!-- Global course error -->
          <p v-if="fieldErrors.courses" class="text-red-400 text-sm">⚠ {{ fieldErrors.courses }}</p>

        </div><!-- end course tables -->

        <!-- Submit Button -->
        <button
          class="btn-primary w-full py-4 text-base mt-7"
          @click="predict"
          :disabled="loading || showSIWESWarning">
          <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full anim-spin"></span>
          <span>{{ loading ? 'Analysing...' : '⚡ Predict Performance' }}</span>
        </button>

      </div><!-- end form panel -->

      <!-- ── Result Panel ─────────────────────────────────────────────────── -->
      <div class="glass-card p-6 xl:w-[400px] shrink-0 flex flex-col justify-center anim-slide-right">

        <!-- Empty state -->
        <div v-if="!result && !errorMsg && !loading" class="flex flex-col items-center text-center py-10 gap-4">
          <div class="w-20 h-20 rounded-full flex items-center justify-center text-4xl"
               style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);">🎓</div>
          <div>
            <p class="text-white font-semibold mb-1">AI Result Panel</p>
            <p class="text-slate-500 text-sm leading-relaxed">
              Fill in the student profile and enter course scores,<br/>
              then click <strong class="text-slate-400">Predict Performance</strong>.
            </p>
          </div>
          <div class="w-full mt-2 space-y-2 opacity-30">
            <div class="h-3 rounded-full anim-shimmer" style="background:rgba(99,102,241,0.2);"></div>
            <div class="h-3 rounded-full anim-shimmer w-3/4" style="background:rgba(99,102,241,0.15);"></div>
            <div class="h-3 rounded-full anim-shimmer w-1/2" style="background:rgba(99,102,241,0.1);"></div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex flex-col items-center py-12 gap-5">
          <div class="relative w-16 h-16">
            <div class="absolute inset-0 border-2 border-indigo-500/20 rounded-full"></div>
            <div class="absolute inset-0 border-2 border-t-indigo-400 border-r-violet-400 rounded-full anim-spin"></div>
            <div class="absolute inset-2 border-2 border-t-violet-400 border-r-cyan-400 rounded-full anim-spin" style="animation-direction:reverse;animation-duration:0.7s;"></div>
          </div>
          <div class="text-center">
            <p class="text-white font-semibold">Analysing Profile…</p>
            <p class="text-slate-400 text-xs mt-1">Running 4 ML models in parallel</p>
          </div>
          <div class="flex gap-1.5">
            <span v-for="n in 4" :key="n" class="w-2 h-2 rounded-full bg-indigo-400 anim-pulse" :style="`animation-delay:${(n-1)*0.2}s`"></span>
          </div>
        </div>

        <!-- Error -->
        <div v-if="errorMsg && !loading" class="p-4 rounded-xl text-sm text-red-300 leading-relaxed"
             style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3);">
          ⚠️ {{ errorMsg }}
        </div>

        <!-- Success -->
        <div v-if="result && !loading" class="flex flex-col gap-4 anim-scale-in">

          <!-- Student ID badge -->
          <div v-if="result.student_id" class="text-xs text-slate-500 text-center">
            Record for <span class="text-slate-300 font-semibold font-mono">{{ result.student_id }}</span>
          </div>

          <!-- Outcome ring -->
          <div class="rounded-2xl p-5 flex items-center gap-5"
               :style="`background:${predictionColor.bg};border:1px solid ${predictionColor.border};`">
            <div class="relative w-20 h-20 shrink-0">
              <svg class="w-20 h-20 -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="10"/>
                <circle cx="50" cy="50" r="45" fill="none"
                        :stroke="predictionColor.text" stroke-width="10"
                        stroke-linecap="round"
                        :stroke-dasharray="283"
                        :stroke-dashoffset="ringOffset"
                        style="transition:stroke-dashoffset 1.4s cubic-bezier(0.4,0,0.2,1);"/>
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-lg font-black" :style="`color:${predictionColor.text}`">{{ gpaScore }}%</span>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-semibold tracking-widest text-slate-400 mb-1">PREDICTED OUTCOME</div>
              <div class="text-2xl font-black mb-2" :style="`color:${predictionColor.text}`">
                {{ predictionIcon }} {{ result.prediction }}
              </div>
              <RiskBadge :level="riskLevel" size="md" />
            </div>
          </div>

          <!-- Confidence bar -->
          <div>
            <div class="flex justify-between text-xs mb-1.5">
              <span class="text-slate-400 font-semibold uppercase tracking-wider">Model Confidence</span>
              <span class="font-black text-white">{{ confidenceScore }}%</span>
            </div>
            <div class="h-2.5 rounded-full" style="background:rgba(255,255,255,0.06);">
              <div class="h-2.5 rounded-full transition-all duration-1000"
                   :style="`width:${confidenceScore}%;background:linear-gradient(90deg,${predictionColor.text}99,${predictionColor.text});`"></div>
            </div>
          </div>

          <!-- Class Probabilities -->
          <div v-if="result.probabilities">
            <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Class Probabilities</div>
            <div class="flex flex-col gap-2">
              <div v-for="cls in classOrder" :key="cls" v-if="result.probabilities[cls] !== undefined">
                <div class="flex justify-between text-xs mb-1">
                  <span class="text-slate-300 font-medium">{{ cls }}</span>
                  <span class="font-bold" :style="`color:${probColor(cls)}`">{{ result.probabilities[cls] }}%</span>
                </div>
                <div class="h-2 rounded-full" style="background:rgba(255,255,255,0.06);">
                  <div class="h-2 rounded-full"
                       :style="`width:${result.probabilities[cls]}%;background:${probColor(cls)}99;`"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Derived Stats -->
          <div v-if="result.derived" class="grid grid-cols-3 gap-2 text-center">
            <div class="p-2 rounded-lg" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);">
              <div class="text-xs text-slate-500 mb-0.5">Prev Avg</div>
              <div class="font-bold text-slate-200 text-sm">{{ result.derived.Previous_Course_Average?.toFixed(1) }}</div>
            </div>
            <div class="p-2 rounded-lg" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);">
              <div class="text-xs text-slate-500 mb-0.5">CA Avg</div>
              <div class="font-bold text-slate-200 text-sm">{{ result.derived.Course_CA_Average?.toFixed(1) }}</div>
            </div>
            <div class="p-2 rounded-lg" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);">
              <div class="text-xs text-slate-500 mb-0.5">Units</div>
              <div class="font-bold text-slate-200 text-sm">{{ result.derived.Total_Units }}</div>
            </div>
          </div>

          <!-- Sparkline -->
          <div v-if="sparklineData" class="p-4 rounded-xl"
               style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);">
            <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <span>📉</span> Projected Performance Trend
            </div>
            <div style="height:90px;">
              <Line :data="sparklineData" :options="sparklineOptions" />
            </div>
          </div>

          <!-- AI Narrative -->
          <div class="p-4 rounded-xl text-sm leading-relaxed"
               style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);">
            <div class="text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <span>🧠</span> AI Explanation
            </div>
            <p class="text-slate-300">{{ aiNarrative }}</p>
          </div>

          <!-- Key Factors -->
          <div v-if="result.explanations?.length">
            <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Key Factors</div>
            <div class="flex flex-col gap-2">
              <div v-for="exp in result.explanations" :key="exp.feature"
                   class="flex items-start gap-3 p-3 rounded-xl text-sm"
                   style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.06);">
                <span class="font-black text-base shrink-0" :style="`color:${impactColor(exp.impact)}`">{{ impactIcon(exp.impact) }}</span>
                <div>
                  <div class="font-semibold text-white text-xs mb-0.5">{{ exp.label }}</div>
                  <div class="text-slate-400 text-xs leading-relaxed">{{ exp.detail }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recommended Action -->
          <div class="mt-2 p-4 rounded-xl border border-indigo-500/30 bg-indigo-900/20">
            <div class="text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              🎯 Recommended Action
            </div>
            <p class="text-slate-300 text-sm mb-3">
              {{ riskLevel === 'high' ? 'High priority intervention needed. Schedule academic advising immediately.'
               : riskLevel === 'medium' ? 'Review study habits and consider peer tutoring or study groups.'
               : 'No immediate action required. Encourage continued excellent performance.' }}
            </p>
            <button @click="router.push('/interventions')"
              class="w-full btn-ghost py-2 text-sm border-indigo-500/50 hover:bg-indigo-500/20 text-indigo-300 hover:text-white">
              View Intervention Strategies →
            </button>
          </div>

        </div><!-- end success -->
      </div><!-- end result panel -->
    </div><!-- end single tab -->

    <!-- ── Batch Upload Tab ──────────────────────────────────────────────── -->
    <div v-if="activeTab === 'batch'" class="anim-fade-up delay-1 max-w-3xl mx-auto">
      <div class="glass-card p-8">
        <h2 class="text-xl font-bold text-white mb-2 flex items-center gap-2">
          <span class="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-sm">📁</span>
          Batch Predictions
        </h2>
        <p class="text-slate-400 text-sm mb-2">
          Upload a CSV or Excel file with model-ready CS student data. The file must include all 17 feature columns below.
          <strong class="text-slate-300">Do not include Performance_Status</strong> — the model predicts it.
        </p>

        <!-- Required Columns Info -->
        <div class="mb-6 p-4 rounded-xl text-xs" style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.2);">
          <div class="font-bold text-indigo-300 mb-2 uppercase tracking-wider">Required Columns</div>
          <div class="flex flex-wrap gap-1.5">
            <span v-for="col in ['Gender','Age','Socioeconomic_Status','Level','Semester','Study_Hours_Per_Week','Previous_CGPA',
                                  'Previous_Course_Average','Lowest_Previous_Score','Weak_Previous_Count',
                                  'Course_CA_Average','Lowest_CA_Score','Weak_CA_Count',
                                  'Core_CA_Average','Elective_CA_Average','University_CA_Average','Total_Units']"
                  :key="col"
                  class="px-2 py-0.5 rounded font-mono"
                  style="background:rgba(99,102,241,0.15);color:#a5b4fc;border:1px solid rgba(99,102,241,0.2);">
            {{ col }}
          </span>
          </div>
          <p class="text-slate-500 mt-2">Optional: include <code class="text-slate-400">Student_ID</code> for tracking (not a model feature).</p>
        </div>

        <!-- Drop Zone -->
        <div
          class="border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center text-center transition-all duration-300 mb-6 relative overflow-hidden"
          :class="isDragging ? 'border-indigo-400 bg-indigo-500/20 scale-[1.02] shadow-[0_0_30px_rgba(99,102,241,0.2)]' : 'border-indigo-500/30 bg-indigo-500/5 hover:border-indigo-500/60'"
          @dragenter.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @dragover.prevent="isDragging = true"
          @drop.prevent="handleFileDrop"
        >
          <input type="file" ref="fileInput" accept=".csv,.xlsx" class="hidden" @change="handleFileChange" />

          <div class="text-5xl mb-4 opacity-50 transition-transform duration-300" :class="isDragging ? 'scale-125 -translate-y-2' : ''">📄</div>
          <h3 class="text-lg font-bold text-white mb-1">Drag & Drop or Paste your file here</h3>
          <p class="text-slate-400 text-sm mb-4" :class="isDragging ? 'opacity-0' : 'opacity-100'">
            Accepts .csv or .xlsx files
          </p>
          <button class="btn-ghost text-sm" :class="isDragging ? 'opacity-0' : 'opacity-100'" @click="$refs.fileInput.click()">
            Browse Files
          </button>

          <!-- File selected overlay -->
          <div v-if="selectedFile" class="absolute inset-0 bg-slate-900/95 backdrop-blur-md rounded-2xl flex flex-col items-center justify-center p-6 anim-fade-in z-10 border border-emerald-500/30">
            <div class="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center mb-3 text-emerald-400 border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
              <span class="text-2xl">✓</span>
            </div>
            <div class="text-white font-bold mb-1 truncate max-w-full px-4 text-lg">{{ selectedFile.name }}</div>
            <div class="text-slate-400 text-sm mb-4 flex items-center gap-2">
              <span>{{ (selectedFile.size / 1024).toFixed(1) }} KB</span>
              <span v-if="filePreview?.rowCount" class="text-slate-600">•</span>
              <span v-if="filePreview?.rowCount" class="text-indigo-400 font-medium">{{ filePreview.rowCount }} rows detected</span>
            </div>
            <!-- Mini preview -->
            <div v-if="filePreview?.previewRows?.length" class="w-full max-w-md bg-slate-800/60 rounded-xl p-3 mb-4 overflow-x-auto text-left text-xs border border-white/10">
              <div class="text-slate-400 mb-2 uppercase tracking-widest font-bold text-[10px]">Data Preview</div>
              <div class="flex gap-4 border-b border-white/10 pb-1.5 mb-1.5 font-mono text-slate-300 font-semibold">
                <div v-for="header in filePreview.headers.slice(0,4)" :key="header" class="w-20 shrink-0 truncate">{{ header }}</div>
                <div v-if="filePreview.headers.length > 4" class="text-slate-500 italic">...</div>
              </div>
              <div v-for="(row, idx) in filePreview.previewRows" :key="idx" class="flex gap-4 py-1 font-mono text-slate-400">
                <div v-for="(cell, cidx) in row.slice(0,4)" :key="cidx" class="w-20 shrink-0 truncate">{{ cell }}</div>
                <div v-if="row.length > 4" class="text-slate-500 italic">...</div>
              </div>
            </div>
            <button class="btn-ghost text-xs hover:bg-red-500/20 hover:text-red-300 hover:border-red-500/30 transition-all"
              @click.stop="selectedFile = null; filePreview = null; batchError = ''">
              Remove File
            </button>
          </div>
        </div>

        <!-- Feedback -->
        <div v-if="batchError" class="p-4 rounded-xl text-sm text-red-300 leading-relaxed mb-6"
             style="background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.3);">
          ⚠️ {{ batchError }}
        </div>
        <div v-if="batchSuccess" class="p-4 rounded-xl text-sm text-emerald-300 leading-relaxed mb-6"
             style="background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3);">
          ✅ Predictions completed! The results file has been downloaded to your computer.
        </div>

        <!-- Replace Toggle -->
        <label class="flex items-center gap-3 p-4 rounded-xl cursor-pointer mb-4 transition-all duration-200"
               :class="replaceDataset ? 'bg-red-500/8 border border-red-500/25' : 'bg-white/3 border border-white/8 hover:bg-white/5'">
          <div class="relative shrink-0">
            <input type="checkbox" v-model="replaceDataset" class="sr-only" id="replaceToggle" />
            <div class="w-10 h-6 rounded-full transition-colors duration-200" :class="replaceDataset ? 'bg-red-500' : 'bg-slate-700'"></div>
            <div class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow transition-transform duration-200" :class="replaceDataset ? 'translate-x-4' : 'translate-x-0'"></div>
          </div>
          <div>
            <div class="text-sm font-semibold" :class="replaceDataset ? 'text-red-300' : 'text-slate-300'">Replace Existing Dataset</div>
            <div class="text-xs text-slate-500 mt-0.5">Clears all current records before inserting new batch predictions</div>
          </div>
          <span v-if="replaceDataset" class="ml-auto text-xs px-2 py-0.5 rounded-full font-bold"
                style="background:rgba(239,68,68,0.15);color:#EF4444;border:1px solid rgba(239,68,68,0.3);">REPLACE</span>
        </label>

        <!-- Submit -->
        <button
          class="btn-primary w-full py-4 text-base"
          @click="uploadBatch"
          :disabled="!selectedFile || batchLoading"
          :style="replaceDataset ? 'background:linear-gradient(135deg,#dc2626,#b91c1c);box-shadow:0 4px 20px rgba(239,68,68,0.3);' : ''">
          <span v-if="batchLoading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full anim-spin mr-2"></span>
          <span>{{ batchLoading ? 'Processing Batch...' : replaceDataset ? '🔄 Replace Dataset & Process' : 'Process and Download Results' }}</span>
        </button>
      </div>
    </div>

    <!-- Replace Confirmation Modal -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="showReplaceModal"
             class="fixed inset-0 z-50 flex items-center justify-center p-4"
             style="background:rgba(0,0,0,0.75);backdrop-filter:blur(8px);"
             @click.self="showReplaceModal = false">
          <div class="glass-card p-8 max-w-md w-full anim-scale-in"
               style="border-color:rgba(239,68,68,0.4);background:rgba(13,20,45,0.98);">
            <div class="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-5"
                 style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);">⚠️</div>
            <h2 class="text-2xl font-black text-white text-center mb-2">Replace Dataset?</h2>
            <p class="text-slate-400 text-sm text-center leading-relaxed mb-6">
              Uploading with <strong class="text-white">Replace Mode</strong> will:
            </p>
            <ul class="text-sm text-slate-400 space-y-2 mb-8">
              <li class="flex items-start gap-2"><span class="text-red-400 font-bold shrink-0">✗</span> Clear all existing prediction records</li>
              <li class="flex items-start gap-2"><span class="text-red-400 font-bold shrink-0">✗</span> Reset all dashboard analytics and charts</li>
              <li class="flex items-start gap-2"><span class="text-emerald-400 font-bold shrink-0">✓</span> Insert the new batch as the active dataset</li>
              <li class="flex items-start gap-2"><span class="text-emerald-400 font-bold shrink-0">✓</span> Regenerate all system insights from the new data</li>
            </ul>
            <div class="flex gap-3">
              <button class="flex-1 btn-ghost" @click="showReplaceModal = false">Cancel</button>
              <button class="flex-1 py-3 rounded-xl font-bold text-white transition-all"
                style="background:linear-gradient(135deg,#dc2626,#b91c1c);border:1px solid rgba(239,68,68,0.4);"
                @click="runBatchUpload(true)">
                🔄 Yes, Replace Dataset
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

  </div>
</template>
