/**
 * Dashboard Service
 * 
 * API calls for:
 * - Generate dashboard
 * - Get dashboard templates
 * - Get dashboard recommendations
 */

import apiClient from './api'

class DashboardService {
  /**
   * Generate dashboard from metadata
   */
  async generateDashboard(metadataId) {
    const response = await apiClient.post(`/dashboards/generate/${metadataId}`)
    return response.data.data
  }

  /**
   * Get dashboard templates
   */
  async getTemplates() {
    const response = await apiClient.get('/dashboards/templates')
    return response.data.data
  }

  /**
   * Get dashboard recommendations for metadata
   */
  async getRecommendations(metadataId) {
    const response = await apiClient.get(`/dashboards/recommendations/${metadataId}`)
    return response.data.data
  }

  /**
   * Save dashboard layout
   */
  async saveDashboard(payload) {
    const response = await apiClient.post('/dashboards', payload)
    return response.data.data
  }

  /**
   * Get saved dashboard
   */
  async getDashboard(id) {
    const response = await apiClient.get(`/dashboards/${id}`)
    return response.data.data
  }

  /**
   * List saved dashboards
   */
  async listDashboards(offset = 0, limit = 50) {
    const response = await apiClient.get('/dashboards', {
      params: { offset, limit },
    })
    return response.data.data
  }

  /**
   * Delete dashboard
   */
  async deleteDashboard(id) {
    const response = await apiClient.delete(`/dashboards/${id}`)
    return response.data.data
  }

  /**
   * Update dashboard
   */
  async updateDashboard(id, updates) {
    const response = await apiClient.put(`/dashboards/${id}`, updates)
    return response.data.data
  }
}

export default new DashboardService()
