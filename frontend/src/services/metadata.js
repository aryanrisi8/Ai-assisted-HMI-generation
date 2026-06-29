/**
 * Metadata Service
 * 
 * API calls for:
 * - List metadata
 * - Get metadata by ID
 * - Create metadata
 * - Update metadata
 * - Delete metadata
 */

import apiClient from './api'

class MetadataService {
  /**
   * List all metadata with pagination
   */
  async listMetadata(offset = 0, limit = 100) {
    const response = await apiClient.get('/metadata', {
      params: { offset, limit },
    })
    return response.data.data
  }

  /**
   * Get metadata by ID
   */
  async getMetadata(id) {
    const response = await apiClient.get(`/metadata/${id}`)
    return response.data.data
  }

  /**
   * Create new metadata
   */
  async createMetadata(data) {
    const response = await apiClient.post('/metadata', data)
    return response.data.data
  }

  /**
   * Update metadata
   */
  async updateMetadata(id, data) {
    const response = await apiClient.put(`/metadata/${id}`, data)
    return response.data.data
  }

  /**
   * Delete metadata
   */
  async deleteMetadata(id) {
    const response = await apiClient.delete(`/metadata/${id}`)
    return response.data.data
  }

  /**
   * Search metadata
   */
  async searchMetadata(query) {
    const response = await apiClient.get('/metadata/search', {
      params: { q: query },
    })
    return response.data
  }
}

export default new MetadataService()
