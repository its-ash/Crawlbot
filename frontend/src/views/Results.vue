<template>
  <div class="min-h-screen bg-background">
    <header class="border-b-2 border-border-dark py-6 mb-8">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button 
              @click="$router.push('/')"
              class="w-12 h-12 rounded-full bg-background flex items-center justify-center shadow-floating hover:shadow-pressed active:shadow-recessed transition-all"
            >
              <ArrowLeft class="w-6 h-6 text-accent" :stroke-width="2" />
            </button>
            <div>
              <h1 class="text-3xl font-extrabold tracking-tight drop-shadow-embossed">
                Extraction Results
              </h1>
              <p class="text-xs font-mono uppercase tracking-wider text-text-muted mt-1">
                {{ agent?.name || 'Loading...' }}
              </p>
            </div>
          </div>
          
          <div class="flex gap-3">
            <button @click="exportJSON" class="btn-secondary text-sm py-2 px-4 flex items-center gap-2">
              <Download :size="16" :stroke-width="2" />
              Export JSON
            </button>
            <button @click="exportCSV" class="btn-primary text-sm py-2 px-4 flex items-center gap-2">
              <FileText :size="16" :stroke-width="2" />
              Export CSV
            </button>
            <button 
              @click="handleLogout"
              class="btn-secondary text-sm py-2 px-4 flex items-center gap-2"
            >
              <LogOut :size="16" :stroke-width="2" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 pb-12">
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block w-16 h-16 border-4 border-muted border-t-accent rounded-full animate-spin"></div>
        <p class="text-text-muted font-mono mt-4 text-lg">Loading results...</p>
      </div>

      <div v-else-if="results.length === 0" class="card text-center py-20">
        <Database class="w-20 h-20 text-text-muted mx-auto mb-4" :stroke-width="1.5" />
        <h3 class="text-2xl font-bold mb-2">No Results Yet</h3>
        <p class="text-text-muted">This agent hasn't extracted any data yet. Start the agent to begin scraping.</p>
      </div>

      <div v-else>
        <div class="mb-6 flex items-center justify-between">
          <div>
            <p class="text-text-muted font-mono text-sm">
              Total Results: <span class="text-accent font-bold text-lg">{{ results.length }}</span>
            </p>
          </div>
          <div class="flex items-center gap-2">
            <div class="led-indicator led-online"></div>
            <span class="text-xs font-mono uppercase tracking-wide text-text-muted">
              {{ results.length }} {{ results.length === 1 ? 'RESULT' : 'RESULTS' }} FOUND
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-6">
          <div v-for="result in results" :key="result.id" class="card">
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <h3 class="text-xl font-bold mb-2 drop-shadow-embossed">
                  {{ result.title || 'Untitled' }}
                </h3>
                <a 
                  :href="result.url" 
                  target="_blank" 
                  class="text-accent hover:underline flex items-center gap-2 font-mono text-sm"
                >
                  <ExternalLink :size="16" :stroke-width="2" />
                  {{ result.url }}
                </a>
              </div>
            </div>

            <div v-if="result.meta_description" class="mb-4 p-3 bg-muted rounded-md shadow-recessed">
              <p class="text-sm text-text-muted italic">{{ result.meta_description }}</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-if="result.emails" class="bg-muted rounded-lg p-4 shadow-recessed">
                <div class="text-xs font-mono uppercase text-text-muted mb-2 flex items-center gap-2">
                  <Mail :size="16" :stroke-width="2" class="text-accent" />
                  Emails
                </div>
                <div class="font-mono text-sm break-all">
                  {{ result.emails }}
                </div>
              </div>

              <div v-if="result.phones" class="bg-muted rounded-lg p-4 shadow-recessed">
                <div class="text-xs font-mono uppercase text-text-muted mb-2 flex items-center gap-2">
                  <Phone :size="16" :stroke-width="2" class="text-accent" />
                  Phones
                </div>
                <div class="font-mono text-sm">
                  {{ result.phones }}
                </div>
              </div>

              <div v-if="result.addresses" class="bg-muted rounded-lg p-4 shadow-recessed">
                <div class="text-xs font-mono uppercase text-text-muted mb-2 flex items-center gap-2">
                  <MapPin :size="16" :stroke-width="2" class="text-accent" />
                  Addresses
                </div>
                <div class="font-mono text-sm">
                  {{ result.addresses }}
                </div>
              </div>

              <div v-if="result.company_names" class="bg-muted rounded-lg p-4 shadow-recessed">
                <div class="text-xs font-mono uppercase text-text-muted mb-2 flex items-center gap-2">
                  <Building :size="16" :stroke-width="2" class="text-accent" />
                  Companies
                </div>
                <div class="font-mono text-sm">
                  {{ result.company_names }}
                </div>
              </div>

              <div v-if="result.social_links && result.social_links !== '{}'" class="bg-muted rounded-lg p-4 shadow-recessed">
                <div class="text-xs font-mono uppercase text-text-muted mb-2 flex items-center gap-2">
                  <Share2 :size="16" :stroke-width="2" class="text-accent" />
                  Social Media
                </div>
                <div class="font-mono text-sm break-all">
                  {{ result.social_links }}
                </div>
              </div>

              <div v-if="result.contact_forms" class="bg-muted rounded-lg p-4 shadow-recessed">
                <div class="text-xs font-mono uppercase text-text-muted mb-2 flex items-center gap-2">
                  <MessageSquare :size="16" :stroke-width="2" class="text-accent" />
                  Contact Forms
                </div>
                <div class="font-mono text-sm break-all">
                  {{ result.contact_forms }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Download, FileText, Database, ExternalLink, Mail, Phone, MapPin, Building, Share2, MessageSquare, LogOut } from 'lucide-vue-next'
import { agentService } from '../services/api'
import { authService } from '../services/auth'

const route = useRoute()
const router = useRouter()
const agentId = parseInt(route.params.id)

const agent = ref(null)
const results = ref([])
const loading = ref(true)

const loadAgent = async () => {
  try {
    const response = await agentService.getAgent(agentId)
    agent.value = response.data
  } catch (error) {
    console.error('Failed to load agent:', error)
  }
}

const loadResults = async () => {
  try {
    const response = await agentService.getResults(agentId)
    results.value = response.data
  } catch (error) {
    console.error('Failed to load results:', error)
  } finally {
    loading.value = false
  }
}

const exportJSON = async () => {
  try {
    const response = await agentService.exportJSON(agentId)
    const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' })
    downloadFile(blob, `${agent.value?.name || 'results'}_results.json`)
  } catch (error) {
    console.error('Failed to export JSON:', error)
  }
}

const exportCSV = async () => {
  try {
    const response = await agentService.exportCSV(agentId)
    const blob = new Blob([response.data.csv], { type: 'text/csv' })
    downloadFile(blob, `${agent.value?.name || 'results'}_results.csv`)
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

const handleLogout = () => {
  authService.logout()
  router.push('/login')
}

onMounted(() => {
  loadAgent()
  loadResults()
})
</script>
