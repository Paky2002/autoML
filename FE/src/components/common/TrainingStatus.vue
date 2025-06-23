<template>
  <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-xl font-semibold text-white">Training Status</h3>
      <button
        v-if="canClose"
        @click="$emit('close')"
        class="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/20 transition-all duration-200"
      >
        <X class="w-4 h-4 text-white/70" />
      </button>
    </div>

    <!-- Training Progress -->
    <div v-if="status === 'training'" class="space-y-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
        <div>
          <p class="text-white font-medium">Training in Progress</p>
          <p class="text-white/70 text-sm">Model: {{ modelName }}</p>
        </div>
      </div>
      
      <div class="bg-white/5 rounded-xl p-4 border border-white/10">
        <div class="flex justify-between items-center mb-2">
          <span class="text-white/80 text-sm">Estimated Progress</span>
          <span class="text-white/80 text-sm">{{ Math.floor(progress) }}%</span>
        </div>
        <div class="w-full bg-white/10 rounded-full h-2">
          <div
            class="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500 ease-out"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <p class="text-white/60 text-xs mt-2">
          Training may take several minutes depending on dataset size and complexity
        </p>
      </div>
    </div>

    <!-- Completed Status -->
    <div v-else-if="status === 'completed'" class="space-y-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
          <CheckCircle class="w-5 h-5 text-green-400" />
        </div>
        <div>
          <p class="text-white font-medium">Training Completed!</p>
          <p class="text-white/70 text-sm">Model: {{ modelName }}</p>
        </div>
      </div>
      
      <div v-if="trainingResult" class="bg-green-500/10 rounded-xl p-4 border border-green-500/30">
        <h4 class="text-green-200 font-medium mb-3">Training Results</h4>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-green-300/70">Best Model:</span>
            <p class="text-green-200 font-mono">{{ trainingResult.best_model_name || 'N/A' }}</p>
          </div>
          <div>
            <span class="text-green-300/70">Best Score:</span>
            <p class="text-green-200 font-mono">{{ formatScore(trainingResult.best_score) }}</p>
          </div>
        </div>
        <div class="mt-4 flex gap-3">
          <button
            @click="$emit('view-model', modelUuid)"
            class="flex items-center gap-2 px-4 py-2 bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 rounded-xl text-green-200 text-sm font-medium transition-all duration-200"
          >
            <Eye class="w-4 h-4" />
            View Model
          </button>
          <button
            @click="$emit('train-another')"
            class="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white/90 text-sm font-medium transition-all duration-200"
          >
            <Plus class="w-4 h-4" />
            Train Another
          </button>
        </div>
      </div>
    </div>

    <!-- Failed Status -->
    <div v-else-if="status === 'failed'" class="space-y-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center">
          <AlertCircle class="w-5 h-5 text-red-400" />
        </div>
        <div>
          <p class="text-white font-medium">Training Failed</p>
          <p class="text-white/70 text-sm">Model: {{ modelName }}</p>
        </div>
      </div>
      
      <div class="bg-red-500/10 rounded-xl p-4 border border-red-500/30">
        <h4 class="text-red-200 font-medium mb-2">Error Details</h4>
        <p class="text-red-300/80 text-sm">{{ errorMessage || 'An unknown error occurred during training' }}</p>
        <div class="mt-4 flex gap-3">
          <button
            @click="$emit('retry-training')"
            class="flex items-center gap-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-xl text-red-200 text-sm font-medium transition-all duration-200"
          >
            <RotateCcw class="w-4 h-4" />
            Retry Training
          </button>
          <button
            @click="$emit('train-another')"
            class="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white/90 text-sm font-medium transition-all duration-200"
          >
            <Plus class="w-4 h-4" />
            Train New Model
          </button>
        </div>
      </div>
    </div>

    <!-- Unknown Status -->
    <div v-else class="space-y-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-yellow-500/20 rounded-full flex items-center justify-center">
          <Clock class="w-5 h-5 text-yellow-400" />
        </div>
        <div>
          <p class="text-white font-medium">Unknown Status</p>
          <p class="text-white/70 text-sm">Status: {{ status }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { CheckCircle, AlertCircle, Clock, Eye, Plus, RotateCcw, X } from 'lucide-vue-next';

interface Props {
  modelUuid: string;
  modelName: string;
  status: string;
  trainingResult?: {
    best_model_name?: string;
    best_score?: number;
    leaderboard?: any[];
  };
  errorMessage?: string;
  canClose?: boolean;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

interface Emits {
  (e: 'status-changed', status: string): void;
  (e: 'view-model', uuid: string): void;
  (e: 'train-another'): void;
  (e: 'retry-training'): void;
  (e: 'close'): void;
}

const props = withDefaults(defineProps<Props>(), {
  canClose: true,
  autoRefresh: true,
  refreshInterval: 5000
});

const emit = defineEmits<Emits>();

const progress = ref(0);
let refreshTimer: NodeJS.Timeout | null = null;

const formatScore = (score?: number): string => {
  if (score === undefined || score === null) return 'N/A';
  return score.toFixed(4);
};

const updateProgress = () => {
  if (props.status === 'training') {
    // Simulate progress for visual feedback
    const currentProgress = progress.value;
    if (currentProgress < 90) {
      progress.value = Math.min(90, currentProgress + Math.random() * 5);
    }
  } else if (props.status === 'completed') {
    progress.value = 100;
  }
};

const checkStatus = async () => {
  if (props.status === 'training' && props.autoRefresh) {
    try {
      // In a real implementation, you would call an API to check status
      // For now, we'll emit the current status
      emit('status-changed', props.status);
    } catch (error) {
      console.error('Error checking training status:', error);
    }
  }
};

onMounted(() => {
  updateProgress();
  
  if (props.autoRefresh && props.status === 'training') {
    refreshTimer = setInterval(() => {
      checkStatus();
      updateProgress();
    }, props.refreshInterval);
  }
});

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }
});
</script>

<style scoped>
/* Animazioni personalizzate */
@keyframes pulse-success {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse-success {
  animation: pulse-success 2s ease-in-out infinite;
}

/* Effetto glow per il progress bar */
.bg-gradient-to-r {
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
}
</style>