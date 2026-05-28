<template>
  <div class="min-h-screen bg-background flex items-center justify-center p-6">
    <div class="card max-w-md w-full">
      <div class="text-center mb-8">
        <div class="w-20 h-20 mx-auto rounded-full bg-background flex items-center justify-center shadow-floating mb-4">
          <Lock class="w-10 h-10 text-accent" :stroke-width="2" />
        </div>
        <h1 class="text-4xl font-extrabold tracking-tight drop-shadow-embossed mb-2">
          CRAWLBOT
        </h1>
        <p class="text-xs font-mono uppercase tracking-wider text-text-muted">
          Authentication Required
        </p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-xs font-mono uppercase tracking-wide text-text-muted mb-2">
            Access Token
          </label>
          <input
            v-model="token"
            type="password"
            placeholder="Enter your access token"
            class="w-full bg-muted rounded-lg px-4 py-3 shadow-recessed focus:outline-none focus:ring-2 focus:ring-accent font-mono text-sm"
            required
            :disabled="loading"
          />
        </div>

        <div v-if="error" class="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-3">
          <p class="text-red-400 text-sm font-mono flex items-center gap-2">
            <AlertCircle :size="16" :stroke-width="2" />
            {{ error }}
          </p>
        </div>

        <button
          type="submit"
          class="w-full btn-primary py-3 flex items-center justify-center gap-2"
          :disabled="loading"
        >
          <template v-if="loading">
            <div class="w-5 h-5 border-2 border-background border-t-accent rounded-full animate-spin"></div>
            Authenticating...
          </template>
          <template v-else>
            <LogIn :size="20" :stroke-width="2" />
            Login
          </template>
        </button>
      </form>

      <div class="mt-8 pt-6 border-t border-border-dark">
        <div class="flex items-center gap-2 text-xs text-text-muted">
          <div class="led-indicator led-online"></div>
          <span class="font-mono uppercase tracking-wide">System Operational</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Lock, LogIn, AlertCircle } from 'lucide-vue-next'
import { authService } from '../services/auth'

const router = useRouter()
const token = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    const success = await authService.login(token.value)
    if (success) {
      router.push('/')
    } else {
      error.value = 'Invalid access token'
    }
  } catch (err) {
    error.value = 'Authentication failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
