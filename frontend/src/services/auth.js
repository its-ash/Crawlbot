import axios from 'axios'

const TOKEN_KEY = 'crawlbot_token'

export const authService = {
  async login(token) {
    try {
      const response = await axios.post('/api/auth/login', { token })
      if (response.data.success) {
        localStorage.setItem(TOKEN_KEY, token)
        return true
      }
      return false
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  },

  logout() {
    localStorage.removeItem(TOKEN_KEY)
  },

  isAuthenticated() {
    return !!localStorage.getItem(TOKEN_KEY)
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  }
}
