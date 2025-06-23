<template>
  <div class="min-h-screen">
    <Aura width="100vw" height="30vh" />
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-20 relative z-10">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-20">
        <div class="flex items-center gap-3 text-white">
          <div class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          <span>Loading models...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="py-20">
        <div class="bg-red-900/20 backdrop-blur-sm border border-red-700/30 rounded-2xl p-8 text-center">
          <div class="w-16 h-16 bg-red-500/20 rounded-full mx-auto mb-4 flex items-center justify-center">
            <AlertCircle class="w-8 h-8 text-red-400" />
          </div>
          <h3 class="text-xl font-semibold text-red-200 mb-2">Error Loading Models</h3>
          <p class="text-red-300 mb-6">{{ error }}</p>
          <button
            @click="fetchModels"
            class="px-6 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-xl text-red-200 font-medium transition-all duration-200"
          >
            Try Again
          </button>
        </div>
      </div>

      <!-- Models Table -->
      <div v-else>
        <ModelsTable
          :models="models"
          @view-model="handleViewModel"
          @delete-model="handleDeleteModel"
          @refresh="fetchModels"
        />
      </div>

      <!-- Delete Confirmation Modal -->
      <div
        v-if="modelToDelete"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
        @click="cancelDelete"
      >
        <div
          class="bg-black/80 backdrop-blur-md border border-white/20 rounded-2xl p-8 max-w-md w-full mx-4"
          @click.stop
        >
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center">
              <Trash2 class="w-6 h-6 text-red-400" />
            </div>
            <div>
              <h3 class="text-xl font-semibold text-white">Delete Model</h3>
              <p class="text-white/70">This action cannot be undone</p>
            </div>
          </div>
          
          <p class="text-white/80 mb-6">
            Are you sure you want to delete the model "<span class="font-medium text-white">{{ modelToDelete.name }}</span>"?
          </p>
          
          <div class="flex gap-3">
            <button
              @click="cancelDelete"
              class="flex-1 px-4 py-3 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white font-medium transition-all duration-200"
            >
              Cancel
            </button>
            <button
              @click="confirmDelete"
              :disabled="isDeleting"
              class="flex-1 px-4 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-xl text-red-200 font-medium transition-all duration-200 disabled:opacity-50"
            >
              <span v-if="isDeleting" class="flex items-center justify-center gap-2">
                <div class="w-4 h-4 border-2 border-red-300/30 border-t-red-300 rounded-full animate-spin"></div>
                Deleting...
              </span>
              <span v-else>Delete</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { AlertCircle, Trash2 } from 'lucide-vue-next';
import Aura from '../components/common/Aura.vue';
import ModelsTable from '../components/common/ModelsTable.vue';
import { useApi } from '../composables/useApi';
import type { TrainedModel } from '../types';

const router = useRouter();

// Usa il composable API invece di chiamate dirette
const { getAllModels, deleteModel, isLoading, error } = useApi();

const models = ref<TrainedModel[]>([]);
const modelToDelete = ref<TrainedModel | null>(null);
const isDeleting = ref(false);

// Cache per evitare chiamate multiple
let modelsCache: TrainedModel[] | null = null;
let lastFetchTime = 0;
const CACHE_DURATION = 30000; // 30 secondi

const fetchModels = async (forceRefresh = false) => {
  try {
    // Usa cache se disponibile e recente
    const now = Date.now();
    if (!forceRefresh && modelsCache && (now - lastFetchTime) < CACHE_DURATION) {
      models.value = modelsCache;
      return;
    }

    const fetchedModels = await getAllModels();
    models.value = fetchedModels;
    
    // Aggiorna cache
    modelsCache = fetchedModels;
    lastFetchTime = now;
  } catch (err) {
    console.error('Failed to fetch models:', err);
    // Error già gestito dal composable
  }
};

const handleViewModel = (uuid: string) => {
  router.push(`/models/${uuid}`);
};

const handleDeleteModel = (uuid: string) => {
  const model = models.value.find(m => m.uuid === uuid);
  if (model) {
    modelToDelete.value = model;
  }
};

const cancelDelete = () => {
  modelToDelete.value = null;
};

const confirmDelete = async () => {
  if (!modelToDelete.value) return;
  
  try {
    isDeleting.value = true;
    
    const success = await deleteModel(modelToDelete.value.uuid);
    
    if (success) {
      // Remove from local state immediately
      models.value = models.value.filter(m => m.uuid !== modelToDelete.value!.uuid);
      // Invalida cache
      modelsCache = models.value;
      lastFetchTime = Date.now();
    }
    
    modelToDelete.value = null;
  } catch (err) {
    console.error('Failed to delete model:', err);
  } finally {
    isDeleting.value = false;
  }
};

onMounted(() => {
  fetchModels();
});
</script>