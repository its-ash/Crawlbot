<template>
  <div class="min-h-screen bg-background">
    <header class="border-b-2 border-border-dark py-6 mb-12">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-full bg-background flex items-center justify-center shadow-floating">
              <Search class="w-6 h-6 text-accent" :stroke-width="2" />
            </div>
            <div>
              <h1 class="text-3xl font-extrabold tracking-tight drop-shadow-embossed">
                CRAWLBOT
              </h1>
              <p class="text-xs font-mono uppercase tracking-wider text-text-muted mt-1">
                Marketing Data Extraction System
              </p>
            </div>
          </div>
          
          <div class="flex items-center gap-3">
            <div class="led-indicator led-online"></div>
            <span class="text-xs font-mono uppercase tracking-wide text-text-muted">
              SYSTEM OPERATIONAL
            </span>
            <button 
              @click="handleLogout"
              class="ml-4 btn-secondary text-sm py-2 px-4 flex items-center gap-2"
            >
              <LogOut :size="16" :stroke-width="2" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 pb-12">
      <div class="mb-8">
        <button 
          @click="showCreateModal = true"
          class="btn-primary inline-flex items-center gap-2"
        >
          <Plus :size="20" :stroke-width="2" />
          Create New Agent
        </button>
      </div>

      <div v-if="agents.length === 0" class="card text-center py-16">
        <Bot class="w-16 h-16 text-text-muted mx-auto mb-4" :stroke-width="1.5" />
        <h3 class="text-xl font-bold mb-2">No Agents Yet</h3>
        <p class="text-text-muted">Create your first agent to start extracting marketing data</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AgentCard 
          v-for="agent in agents" 
          :key="agent.id"
          :agent="agent"
          @start="startAgent"
          @stop="stopAgent"
          @delete="deleteAgent"
        />
      </div>
    </main>

    <CreateAgentModal 
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="onAgentCreated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Plus, Bot, LogOut } from 'lucide-vue-next'
import { agentService, WebSocketService } from '../services/api'
import { authService } from '../services/auth'
import AgentCard from '../components/AgentCard.vue'
import CreateAgentModal from '../components/CreateAgentModal.vue'

const router = useRouter()
const agents = ref([])
const showCreateModal = ref(false)
const wsService = new WebSocketService()

const loadAgents = async () => {
  try {
    const response = await agentService.getAgents()
    agents.value = response.data
  } catch (error) {
    console.error('Failed to load agents:', error)
  }
}

const onAgentCreated = () => {
  showCreateModal.value = false
  loadAgents()
}

const startAgent = async (agentId) => {
  try {
    await agentService.startAgent(agentId)
    loadAgents()
  } catch (error) {
    console.error('Failed to start agent:', error)
  }
}

const stopAgent = async (agentId) => {
  try {
    await agentService.stopAgent(agentId)
    loadAgents()
  } catch (error) {
    console.error('Failed to stop agent:', error)
  }
}

const deleteAgent = async (agentId) => {
  if (!confirm('Are you sure you want to delete this agent?')) return
  
  try {
    await agentService.deleteAgent(agentId)
    loadAgents()
  } catch (error) {
    console.error('Failed to delete agent:', error)
  }
}

const handleLogout = () => {
  authService.logout()
  wsService.disconnect()
  router.push('/login')
}

const handleWebSocketMessage = (data) => {
  if (data.type === 'progress_update') {
    const agent = agents.value.find(a => a.id === data.agent_id)
    if (agent) {
      agent.progress = data.progress
      agent.total_sites = data.total
      if (data.results_count !== undefined) {
        agent.results_count = data.results_count
      }
    }
  } else if (data.type === 'agent_update') {
    loadAgents()
  }
}

onMounted(() => {
  loadAgents()
  wsService.connect()
  wsService.addListener(handleWebSocketMessage)
})

onUnmounted(() => {
  wsService.removeListener(handleWebSocketMessage)
  wsService.disconnect()
})
</script>
