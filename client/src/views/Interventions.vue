<script setup>
import { ref, computed } from 'vue'
import { store } from '../store.js'

// ── Data ────────────────────────────────────────────────────────────────────
const riskFilter   = ref('All')
const factorFilter = ref('All')

const riskOptions   = ['All', 'High Risk', 'Medium Risk', 'Low Risk']
const factorOptions = ['All', 'CA Scores', 'Study Hours', 'Socioeconomic', 'Assessment', 'Prior CGPA']

const interventions = [
  {
    id: 1,
    risk: 'High Risk',
    factor: 'CA Scores',
    priority: 'Critical',
    priorityColor: '#EF4444',
    borderColor: '#EF4444',
    icon: '🚨',
    title: 'Continuous Assessment (CA) Deficit Protocol',
    description: 'A high weak-CA count is the single strongest predictor of academic failure in this model (100% relative importance). Students with 3 or more weak CA scores require immediate multi-stakeholder intervention to prevent a compounding downward trajectory.',
    steps: [
      'Schedule a mandatory 1-on-1 academic coaching session within 48 hours.',
      'Identify the specific courses with weak CA scores and assign subject tutors.',
      'Design a remedial CA practice schedule with bi-weekly formative assessments.',
      'Engage parents/guardians via written notice if the student is below Level 200.',
      'Implement a CA recovery contract with measurable weekly improvement targets.',
    ],
    estimatedImprovement: 40,
    category: 'Immediate Action',
    completed: ref([false, false, false, false, false]),
  },
  {
    id: 2,
    risk: 'High Risk',
    factor: 'Study Hours',
    priority: 'Critical',
    priorityColor: '#EF4444',
    borderColor: '#F97316',
    icon: '📚',
    title: 'Study Deficit Intervention',
    description: 'Students logging fewer than 8 study hours per week consistently underperform. Structured academic support must be deployed immediately.',
    steps: [
      'Enroll in structured peer tutoring sessions (3x per week).',
      'Provide a personalised weekly study schedule tailored to their timetable.',
      'Supply supplementary interactive learning materials for each subject.',
      'Teach evidence-based study techniques: spaced repetition, active recall.',
      'Track progress weekly through CA performance scores.',
    ],
    estimatedImprovement: 35,
    category: 'Academic Support',
    completed: ref([false, false, false, false, false]),
  },
  {
    id: 3,
    risk: 'Medium Risk',
    factor: 'Assessment',
    priority: 'High',
    priorityColor: '#F59E0B',
    borderColor: '#F59E0B',
    icon: '📝',
    title: 'Continuous Assessment Improvement',
    description: 'A CA score below 20/50 indicates poor conceptual understanding and requires targeted academic remediation before final examinations.',
    steps: [
      'Identify specific topics where the student is underperforming.',
      'Arrange focused revision sessions with subject-specific tutors.',
      'Provide past exam papers with model answers for self-directed practice.',
      'Introduce formative micro-assessments every two weeks to track recovery.',
    ],
    estimatedImprovement: 28,
    category: 'Assessment Recovery',
    completed: ref([false, false, false, false]),
  },
  {
    id: 4,
    risk: 'High Risk',
    factor: 'Socioeconomic',
    priority: 'High',
    priorityColor: '#F59E0B',
    borderColor: '#8B5CF6',
    icon: '🏠',
    title: 'Socioeconomic Support Programme',
    description: 'Low socioeconomic status correlates strongly with resource scarcity. Institutional support must be mobilised to level the playing field.',
    steps: [
      'Provide school-supplied learning devices and data bundles.',
      'Ensure enrolment in the school meal programme.',
      'Connect the student and family with financial aid and scholarship offices.',
      'Offer access to on-campus study facilities outside class hours.',
    ],
    estimatedImprovement: 22,
    category: 'Welfare Support',
    completed: ref([false, false, false, false]),
  },
  {
    id: 5,
    risk: 'Medium Risk',
    factor: 'Prior CGPA',
    priority: 'Medium',
    priorityColor: '#6366F1',
    borderColor: '#6366F1',
    icon: '📊',
    title: 'Prior Academic Profile (CGPA) Recovery',
    description: 'A previous CGPA below 2.5 on Nigeria\'s 5-point scale signals a growing academic deficit. Early intervention prevents the student\'s performance trajectory from compounding downward into the At-Risk band.',
    steps: [
      'Conduct a detailed gap analysis of prior semester CA and exam scores.',
      'Design a targeted revision plan covering the student\'s weakest courses.',
      'Schedule fortnightly check-ins with the student\'s personal academic tutor.',
      'Set incremental short-term CGPA targets to build measurable momentum.',
    ],
    estimatedImprovement: 20,
    category: 'Academic Recovery',
    completed: ref([false, false, false, false]),
  },
  {
    id: 6,
    risk: 'Low Risk',
    factor: 'Study Hours',
    priority: 'Medium',
    priorityColor: '#10B981',
    borderColor: '#10B981',
    icon: '⭐',
    title: 'Excellence Acceleration Track',
    description: 'High-performing students still benefit from enrichment programmes that cultivate deeper mastery and develop competitive academic profiles.',
    steps: [
      'Nominate for advanced enrichment modules or honours programmes.',
      'Encourage participation in inter-institutional academic competitions.',
      'Facilitate access to research opportunities and mentorship.',
      'Support applications for academic excellence scholarships.',
    ],
    estimatedImprovement: 12,
    category: 'Enrichment',
    completed: ref([false, false, false, false]),
  },
]

const filtered = computed(() => {
  return interventions.filter(i => {
    const riskOk   = riskFilter.value   === 'All' || i.risk   === riskFilter.value
    const factorOk = factorFilter.value === 'All' || i.factor === factorFilter.value
    return riskOk && factorOk
  })
})

function toggleStep(intervention, idx) {
  intervention.completed.value[idx] = !intervention.completed.value[idx]
}

const completedCount = (i) => i.completed.value.filter(Boolean).length
const progressPct    = (i) => Math.round((completedCount(i) / i.steps.length) * 100)

const priorityBg = (p) => ({
  'Critical': 'rgba(239,68,68,0.15)',
  'High':     'rgba(245,158,11,0.15)',
  'Medium':   'rgba(99,102,241,0.15)',
})[p] ?? 'rgba(99,102,241,0.1)'

// Get applicable student count from store
const getApplicableCount = (riskLevel) => {
  if (riskLevel === 'High Risk') return store.stats.at_risk_count || 0
  if (riskLevel === 'Medium Risk') return store.stats.average_count || 0
  if (riskLevel === 'Low Risk') return store.stats.excellent_count || 0
  return 0
}
</script>

<template>
  <div class="min-h-screen px-6 py-10 max-w-6xl mx-auto">

    <!-- Header -->
    <div class="mb-10 anim-fade-up">
      <h1 class="text-4xl md:text-5xl font-black text-white mb-3">
        Pedagogical <span class="gradient-text">Interventions</span>
      </h1>
      <p class="text-slate-400 max-w-2xl leading-relaxed">
        Actionable, evidence-based strategies for educators. Filter by risk level or factor to surface the most relevant interventions. Check off steps as you complete them.
      </p>
    </div>

    <!-- Empty State — shown when no predictions exist -->
    <div v-if="store.stats.total_students === 0" class="glass-card p-16 text-center anim-fade-up"
         style="border: 1px dashed rgba(239,68,68,0.3); background: rgba(239,68,68,0.03);">
      <div class="w-20 h-20 rounded-2xl flex items-center justify-center text-4xl mx-auto mb-6 anim-float"
           style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);">🎯</div>
      <h2 class="text-2xl font-black text-white mb-3">No Predictions Available</h2>
      <p class="text-slate-400 max-w-lg mx-auto mb-8 leading-relaxed">
        Intervention strategies are generated based on your active student dataset.
        Run a batch prediction or upload a CSV file first to populate the system with academic records.
      </p>
      <div class="flex flex-wrap gap-4 justify-center">
        <router-link to="/predict" class="btn-primary text-base px-8 py-3.5">⚡ Upload Dataset</router-link>
        <router-link to="/insights" class="btn-ghost">📊 View Model Insights</router-link>
      </div>
    </div>

    <!-- Content — only shown when predictions exist -->
    <template v-else>

    <!-- AI Insight Panel -->
    <div class="glass-card p-6 mb-8 anim-fade-up delay-1"
         style="border-left: 3px solid #6366F1; background: rgba(99,102,241,0.06);">
      <div class="flex items-start gap-4 mb-5">
        <div class="w-10 h-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 text-lg">🧠</div>
        <div>
          <div class="text-xs font-bold text-indigo-300 uppercase tracking-widest mb-1">AI Advisory Summary</div>
          <p class="text-slate-300 text-sm leading-relaxed">
            Based on the trained model's feature importance analysis, <strong class="text-white">weak CA count</strong> and <strong class="text-white">core course CA average</strong> are the top two predictors of academic outcome, accounting for 100% and 91.8% of relative feature importance respectively. Students flagged as <span class="text-red-400 font-semibold">High Risk</span> typically exhibit compounding CA deficits across multiple courses — requiring a holistic, multi-intervention approach rather than a single targeted action. Interventions should be prioritised by severity and reviewed fortnightly.
          </p>
        </div>
      </div>
      
      <!-- Live Risk Summary Bar -->
      <div class="p-3 rounded-lg flex flex-wrap items-center justify-between gap-4 border border-white/10 bg-white/5">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-red-500 anim-pulse"></span>
          <span class="text-sm font-semibold text-white">{{ store.stats.at_risk_count }}</span>
          <span class="text-xs text-slate-400">High Risk</span>
        </div>
        <div class="w-px h-4 bg-white/10 hidden sm:block"></div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span>
          <span class="text-sm font-semibold text-white">{{ store.stats.average_count }}</span>
          <span class="text-xs text-slate-400">Medium Risk</span>
        </div>
        <div class="w-px h-4 bg-white/10 hidden sm:block"></div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span class="text-sm font-semibold text-white">{{ store.stats.excellent_count }}</span>
          <span class="text-xs text-slate-400">Low Risk</span>
        </div>
      </div>
    </div>

    <!-- Filter Panel -->
    <div class="glass-card p-5 mb-8 flex flex-col sm:flex-row gap-5 anim-fade-up delay-1">
      <div class="flex-1">
        <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Filter by Risk Level</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="opt in riskOptions" :key="opt"
            @click="riskFilter = opt"
            class="px-3 py-1.5 rounded-full text-xs font-semibold border transition-all duration-200"
            :class="riskFilter === opt
              ? 'bg-indigo-600 text-white border-indigo-500'
              : 'text-slate-400 border-white/10 hover:text-white hover:border-white/20'"
          >{{ opt }}</button>
        </div>
      </div>
      <div class="w-px bg-white/10 hidden sm:block"></div>
      <div class="flex-1">
        <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Filter by Risk Factor</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="opt in factorOptions" :key="opt"
            @click="factorFilter = opt"
            class="px-3 py-1.5 rounded-full text-xs font-semibold border transition-all duration-200"
            :class="factorFilter === opt
              ? 'bg-violet-600 text-white border-violet-500'
              : 'text-slate-400 border-white/10 hover:text-white hover:border-white/20'"
          >{{ opt }}</button>
        </div>
      </div>
    </div>

    <!-- Results Count -->
    <div class="text-xs text-slate-500 mb-5 anim-fade-up">
      Showing <span class="text-white font-bold">{{ filtered.length }}</span> of {{ interventions.length }} interventions
    </div>

    <!-- Intervention Cards -->
    <div v-if="filtered.length === 0" class="glass-card p-12 text-center anim-fade-up">
      <div class="text-5xl mb-4">🔍</div>
      <p class="text-slate-400">No interventions match the selected filters.</p>
    </div>

    <div class="flex flex-col gap-6 anim-fade-up delay-2">
      <div
        v-for="item in filtered" :key="item.id"
        class="glass-card p-6 transition-all duration-300 hover:shadow-[0_8px_30px_rgba(0,0,0,0.3)] hover:-translate-y-0.5"
        :style="`border-left: 4px solid ${item.borderColor};`"
      >
        <!-- Card Header -->
        <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-5">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shrink-0"
                 :style="`background: ${item.borderColor}20; border: 1px solid ${item.borderColor}40;`">
              {{ item.icon }}
            </div>
            <div>
              <div class="flex items-center gap-2 flex-wrap mb-1">
                <span class="text-xs font-bold px-2.5 py-0.5 rounded-full"
                      :style="`background: ${priorityBg(item.priority)}; color: ${item.priorityColor};`">
                  {{ item.priority }}
                </span>
                <span class="text-xs text-slate-500 font-medium">{{ item.category }}</span>
              </div>
              <h2 class="text-lg font-bold text-white">{{ item.title }}</h2>
              <div class="flex items-center gap-2 mt-1 flex-wrap">
                <span class="text-xs text-slate-500 font-medium">{{ item.risk }}</span>
                <span class="text-slate-700">·</span>
                <span class="text-xs text-slate-500">Factor: <span class="text-slate-300">{{ item.factor }}</span></span>
                <span class="text-slate-700">·</span>
                <span class="text-xs px-2 py-0.5 rounded border" :style="`color: ${item.borderColor}; border-color: ${item.borderColor}40; background: ${item.borderColor}10`">
                  Applicable to {{ getApplicableCount(item.risk) }} students
                </span>
              </div>
            </div>
          </div>

          <!-- Estimated Improvement -->
          <div class="shrink-0 text-center p-3 rounded-xl sm:w-28"
               style="background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.2);">
            <div class="text-2xl font-black text-indigo-400">+{{ item.estimatedImprovement }}%</div>
            <div class="text-xs text-slate-400 mt-0.5">Est. Improvement</div>
          </div>
        </div>

        <!-- Description -->
        <p class="text-slate-400 text-sm leading-relaxed mb-5">{{ item.description }}</p>

        <!-- Action Steps -->
        <div class="mb-5">
          <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Action Steps</div>
          <div class="flex flex-col gap-2.5">
            <label
              v-for="(step, idx) in item.steps" :key="idx"
              class="flex items-start gap-3 p-3 rounded-xl cursor-pointer transition-all duration-200"
              :class="item.completed.value[idx] ? 'bg-emerald-500/8 border border-emerald-500/20' : 'bg-white/3 border border-white/5 hover:bg-white/5'"
              @click="toggleStep(item, idx)"
            >
              <div class="w-5 h-5 rounded-md border flex items-center justify-center shrink-0 mt-0.5 transition-all duration-200"
                   :class="item.completed.value[idx]
                     ? 'bg-emerald-500 border-emerald-500'
                     : 'border-slate-600'">
                <svg v-if="item.completed.value[idx]" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <span class="text-sm transition-colors"
                    :class="item.completed.value[idx] ? 'text-emerald-300 line-through opacity-70' : 'text-slate-300'">
                {{ step }}
              </span>
            </label>
          </div>
        </div>

        <!-- Progress Bar -->
        <div>
          <div class="flex justify-between text-xs mb-2">
            <span class="text-slate-400 font-semibold uppercase tracking-wider">Progress</span>
            <span class="font-black text-white">{{ completedCount(item) }}/{{ item.steps.length }} steps · {{ progressPct(item) }}%</span>
          </div>
          <div class="h-2 rounded-full" style="background: rgba(255,255,255,0.06);">
            <div class="h-2 rounded-full transition-all duration-500"
                 :style="`width: ${progressPct(item)}%; background: linear-gradient(90deg, #6366F1, #8B5CF6);`"></div>
          </div>
        </div>

      </div>
    </div>

    </template><!-- end v-else -->

  </div>
</template>
