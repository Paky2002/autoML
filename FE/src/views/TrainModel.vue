<template>
  <div class="">
    <div class="flex justify-center">
      <Aura width="90vw" height="50vh" />
    </div>
    <!-- File Upload Section -->
    <div ref="uploadSection" class="pd-8">
      <FileUploader :is-uploading="isUploading" :progress-percentage="progressPercentage" :current-stage="currentStage"
        :error="uploadError" @file-selected="handleFileUpload" />
    </div>

    <!-- Dataset Preview and Training Form -->
    <div v-if="dataset" ref="datasetSection" class="space-y-8 animate-slide-up">
      <!-- Dataset Table - Ora usa preview invece di rows completi -->
      <DataTable :headers="dataset.headers" :preview-rows="getPreviewRows()" :total-rows="dataset.totalRows" />

      <!-- Training Form -->
      <TrainingForm :columns="dataset.columns" :is-training="isTrainingInProgress" @submit="handleTrainingSubmit" />

      <!-- Training Status -->
      <div v-if="trainingStatus" class="bg-blue-50 border border-blue-200 rounded-xl p-4">
        <div class="flex items-center gap-2">
          <div class="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-blue-700 font-medium">{{ trainingStatus }}</span>
        </div>
      </div>

      <!-- Training Error -->
      <div v-if="trainingError" class="bg-red-50 border border-red-200 rounded-xl p-4">
        <p class="text-red-700">{{ trainingError }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, computed } from 'vue';
import FileUploader from '../components/common/FileUploader.vue';
import DataTable from '../components/common/DataTable.vue';
import TrainingForm from '../components/forms/TrainingForm.vue';
import { useFileUpload } from '../composables/useFileUpload';
import { useApi } from '../composables/useApi';
import type { TrainingConfig, TrainingRequest } from '../types';
import Aura from '../components/common/Aura.vue';

// File upload composable
const {
  isUploading,
  progressPercentage,
  currentStage,
  error: uploadError,
  dataset,
  uploadFile,
  reset: resetUpload
} = useFileUpload();

// API composable
const {
  isLoading: isTrainingInProgress,
  error: trainingError,
  startTraining
} = useApi();

// Refs for smooth scrolling
const uploadSection = ref<HTMLElement>();
const datasetSection = ref<HTMLElement>();

// Training status
const trainingStatus = ref<string>('');

// Funzione per ottenere le righe di anteprima
const getPreviewRows = () => {
  if (!dataset.value) return [];

  // Usa il campo preview se disponibile, altrimenti prendi le prime 50 righe
  if (dataset.value.preview && dataset.value.preview.length > 0) {
    // Converte gli oggetti preview in array per la tabella
    return dataset.value.preview.map(obj =>
      dataset.value!.headers.map(header => obj[header])
    );
  }

  // Fallback: usa le prime 50 righe
  return dataset.value.rows.slice(0, 50);
};

const handleFileUpload = async (file: File) => {
  try {
    await uploadFile(file);

    // Debug: Log per verificare che tutti i dati siano stati caricati
    if (dataset.value) {
      console.log('Dataset caricato:', {
        filename: dataset.value.filename,
        totalRows: dataset.value.totalRows,
        actualDataRows: dataset.value.rows.length,
        previewRows: dataset.value.preview?.length || 0,
        headers: dataset.value.headers.length
      });
    }

    // Smooth scroll to dataset section
    await nextTick();
    if (datasetSection.value) {
      datasetSection.value.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  } catch (error) {
    console.error('File upload failed:', error);
  }
};

const handleTrainingSubmit = async (config: TrainingConfig) => {
  if (!dataset.value) return;

  try {
    trainingStatus.value = 'Preparing training data...';

    // Debug: Verifica che stiamo inviando tutti i dati
    console.log('Invio al training:', {
      datasetRows: dataset.value.rows.length,
      totalRows: dataset.value.totalRows,
      config
    });

    const request: TrainingRequest = {
      dataset: dataset.value, // Questo ora contiene TUTTI i dati in 'rows'
      config
    };

    const result = await startTraining(request);

    trainingStatus.value = 'Training started successfully!';
    console.log('Training result:', result);

    // You can redirect to ViewModel or show success message
    setTimeout(() => {
      trainingStatus.value = '';
    }, 3000);

  } catch (error) {
    trainingStatus.value = '';
    console.error('Training failed:', error);
  }
};
</script>