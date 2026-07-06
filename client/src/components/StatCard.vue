<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  icon:    { type: String,  default: '📊' },
  label:   { type: String,  required: true },
  value:   { type: [String, Number], required: true },
  color:   { type: String,  default: '#6366F1' },
  trend:   { type: String,  default: '' },     // e.g. "+12%" or "-3%"
  trendUp: { type: Boolean, default: true },
})

const displayed = ref(0)
const isNumeric = (v) => !isNaN(parseFloat(v)) && isFinite(v)

const animateValue = () => {
  if (!isNumeric(props.value)) {
    displayed.value = props.value
    return
  }
  const target = parseFloat(props.value)
  const duration = 1200
  const start = performance.now()
  const step = (now) => {
    const progress = Math.min((now - start) / duration, 1)
    const ease = 1 - Math.pow(1 - progress, 3)
    displayed.value = Math.round(ease * target)
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}

onMounted(() => {
  animateValue()
})

watch(() => props.value, () => {
  animateValue()
})
</script>

<template>
  <div
    class="glass-card p-6 flex flex-col gap-3 group cursor-default transition-all duration-300
           hover:scale-[1.03] hover:shadow-[0_8px_40px_rgba(99,102,241,0.18)]"
    :style="`border-color: ${color}22;`"
  >
    <!-- Icon + Trend row -->
    <div class="flex items-center justify-between">
      <div
        class="w-11 h-11 rounded-xl flex items-center justify-center text-xl shrink-0"
        :style="`background: ${color}18; border: 1px solid ${color}33;`"
      >
        {{ icon }}
      </div>
      <span
        v-if="trend"
        class="text-xs font-bold px-2 py-0.5 rounded-full"
        :style="trendUp
          ? 'background:rgba(16,185,129,0.12);color:#10B981;border:1px solid rgba(16,185,129,0.25);'
          : 'background:rgba(239,68,68,0.12);color:#EF4444;border:1px solid rgba(239,68,68,0.25);'"
      >
        {{ trendUp ? '↑' : '↓' }} {{ trend }}
      </span>
    </div>

    <!-- Value -->
    <div
      class="text-3xl font-black text-white anim-counter-up"
      :style="`text-shadow: 0 0 20px ${color}44;`"
    >
      {{ isNumeric(value) ? displayed.toLocaleString() : value }}
    </div>

    <!-- Label -->
    <div class="text-sm text-slate-400 font-medium">{{ label }}</div>

    <!-- Bottom glow bar -->
    <div
      class="h-0.5 rounded-full w-0 group-hover:w-full transition-all duration-500"
      :style="`background: linear-gradient(90deg, ${color}, transparent);`"
    ></div>
  </div>
</template>
