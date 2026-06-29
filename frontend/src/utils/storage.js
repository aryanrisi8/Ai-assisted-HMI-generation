/**
 * Local storage utilities
 */

const PREFIX = 'hmi_'

export const storage = {
  set: (key, value) => {
    try {
      localStorage.setItem(PREFIX + key, JSON.stringify(value))
    } catch (err) {
      console.error('Storage set failed:', err)
    }
  },

  get: (key) => {
    try {
      const item = localStorage.getItem(PREFIX + key)
      return item ? JSON.parse(item) : null
    } catch (err) {
      console.error('Storage get failed:', err)
      return null
    }
  },

  remove: (key) => {
    try {
      localStorage.removeItem(PREFIX + key)
    } catch (err) {
      console.error('Storage remove failed:', err)
    }
  },

  clear: () => {
    try {
      const keys = Object.keys(localStorage)
      keys.forEach((key) => {
        if (key.startsWith(PREFIX)) {
          localStorage.removeItem(key)
        }
      })
    } catch (err) {
      console.error('Storage clear failed:', err)
    }
  },
}
