import { ref } from 'vue';
import type { TrainingRequest } from '../types';

export function useApi() {
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

  const startTraining = async (request: TrainingRequest) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiUrl}/api/train`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Training request failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    isLoading,
    error,
    startTraining
  };
}