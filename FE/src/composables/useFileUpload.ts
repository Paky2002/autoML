import { ref, computed } from 'vue';
import type { DatasetDTO, FileUploadProgress } from '../types';

export function useFileUpload() {
  const isUploading = ref(false);
  const progress = ref<FileUploadProgress>({
    loaded: 0,
    total: 0,
    percentage: 0,
    stage: 'uploading'
  });
  const error = ref<string | null>(null);
  const dataset = ref<DatasetDTO | null>(null);

  const progressPercentage = computed(() => progress.value.percentage);
  const currentStage = computed(() => progress.value.stage);

  const uploadFile = async (file: File): Promise<void> => {
    if (!file) return;
    
    isUploading.value = true;
    error.value = null;
    dataset.value = null;
    
    try {
      // Validate file
      if (!file.name.toLowerCase().endsWith('.csv')) {
        throw new Error('Please upload a CSV file');
      }
      
      const maxSize = parseInt(import.meta.env.VITE_MAX_FILE_SIZE || '104857600');
      if (file.size > maxSize) {
        throw new Error('File size exceeds maximum limit (100MB)');
      }

      // Create worker
      const worker = new Worker(
        new URL('../workers/csvParser.workers', import.meta.url),
        { type: 'module' }
      );

      return new Promise((resolve, reject) => {
        worker.onmessage = (e) => {
          const { type, data } = e.data;

          switch (type) {
            case 'progress':
              progress.value = {
                ...progress.value,
                ...data,
                percentage: data.percentage
              };
              break;
              
            case 'success':
              dataset.value = data;
              isUploading.value = false;
              worker.terminate();
              resolve();
              break;
              
            case 'error':
              error.value = data;
              isUploading.value = false;
              worker.terminate();
              reject(new Error(data));
              break;
          }
        };

        worker.onerror = (err) => {
          error.value = 'Worker error occurred';
          isUploading.value = false;
          worker.terminate();
          reject(err);
        };

        // Start processing
        worker.postMessage({ file, filename: file.name });
      });
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Upload failed';
      isUploading.value = false;
      throw err;
    }
  };

  const reset = () => {
    isUploading.value = false;
    progress.value = {
      loaded: 0,
      total: 0,
      percentage: 0,
      stage: 'uploading'
    };
    error.value = null;
    dataset.value = null;
  };

  return {
    isUploading,
    progress,
    progressPercentage,
    currentStage,
    error,
    dataset,
    uploadFile,
    reset
  };
}