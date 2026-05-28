<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-6 z-50" @click.self="$emit('close')">
    <div class="card max-w-lg w-full">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold drop-shadow-embossed">Create New Agent</h2>
        <button @click="$emit('close')" class="text-text-muted hover:text-accent">
          <X :size="24" :stroke-width="2" />
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-text-muted mb-2">
            Agent Name
          </label>
          <input 
            v-model="formData.name"
            type="text"
            required
            placeholder="e.g., Real Estate Leads California"
            class="input-field"
          />
        </div>

        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-text-muted mb-2">
            Search Keywords
          </label>
          <input 
            v-model="formData.keywords"
            type="text"
            required
            placeholder="e.g., real estate agents Los Angeles contact"
            class="input-field"
          />
        </div>

        <div>
          <label class="block text-xs font-mono uppercase tracking-wider text-text-muted mb-3">
            Search Engine
          </label>
          <div class="grid grid-cols-2 gap-3">
            <label 
              class="card cursor-pointer transition-all"
              :class="{ 'ring-2 ring-accent': formData.search_engine === 'duckduckgo' }"
            >
              <input 
                type="radio" 
                v-model="formData.search_engine" 
                value="duckduckgo"
                class="sr-only"
              />
              <div class="flex items-center gap-3 p-2">
                <Search :size="20" class="text-accent" :stroke-width="2" />
                <div>
                  <div class="font-bold text-sm">DuckDuckGo</div>
                  <div class="text-xs text-text-muted font-mono">No API Key</div>
                </div>
              </div>
            </label>

            <label 
              class="card cursor-pointer transition-all"
              :class="{ 'ring-2 ring-accent': formData.search_engine === 'google' }"
            >
              <input 
                type="radio" 
                v-model="formData.search_engine" 
                value="google"
                class="sr-only"
              />
              <div class="flex items-center gap-3 p-2">
                <Globe :size="20" class="text-accent" :stroke-width="2" />
                <div>
                  <div class="font-bold text-sm">Google</div>
                  <div class="text-xs text-text-muted font-mono">API Required</div>
                </div>
              </div>
            </label>
          </div>
        </div>

        <div class="flex gap-3 pt-4">
          <button type="button" @click="$emit('close')" class="flex-1 btn-secondary">
            Cancel
          </button>
          <button type="submit" class="flex-1 btn-primary flex items-center justify-center gap-2">
            <Plus :size="20" :stroke-width="2" />
            Create Agent
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { X, Plus, Search, Globe } from 'lucide-vue-next'
import { agentService } from '../services/api'

const emit = defineEmits(['close', 'created'])

const formData = ref({
  name: '',
  keywords: '',
  search_engine: 'duckduckgo'
})

const handleSubmit = async () => {
  try {
    await agentService.createAgent(formData.value)
    emit('created')
  } catch (error) {
    console.error('Failed to create agent:', error)
    alert('Failed to create agent. Please try again.')
  }
}
</script>
