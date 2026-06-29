/**
 * useFetch Hook
 * 
 * Generic data fetching with loading, error, and retry
 */

import { useState, useEffect, useCallback } from 'react'

export function useFetch(fetchFn, dependencies = []) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetch = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchFn()
      setData(result)
    } catch (err) {
      setError(err)
    } finally {
      setLoading(false)
    }
  }, [fetchFn])

  useEffect(() => {
    fetch()
  }, dependencies)

  const retry = useCallback(() => fetch(), [fetch])

  return { data, loading, error, retry }
}
