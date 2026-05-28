import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const agentService = {
  getAgents: () => api.get('/agents'),
  getAgent: (id) => api.get(`/agents/${id}`),
  createAgent: (data) => api.post('/agents', data),
  deleteAgent: (id) => api.delete(`/agents/${id}`),
  startAgent: (id) => api.post(`/agents/${id}/start`),
  stopAgent: (id) => api.post(`/agents/${id}/stop`),
  getResults: (id) => api.get(`/agents/${id}/results`),
  exportJSON: (id) => api.get(`/agents/${id}/export/json`),
  exportCSV: (id) => api.get(`/agents/${id}/export/csv`)
}

export class WebSocketService {
  constructor() {
    this.ws = null
    this.listeners = []
  }
  
  connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws`
    
    this.ws = new WebSocket(wsUrl)
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      this.listeners.forEach(listener => listener(data))
    }
    
    this.ws.onclose = () => {
      setTimeout(() => this.connect(), 3000)
    }
  }
  
  addListener(callback) {
    this.listeners.push(callback)
  }
  
  removeListener(callback) {
    this.listeners = this.listeners.filter(l => l !== callback)
  }
  
  disconnect() {
    if (this.ws) {
      this.ws.close()
    }
  }
}

export default api
