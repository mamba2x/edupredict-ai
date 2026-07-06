<script setup>
defineProps({
  title: { type: String, required: true },
  icon:  { type: String, default: '📊' },
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <div class="glass-card p-6 flex flex-col gap-4 h-full">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-base shrink-0">
          {{ icon }}
        </div>
        <div>
          <h3 class="font-bold text-white text-base leading-tight">{{ title }}</h3>
          <p v-if="subtitle" class="text-slate-400 text-xs mt-0.5">{{ subtitle }}</p>
        </div>
      </div>
      <slot name="action" />
    </div>
    <div class="flex-1 min-h-0">
      <slot />
    </div>
  </div>
</template>
