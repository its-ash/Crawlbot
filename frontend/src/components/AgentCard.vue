<template>
  <div class="card group cursor-pointer">
    <div class="absolute top-3 left-3 flex gap-1">
      <div class="w-2 h-2 rounded-full bg-muted shadow-recessed"></div>
      <div class="w-2 h-2 rounded-full bg-muted shadow-recessed"></div>
      <div class="w-2 h-2 rounded-full bg-muted shadow-recessed"></div>
    </div>

    <div class="absolute top-3 right-3 flex gap-1">
      <div class="h-6 w-0.5 rounded-full bg-muted shadow-recessed"></div>
      <div class="h-6 w-0.5 rounded-full bg-muted shadow-recessed"></div>
      <div class="h-6 w-0.5 rounded-full bg-muted shadow-recessed"></div>
    </div>

    <div class="mt-8 mb-4">
      <div class="flex items-start justify-between mb-3">
        <div class="flex-1">
          <h3 class="text-xl font-bold mb-1 drop-shadow-embossed">{{ agent.name }}</h3>
          <p class="text-xs font-mono uppercase tracking-wider text-text-muted">
            {{ agent.search_engine }}
          </p>
        </div>
        
        <div :class="statusLEDClass"></div>
      </div>

      <div class="bg-muted rounded-md p-3 shadow-recessed mb-4">
        <p class="text-sm font-mono text-text-muted">{{ agent.keywords }}</p>
      </div>

      <div v-if="agent.status === 'running'" class="mb-4">
        <div class="flex justify-between text-xs font-mono mb-2">
          <span class="text-text-muted">PROGRESS</span>
          <span class="text-accent font-bold">{{ agent.progress }}/{{ agent.total_sites }}</span>
        </div>
        <div class="h-2 bg-muted rounded-full shadow-recessed overflow-hidden">
          <div 
            class="h-full bg-accent transition-all duration-300"
            :style="{ width: progressPercent + '%' }"
          ></div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-2 mb-4">
        <div class="bg-muted rounded p-2 shadow-recessed">
          <div class="text-xs font-mono uppercase tracking-wide text-text-muted mb-1">Status</div>
          <div class="text-sm font-bold uppercase">{{ agent.status }}</div>
        </div>
        <div class="bg-muted rounded p-2 shadow-recessed">
          <div class="text-xs font-mono uppercase tracking-wide text-text-muted mb-1">Results</div>
          <div class="text-sm font-bold font-mono">{{ agent.results_count || 0 }}</div>
        </div>
      </div>
    </div>

    <div class="flex gap-2">
      <button 
        v-if="agent.status !== 'running'"
        @click.stop="$emit('start', agent.id)"
        class="flex-1 btn-secondary text-sm py-2 px-4 flex items-center justify-center gap-2"
      >
        <Play :size="16" :stroke-width="2" />
        Start
      </button>
      <button 
        v-else
        @click.stop="$emit('stop', agent.id)"
        class="flex-1 btn-secondary text-sm py-2 px-4 flex items-center justify-center gap-2"
      >
        <Pause :size="16" :stroke-width="2" />
        Stop
      </button>

      <button 
        @click.stop="viewResults"
        class="flex-1 btn-primary text-sm py-2 px-4 flex items-center justify-center gap-2"
      >
        <Eye :size="16" :stroke-width="2" />
        View
      </button>

      <button 
        @click.stop="$emit('delete', agent.id)"
        class="btn-secondary text-sm py-2 px-4"
      >
        <Trash2 :size="16" :stroke-width="2" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Play, Pause, Eye, Trash2 } from 'lucide-vue-next'

const router = useRouter()

const props = defineProps({
  agent: {
    type: Object,
    required: true
  }
})

defineEmits(['start', 'stop', 'delete'])

const viewResults = () => {
  router.push(`/agent/${props.agent.id}/results`)
}

const progressPercent = computed(() => {
  if (props.agent.total_sites === 0) return 0
  return (props.agent.progress / props.agent.total_sites) * 100
})

const statusLEDClass = computed(() => {
  const baseClass = 'led-indicator '
  switch (props.agent.status) {
    case 'running': return baseClass + 'led-running'
    case 'completed': return baseClass + 'led-online'
    case 'failed': return baseClass + 'led-failed'
    default: return baseClass + 'led-idle'
  }
})
</script>
