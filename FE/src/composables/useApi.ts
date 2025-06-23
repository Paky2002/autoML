// FE/src/composables/useApi.ts
import { ref } from 'vue';
import type { TrainingRequest, TrainedModel } from '../types';

export function useApi() {
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

  const startTraining = async (request: TrainingRequest) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiUrl}/api/training/train`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (!result.success) {
        throw new Error(result.error || 'Training failed');
      }

      return result.data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Training request failed';
      error.value = errorMessage;
      throw new Error(errorMessage);
    } finally {
      isLoading.value = false;
    }
  };

  const getTrainingStatus = async (modelUuid: string) => {
    try {
      const response = await fetch(`${apiUrl}/api/training/status/${modelUuid}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to get training status';
      throw err;
    }
  };

  const getAllModels = async (): Promise<TrainedModel[]> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiUrl}/api/models`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (!result.success) {
        throw new Error(result.error || 'Failed to fetch models');
      }

      return result.models || [];
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch models';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const getModelByUuid = async (modelUuid: string): Promise<TrainedModel | null> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiUrl}/api/models/${modelUuid}`);
      
      if (response.status === 404) {
        return null;
      }
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (!result.success) {
        throw new Error(result.error || 'Failed to fetch model');
      }

      return result.model;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch model';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const deleteModel = async (modelUuid: string): Promise<boolean> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${apiUrl}/api/models/${modelUuid}`, {
        method: 'DELETE',
      });
      
      if (response.status === 404) {
        return false;
      }
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result.success;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete model';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const predict = async (modelUuid: string, data: Record<string, any>[]): Promise<any> => {
    try {
      const response = await fetch(`${apiUrl}/api/predictions/${modelUuid}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Prediction failed';
      throw new Error(errorMessage);
    }
  };

  return {
    isLoading,
    error,
    startTraining,
    getTrainingStatus,
    getAllModels,
    getModelByUuid,
    deleteModel,
    predict
  };
}