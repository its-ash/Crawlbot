<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-6 z-50 overflow-y-auto" @click.self="$emit('close')">
    <div class="card max-w-6xl w-full my-8">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-bold drop-shadow-embossed">{{ agent.name }}</h2>
          <p class="text-xs font-mono uppercase tracking-wider text-text-muted mt-1">
            Extraction Results
          </p>
        </div>
        <button @click="$emit('close')" class="text-text-muted hover:text-accent">
          <X :size="24" :stroke-width="2" />
        </button>
      </div>

      <div class="flex gap-3 mb-6">
        <button @click="exportJSON" class="btn-secondary text-sm py-2 px-4 flex items-center gap-2">
          <Download :size="16" :stroke-width="2" />
          Export JSON
        </button>
        <button @click="exportCSV" class="btn-secondary text-sm py-2 px-4 flex items-center gap-2">
          <FileText :size="16" :stroke-width="2" />
          Export CSV
        </button>
      </div>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block w-12 h-12 border-4 border-muted border-t-accent rounded-full animate-spin"></div>
        <p class="text-text-muted font-mono mt-4">Loading results...</p>
      </div>

      <div v-else-if="results.length === 0" class="text-center py-12">
        <Database class="w-16 h-16 text-text-muted mx-auto mb-4" :stroke-width="1.5" />
        <p class="text-text-muted">No results yet</p>
      </div>

      <div v-else class="space-y-4 max-h-96 overflow-y-auto pr-2">
        <div v-for="result in results" :key="result.id" class="bg-muted rounded-lg p-4 shadow-recessed">
          <div class="flex items-start justify-between mb-3">
            <a :href="result.url" target="_blank" class="font-bold text-accent hover:underline flex items-center gap-2">
              <ExternalLink :size="16" :stroke-width="2" />
              {{ result.title || result.url }}
            </a>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div v-if="result.emails">
              <div class="text-xs font-mono uppercase text-text-muted mb-1 flex items-center gap-2">
                <Mail :size="14" :stroke-width="2" />
                Emails
              </div>
              <div class="font-mono text-xs">
                {{ result.emails }}
              </div>
            </div>

            <div v-if="result.phones">
              <div class="text-xs font-mono uppercase text-text-muted mb-1 flex items-center gap-2">
                <Phone :size="14" :stroke-width="2" />
                Phones
              </div>
              <div class="font-mono text-xs">
                {{ result.phones }}
              </div>
            </div>

            <div v-if="result.addresses">
              <div class="text-xs font-mono uppercase text-text-muted mb-1 flex items-center gap-2">
                <MapPin :size="14" :stroke-width="2" />
                Addresses
              </div>
              <div class="font-mono text-xs">
                {{ result.addresses }}
              </div>
            </div>

            <div v-if="result.company_names">
              <div class="text-xs font-mono uppercase text-text-muted mb-1 flex items-center gap-2">
                <Building :size="14" :stroke-width="2" />
                Companies
              </div>
              <div class="font-mono text-xs">
                {{ result.company_names }}
              </div>
            </div>

            <div v-if="result.social_links && result.social_links !== '{}'">
              <div class="text-xs font-mono uppercase text-text-muted mb-1 flex items-center gap-2">
                <Share2 :size="14" :stroke-width="2" />
                Social Media
              </div>
              <div class="font-mono text-xs">
                {{ result.social_links }}
              </div>
            </div>

            <div v-if="result.contact_forms">
              <div class="text-xs font-mono uppercase text-text-muted mb-1 flex items-center gap-2">
                <MessageSquare :size="14" :stroke-width="2" />
                Contact Forms
              </div>
              <div class="font-mono text-xs">
                {{ result.contact_forms }}
              </div>
            </div>
          </div>

          <div v-if="result.meta_description" class="mt-3 pt-3 border-t border-border-dark">
            <div class="text-xs text-text-muted italic">
              {{ result.meta_description }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { X, Download, FileText, Database, ExternalLink, Mail, Phone, MapPin, Building, Share2, MessageSquare } from 'lucide-vue-next'
import { agentService } from '../services/api'

const props = defineProps({
  agent: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const results = ref([])
const loading = ref(true)

const loadResults = async () => {
  try {
    const response = await agentService.getResults(props.agent.id)
    results.value = response.data
  } catch (error) {
    console.error('Failed to load results:', error)
  } finally {
    loading.value = false
  }
}

const exportJSON = async () => {
  try {
    const response = await agentService.exportJSON(props.agent.id)
    const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
    downloadFile(blob, `${props.agent.name}_results.json`)
  } catch (error) {
    console.error('Failed to export JSON:', error)
  }
}

const exportCSV = async () => {
  try {
    const response = await agentService.exportCSV(props.agent.id)
    const blob = new Blob([response.data.csv], { type: 'text/csv' })
    downloadFile(blob, `${props.agent.name}_results.csv`)
  } catch (error) {
    console.error('Failed to export CSV:', error)
  }
}

const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  window.URL.revokeObjectURL(url)
}

onMounted(() => {
  loadResults()
})
</script>
