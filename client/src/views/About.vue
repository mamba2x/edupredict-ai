<script setup>
// No reactive data needed — purely presentational
</script>

<template>
  <div class="min-h-screen px-6 py-10 max-w-4xl mx-auto">

    <!-- Header -->
    <div class="text-center mb-12 anim-fade-up">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold mb-5"
           style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.3);color:#A5B4FC;">
        <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 anim-pulse inline-block"></span>
        Final Year Project · Academic ML System
      </div>
      <h1 class="text-4xl md:text-5xl font-black text-white mb-4">
        Project <span class="gradient-text">Methodology</span>
      </h1>
      <p class="text-slate-400 max-w-xl mx-auto leading-relaxed">
        A detailed overview of the system architecture, datasets, and machine learning models powering this academic intelligence platform.
      </p>
    </div>

    <!-- Abstract -->
    <div class="glass-card p-8 mb-6 anim-fade-up delay-1"
         style="border-left: 3px solid #6366F1;">
      <div class="flex items-start gap-4 mb-4">
        <div class="w-10 h-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-lg shrink-0">📄</div>
        <div>
          <div class="text-xs font-bold text-indigo-300 uppercase tracking-widest mb-1">Abstract</div>
          <h2 class="text-xl font-bold text-white">Student Academic Performance Prediction System</h2>
        </div>
      </div>
      <p class="text-slate-300 leading-relaxed">
        This system is designed to proactively identify Computer Science students who are at risk of underperforming. By analysing course-specific Continuous Assessment (CA) scores, previous CGPA, and key academic indicators across core, elective, and university-wide courses, the system employs an ensemble of machine learning algorithms to forecast a student's final academic standing. Early identification enables educators to implement targeted interventions, thereby improving overall student success rates.
      </p>
    </div>

    <!-- Architecture Grid -->
    <div class="mb-6 anim-fade-up delay-2">
      <div class="flex items-center gap-3 mb-5">
        <div class="w-9 h-9 rounded-lg bg-violet-600/20 border border-violet-500/30 flex items-center justify-center text-base">🏗️</div>
        <h2 class="text-xl font-bold text-white">System Architecture</h2>
      </div>
      <div class="grid md:grid-cols-2 gap-5">

        <!-- Frontend Card -->
        <div class="glass-card p-6" style="border-left: 3px solid #6366F1;">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-9 h-9 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-sm">🖥️</div>
            <h3 class="text-indigo-400 font-bold text-base">Frontend</h3>
          </div>
          <ul class="space-y-3">
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">Framework:</strong> Vue 3 with Composition API</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">Styling:</strong> Tailwind CSS v4 + Custom Glassmorphism UI</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">Charts:</strong> Chart.js via vue-chartjs</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">Routing:</strong> Vue Router 4 (SPA)</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">HTTP Client:</strong> Axios</span>
            </li>
          </ul>
        </div>

        <!-- Backend Card -->
        <div class="glass-card p-6" style="border-left: 3px solid #10B981;">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-9 h-9 rounded-lg bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-sm">⚙️</div>
            <h3 class="text-emerald-400 font-bold text-base">Backend</h3>
          </div>
          <ul class="space-y-3">
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">Framework:</strong> FastAPI (Python 3.11)</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">ML Library:</strong> Scikit-Learn · Pandas · NumPy</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">Database:</strong> SQLite (prediction history)</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">Serialisation:</strong> Joblib (ML pipeline storage)</span>
            </li>
            <li class="flex items-start gap-3 text-sm">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0"></span>
              <span class="text-slate-300"><strong class="text-white">CORS:</strong> Enabled for local Vue dev server</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- ML Approach -->
    <div class="glass-card p-8 mb-6 anim-fade-up delay-3">
      <div class="flex items-center gap-3 mb-5">
        <div class="w-9 h-9 rounded-lg bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-base">🤖</div>
        <h2 class="text-xl font-bold text-white">Machine Learning Approach</h2>
      </div>
      <p class="text-slate-300 leading-relaxed mb-6">
        The predictive engine uses an ensemble of four machine learning algorithms trained on a curated educational dataset. Each model is evaluated independently via cross-validation, and the best-performing model is automatically selected as the live predictor. A preprocessing pipeline handles categorical encoding, feature scaling, and train/test splitting automatically.
      </p>

      <!-- 4 Model Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <div v-for="(m, i) in models" :key="m.name"
             class="rounded-xl p-4 text-center transition-all duration-200 hover:-translate-y-1"
             :style="`background: ${m.color}10; border: 1px solid ${m.color}30;`">
          <div class="text-2xl mb-2">{{ m.icon }}</div>
          <div class="text-xs font-bold text-white leading-tight">{{ m.name }}</div>
          <div class="text-xs mt-1 font-semibold" :style="`color: ${m.color}`">{{ m.tag }}</div>
        </div>
      </div>

      <!-- Key Features -->
      <div>
        <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Key Predictive Features</div>
        <div class="flex flex-wrap gap-2">
          <span v-for="f in features" :key="f"
                class="px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors hover:border-indigo-400 hover:text-indigo-300"
                style="background:rgba(99,102,241,0.08);border-color:rgba(99,102,241,0.2);color:#A5B4FC;">
            {{ f }}
          </span>
        </div>
      </div>
    </div>

    <!-- Dataset & Pipeline -->
    <div class="grid md:grid-cols-2 gap-5 mb-6 anim-fade-up delay-4">

      <!-- Dataset -->
      <div class="glass-card p-6" style="border-left: 3px solid #F59E0B;">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-9 h-9 rounded-lg bg-amber-600/20 border border-amber-500/30 flex items-center justify-center text-sm">📊</div>
          <h3 class="text-amber-400 font-bold">Dataset</h3>
        </div>
        <div class="space-y-3">
          <div class="flex justify-between items-center py-2 border-b border-white/5">
            <span class="text-slate-400 text-sm">Total Records</span>
            <span class="text-white font-bold">1,120 students</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-white/5">
            <span class="text-slate-400 text-sm">Training Set</span>
            <span class="text-white font-bold">896 records</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-white/5">
            <span class="text-slate-400 text-sm">Test Set</span>
            <span class="text-white font-bold">224 records</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-white/5">
            <span class="text-slate-400 text-sm">Feature Columns</span>
            <span class="text-white font-bold">17 inputs</span>
          </div>
          <div class="flex justify-between items-center py-2 border-b border-white/5">
            <span class="text-slate-400 text-sm">Target Classes</span>
            <span class="text-white font-bold">3 (Excellent / Average / At-Risk)</span>
          </div>
          <div class="flex justify-between items-center py-2">
            <span class="text-slate-400 text-sm">Train / Test Split</span>
            <span class="text-white font-bold">80% / 20%</span>
          </div>
        </div>
      </div>

      <!-- Pipeline -->
      <div class="glass-card p-6" style="border-left: 3px solid #06B6D4;">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-9 h-9 rounded-lg bg-cyan-600/20 border border-cyan-500/30 flex items-center justify-center text-sm">🔄</div>
          <h3 class="text-cyan-400 font-bold">Processing Pipeline</h3>
        </div>
        <div class="space-y-2.5">
          <div v-for="(step, i) in pipeline" :key="i"
               class="flex items-center gap-3 p-2.5 rounded-lg text-sm"
               style="background:rgba(255,255,255,0.03);">
            <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-black shrink-0"
                 style="background:rgba(6,182,212,0.15);color:#06B6D4;">{{ i + 1 }}</div>
            <span class="text-slate-300">{{ step }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Prediction Outcomes Reference -->
    <div class="glass-card p-8 anim-fade-up delay-5">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-9 h-9 rounded-lg bg-green-600/20 border border-green-500/30 flex items-center justify-center text-base">🎯</div>
        <h2 class="text-xl font-bold text-white">Prediction Outcome Classes</h2>
      </div>
      <div class="grid md:grid-cols-3 gap-4">
        <div v-for="cls in outcomes" :key="cls.label"
             class="rounded-xl p-5 text-center"
             :style="`background: ${cls.color}10; border: 1px solid ${cls.color}30;`">
          <div class="text-3xl mb-2">{{ cls.icon }}</div>
          <div class="font-black text-lg mb-1" :style="`color: ${cls.color}`">{{ cls.label }}</div>
          <p class="text-slate-400 text-xs leading-relaxed">{{ cls.desc }}</p>
          <div class="mt-3 text-xs font-bold px-2 py-1 rounded-full inline-block"
               :style="`background: ${cls.color}15; color: ${cls.color};`">
            {{ cls.range }}
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
// Using Options API for the static data to keep setup() clean
export default {
  data() {
    return {
      models: [
        { name: 'Logistic Regression', icon: '📐', color: '#6366F1', tag: 'Baseline' },
        { name: 'Random Forest',       icon: '🌲', color: '#10B981', tag: 'Best ★' },
        { name: 'Gradient Boosting',   icon: '🚀', color: '#F59E0B', tag: 'Boosting' },
        { name: 'Support Vector',      icon: '⚡', color: '#EF4444', tag: 'Kernel' },
      ],
      features: [
        'Weak CA Count', 'Core Course CA Average', 'Course CA Average',
        'Lowest CA Score', 'Previous CGPA', 'Previous Course Average',
        'Study Hours/Week', 'Weak Previous Courses', 'University CA Average',
        'Elective CA Average', 'Gender', 'Age', 'Level', 'Semester',
        'Socioeconomic Status', 'Study Group Participation', 'Library Usage',
      ],
      pipeline: [
        'CSV data ingestion & validation',
        'Categorical encoding (Label / One-Hot)',
        'Feature scaling (StandardScaler)',
        'Stratified 80/20 train-test split',
        'Model training & cross-validation',
        'Best model serialised via Joblib',
      ],
      outcomes: [
        { label: 'Excellent', icon: '🌟', color: '#10B981', range: 'Top performers', desc: 'Student is on track for strong academic results. Continue current strategies.' },
        { label: 'Average',   icon: '📘', color: '#F59E0B', range: 'Mid-range',      desc: 'Student is progressing adequately but has room for targeted improvement.' },
        { label: 'At-Risk',   icon: '⚠️', color: '#EF4444', range: 'Needs support', desc: 'Student shows indicators of potential failure. Immediate intervention advised.' },
      ],
    }
  }
}
</script>
