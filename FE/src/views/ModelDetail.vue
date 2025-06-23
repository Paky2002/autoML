<template>
  <div class="min-h-screen">
    <Aura width="100vw" height="25vh" />
    
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 -mt-16 relative z-10">
      <!-- Back Button -->
      <div class="mb-6">
        <button
          @click="$router.push('/models')"
          class="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white/90 hover:text-white transition-all duration-200 backdrop-blur-sm group"
        >
          <ArrowLeft class="w-4 h-4 group-hover:-translate-x-1 transition-transform duration-200" />
          Back to Models
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-20">
        <div class="flex items-center gap-3 text-white">
          <div class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
          <span>Loading model details...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="py-20">
        <div class="bg-red-900/20 backdrop-blur-sm border border-red-700/30 rounded-2xl p-8 text-center">
          <div class="w-16 h-16 bg-red-500/20 rounded-full mx-auto mb-4 flex items-center justify-center">
            <AlertCircle class="w-8 h-8 text-red-400" />
          </div>
          <h3 class="text-xl font-semibold text-red-200 mb-2">Model Not Found</h3>
          <p class="text-red-300 mb-6">{{ error }}</p>
          <button
            @click="$router.push('/models')"
            class="px-6 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-xl text-red-200 font-medium transition-all duration-200"
          >
            Back to Models
          </button>
        </div>
      </div>

      <!-- Model Details -->
      <div v-else-if="model" class="space-y-8">
        <!-- Header with Status -->
        <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
          <div class="flex items-start justify-between mb-6">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <Brain class="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 class="text-3xl font-bold text-white mb-2">{{ model.name }}</h1>
                <div class="flex items-center gap-3 mb-2">
                  <!-- Status Badge -->
                  <StatusBadge 
                    :status="model.status" 
                    size="md"
                    :show-progress="true"
                  />
                  <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-white/10 text-white/90 capitalize">
                    {{ model.problem_type }}
                  </span>
                </div>
                <p class="text-white/50 font-mono text-sm">UUID: {{ model.uuid }}</p>
              </div>
            </div>
            
            <div class="text-right">
              <p class="text-white/70 text-sm">Created</p>
              <p class="text-white font-mono">{{ formatDate(model.created_at) }}</p>
              <p class="text-white/50 text-xs mt-1">{{ getTimeAgo(model.created_at) }}</p>
            </div>
          </div>

          <!-- Status-specific Information -->
          <div v-if="model.status === 'training'" class="bg-blue-500/10 rounded-xl p-4 border border-blue-500/30 mb-4">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-6 h-6 border-2 border-blue-400/50 border-t-blue-400 rounded-full animate-spin"></div>
              <h3 class="text-blue-200 font-medium">Training in Progress</h3>
            </div>
            <p class="text-blue-300/80 text-sm">
              This model is currently being trained. The process may take several minutes depending on dataset size and complexity.
            </p>
          </div>

          <div v-else-if="model.status === 'completed'" class="bg-green-500/10 rounded-xl p-4 border border-green-500/30 mb-4">
            <div class="flex items-center gap-3 mb-2">
              <CheckCircle class="w-6 h-6 text-green-400" />
              <h3 class="text-green-200 font-medium">Training Completed Successfully</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
              <div v-if="model.best_score">
                <span class="text-green-300/70 text-sm">Best Score:</span>
                <p class="text-green-200 font-mono text-lg">{{ formatScore(model.best_score) }}</p>
              </div>
              <div v-if="model.best_model_name">
                <span class="text-green-300/70 text-sm">Best Model:</span>
                <p class="text-green-200 font-mono">{{ model.best_model_name }}</p>
              </div>
            </div>
            <div class="mt-4">
              <p class="text-green-300/80 text-sm">
                🎉 Your model is ready! Scroll down to test it with live data or get the API integration code.
              </p>
            </div>
          </div>

          <div v-else-if="model.status === 'failed'" class="bg-red-500/10 rounded-xl p-4 border border-red-500/30 mb-4">
            <div class="flex items-center gap-3 mb-2">
              <XCircle class="w-6 h-6 text-red-400" />
              <h3 class="text-red-200 font-medium">Training Failed</h3>
            </div>
            <p class="text-red-300/80 text-sm mb-3">
              {{ model.error_message || 'The training process encountered an error and could not be completed.' }}
            </p>
            <div class="flex gap-3">
              <button
                @click="retryTraining"
                class="flex items-center gap-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-xl text-red-200 font-medium transition-all duration-200"
              >
                <RotateCcw class="w-4 h-4" />
                Retry Training
              </button>
              <router-link
                to="/train"
                class="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white/90 font-medium transition-all duration-200"
              >
                <Plus class="w-4 h-4" />
                Train New Model
              </router-link>
            </div>
          </div>

          <div v-else-if="model.status === 'deleted'" class="bg-gray-500/10 rounded-xl p-4 border border-gray-500/30 mb-4">
            <div class="flex items-center gap-3 mb-2">
              <Trash2 class="w-6 h-6 text-gray-400" />
              <h3 class="text-gray-200 font-medium">Model Deleted</h3>
            </div>
            <p class="text-gray-300/80 text-sm">
              This model has been marked as deleted and is no longer available for predictions.
            </p>
          </div>
        </div>

        <!-- Training Configuration -->
        <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
          <h2 class="text-2xl font-semibold text-white mb-6 flex items-center gap-3">
            <Settings class="w-6 h-6" />
            Training Configuration
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 class="text-white/70 text-sm font-medium mb-2">Target Feature</h3>
              <p class="text-white font-mono text-lg">{{ model.target_feature }}</p>
            </div>
            
            <div class="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 class="text-white/70 text-sm font-medium mb-2">Problem Type</h3>
              <p class="text-white capitalize text-lg">{{ model.problem_type }}</p>
            </div>
            
            <div class="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 class="text-white/70 text-sm font-medium mb-2">Time Limit</h3>
              <p class="text-white text-lg">{{ model.time_limit }}s</p>
            </div>
            
            <div class="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 class="text-white/70 text-sm font-medium mb-2">Quality Preset</h3>
              <p class="text-white capitalize text-lg">{{ model.presets || 'Default' }}</p>
            </div>
            
            <div class="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 class="text-white/70 text-sm font-medium mb-2">Evaluation Metric</h3>
              <p class="text-white text-lg">{{ model.eval_metric || 'Auto-selected' }}</p>
            </div>
            
            <div class="bg-white/5 rounded-xl p-4 border border-white/10">
              <h3 class="text-white/70 text-sm font-medium mb-2">Verbosity Level</h3>
              <p class="text-white text-lg">{{ getVerbosityLabel(model.verbosity) }}</p>
            </div>
          </div>
        </div>

        <!-- Dataset Information -->
        <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
          <h2 class="text-2xl font-semibold text-white mb-6 flex items-center gap-3">
            <Database class="w-6 h-6" />
            Dataset Information
          </h2>
          
          <div class="bg-white/5 rounded-xl p-6 border border-white/10">
            <div class="flex items-center gap-3 mb-4">
              <FileText class="w-5 h-5 text-white/70" />
              <h3 class="text-white font-medium">{{ model.dataset_filename || 'Unknown Dataset' }}</h3>
            </div>
            <p class="text-white/70">
              This model was trained using the uploaded dataset with the target feature 
              <span class="font-mono text-white">{{ model.target_feature }}</span> 
              for {{ model.problem_type }} prediction.
            </p>
          </div>
        </div>

        <!-- Model Technical Information -->
        <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
          <h2 class="text-2xl font-semibold text-white mb-6 flex items-center gap-3">
            <Info class="w-6 h-6" />
            Technical Information
          </h2>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center py-3 border-b border-white/10">
              <span class="text-white/70">Model UUID</span>
              <span class="font-mono text-white bg-white/5 px-3 py-1 rounded-lg">{{ model.uuid }}</span>
            </div>
            
            <div class="flex justify-between items-center py-3 border-b border-white/10">
              <span class="text-white/70">Status</span>
              <StatusBadge 
                :status="model.status" 
                size="sm"
                :show-progress="false"
              />
            </div>
            
            <div class="flex justify-between items-center py-3 border-b border-white/10">
              <span class="text-white/70">Model Path</span>
              <span class="font-mono text-white/80 text-sm">{{ model.model_path || 'N/A' }}</span>
            </div>
            
            <div class="flex justify-between items-center py-3 border-b border-white/10">
              <span class="text-white/70">Created</span>
              <span class="text-white">{{ formatDateLong(model.created_at) }}</span>
            </div>

            <div v-if="model.updated_at" class="flex justify-between items-center py-3">
              <span class="text-white/70">Last Updated</span>
              <span class="text-white">{{ formatDateLong(model.updated_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Live Prediction Testing - Only for completed models -->
        <div v-if="model.status === 'completed'">
          <PredictionTest
            :model-uuid="model.uuid"
            :target-feature="model.target_feature"
            :required-features="getRequiredFeatures()"
          />
        </div>

        <!-- API Integration Code - Only for completed models -->
        <div v-if="model.status === 'completed'">
          <ApiCodeGenerator
            :model-uuid="model.uuid"
            :target-feature="model.target_feature"
            :required-features="getRequiredFeatures()"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  ArrowLeft, Brain, Settings, Database, FileText, Info, AlertCircle,
  CheckCircle, XCircle, Clock, RotateCcw, Plus, Zap, Trash2
} from 'lucide-vue-next';
import Aura from '../components/common/Aura.vue';
import StatusBadge from '../components/common/StatusBadge.vue';
import PredictionTest from '../components/prediction/PredictionTest.vue';
import ApiCodeGenerator from '../components/prediction/ApiCodeGenerator.vue';
import { useApi } from '../composables/useApi';
import type { TrainedModel } from '../types';

const route = useRoute();
const router = useRouter();

const { isLoading, error, getModelByUuid } = useApi();

const model = ref<TrainedModel | null>(null);

const fetchModel = async () => {
  try {
    const modelUuid = route.params.uuid as string;
    const fetchedModel = await getModelByUuid(modelUuid);
    model.value = fetchedModel;
  } catch (err) {
    console.error('Failed to fetch model:', err);
  }
};

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatDateLong = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getTimeAgo = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) return 'Just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
  return `${Math.floor(diffInSeconds / 86400)} days ago`;
};

const getVerbosityLabel = (level: number): string => {
  const labels = {
    0: 'Silent',
    1: 'Minimal',
    2: 'Standard',
    3: 'Verbose'
  };
  return labels[level as keyof typeof labels] || 'Unknown';
};

const formatScore = (score: number): string => {
  return score.toFixed(4);
};

const retryTraining = () => {
  // Navigate back to training with pre-filled data
  router.push('/train');
};

const getRequiredFeatures = (): string[] => {
  if (!model.value) return [];
  
  // Get feature columns excluding the target feature
  const featureColumns = model.value.feature_columns || [];
  return featureColumns.filter(col => col !== model.value!.target_feature);
};

onMounted(() => {
  fetchModel();
});
</script>

<style scoped>
/* Status-specific animations */
.animate-pulse-slow {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Glow effects for status badges */
.bg-green-500\/20 {
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.1);
}

.bg-blue-500\/20 {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.1);
}

.bg-red-500\/20 {
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.1);
}

/* Smooth transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}
</style>