<script setup>
const props = defineProps({
  level: { type: String, required: true }, // 'low' | 'medium' | 'high'
  size:  { type: String, default: 'md' },   // 'sm' | 'md' | 'lg'
})

const config = {
  low:    { label: 'Low Risk',    bg: 'rgba(16,185,129,0.12)',  border: 'rgba(16,185,129,0.35)',  text: '#10B981', dot: '#10B981' },
  medium: { label: 'Medium Risk', bg: 'rgba(245,158,11,0.12)',  border: 'rgba(245,158,11,0.35)',  text: '#F59E0B', dot: '#F59E0B' },
  high:   { label: 'High Risk',   bg: 'rgba(239,68,68,0.12)',   border: 'rgba(239,68,68,0.35)',   text: '#EF4444', dot: '#EF4444' },
}

const sizeClass = {
  sm: 'text-[10px] px-2 py-0.5 gap-1',
  md: 'text-xs    px-3 py-1   gap-1.5',
  lg: 'text-sm    px-4 py-1.5 gap-2',
}
</script>

<template>
  <span
    class="inline-flex items-center font-bold rounded-full"
    :class="sizeClass[size]"
    :style="`background:${config[level]?.bg};border:1px solid ${config[level]?.border};color:${config[level]?.text};`"
  >
    <span
      class="rounded-full anim-pulse"
      :class="size === 'lg' ? 'w-2.5 h-2.5' : 'w-1.5 h-1.5'"
      :style="`background:${config[level]?.dot};`"
    ></span>
    {{ config[level]?.label ?? level }}
  </span>
</template>
