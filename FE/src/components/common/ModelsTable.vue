<template>
  <div class="rounded-2xl overflow-hidden max-h-screen p-[40px] flex flex-col bg-black/20 backdrop-blur-sm">
    <div class="px-2 py-4 border-b border-white/20">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-2xl font-semibold text-white mb-2">Trained Models</h3>
          <p class="text-sm text-white/70">
            Showing {{ models.length }} trained {{ models.length === 1 ? 'model' : 'models' }}
          </p>
        </div>
        <button
          @click="$emit('refresh')"
          class="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white/90 hover:text-white transition-all duration-200 backdrop-blur-sm group"
        >
          <RotateCcw class="w-4 h-4 group-hover:rotate-180 transition-transform duration-300" />
          <span class="font-medium">Refresh</span>
        </button>
      </div>
    </div>
    
    <div v-if="models.length === 0" class="flex-grow flex items-center justify-center">
      <div class="text-center">
        <div class="w-20 h-20 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center mx-auto mb-4">
          <Brain class="w-10 h-10 text-white/50" />
        </div>
        <h3 class="text-xl font-medium text-white/80 mb-2">No models yet</h3>
        <p class="text-white/60 mb-6">Train your first model to see it here</p>
        <router-link
          to="/train"
          class="inline-flex items-center gap-2 px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/30 rounded-xl text-white font-medium transition-all duration-200 backdrop-blur-sm"
        >
          <Plus class="w-4 h-4" />
          Start Training
        </router-link>
      </div>
    </div>
    
    <div v-else class="overflow-y-auto flex-grow rounded-2xl mt-4 scrollbar-dark">
      <table class="min-w-full divide-y divide-white/10">
        <thead class="sticky top-0 z-10 bg-black/40 backdrop-blur-md">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20">
              Model Name
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20">
              Status
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20">
              Problem Type
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20">
              Target Feature
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20">
              Score
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20">
              Created
            </th>
            <th class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr
            v-for="(model, index) in models"
            :key="model.uuid"
            :data-status="model.status"
            :class="[
              'transition-all duration-200 hover:bg-white/5 cursor-pointer group',
              model.status === 'training' ? 'opacity-75' : '',
              index % 2 === 0 ? 'bg-white/2' : 'bg-transparent'
            ]"
            @click="$emit('view-model', model.uuid)"
          >
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/80 border-r border-white/5">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <Brain class="w-4 h-4 text-white" />
                </div>
                <div>
                  <span class="font-medium text-white">{{ model.name }}</span>
                  <div class="text-xs text-white/50 font-mono">{{ model.uuid.slice(0, 8) }}...</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/80 border-r border-white/5">
              <StatusBadge 
                :status="model.status" 
                size="sm"
                :show-progress="true"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/80 border-r border-white/5">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-white/10 text-white/90 capitalize">
                {{ model.problem_type }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/80 border-r border-white/5">
              <span class="font-mono">{{ model.target_feature }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/80 border-r border-white/5">
              <span v-if="model.best_score" class="font-mono text-green-400">
                {{ formatScore(model.best_score) }}
              </span>
              <span v-else class="text-white/50">—</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/80 border-r border-white/5">
              <span class="font-mono">{{ formatDate(model.created_at) }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-white/80">
              <div class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                <button
                  @click.stop="$emit('view-model', model.uuid)"
                  class="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/20 transition-all duration-200 group/btn"
                  title="View Model Details"
                >
                  <Eye class="w-4 h-4 text-white/70 group-hover/btn:text-white" />
                </button>
                <button
                  v-if="model.status === 'completed'"
                  @click.stop="handlePredict(model.uuid)"
                  class="p-2 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 transition-all duration-200 group/btn"
                  title="Make Predictions"
                >
                  <Zap class="w-4 h-4 text-blue-400 group-hover/btn:text-blue-300" />
                </button>
                <button
                  @click.stop="$emit('delete-model', model.uuid)"
                  :disabled="model.status === 'training'"
                  :class="[
                    'p-2 rounded-lg border transition-all duration-200 group/btn',
                    model.status === 'training' 
                      ? 'bg-gray-500/10 border-gray-500/20 cursor-not-allowed opacity-50'
                      : 'bg-red-500/10 hover:bg-red-500/20 border-red-500/30'
                  ]"
                  title="Delete Model"
                >
                  <Trash2 
                    :class="[
                      'w-4 h-4',
                      model.status === 'training' 
                        ? 'text-gray-400'
                        : 'text-red-400 group-hover/btn:text-red-300'
                    ]" 
                  />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Brain, Eye, Trash2, Plus, RotateCcw, Zap } from 'lucide-vue-next';
import StatusBadge from './StatusBadge.vue';
import type { TrainedModel } from '../../types';

interface Props {
  models: TrainedModel[];
}

interface Emits {
  (e: 'view-model', uuid: string): void;
  (e: 'delete-model', uuid: string): void;
  (e: 'refresh'): void;
  (e: 'predict', uuid: string): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

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

const formatScore = (score: number): string => {
  return score.toFixed(4);
};

const handlePredict = (uuid: string) => {
  emit('predict', uuid);
  // For now, just redirect to model detail page
  // In future this could open a prediction modal
  emit('view-model', uuid);
};
</script>

<style scoped>
/* Custom scrollbar per tema scuro */
.scrollbar-dark {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.3) transparent;
}

.scrollbar-dark::-webkit-scrollbar {
  width: 8px;
}

.scrollbar-dark::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-dark::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  border: 2px solid transparent;
}

.scrollbar-dark::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

/* Animazione hover per le righe */
tbody tr {
  position: relative;
}

tbody tr::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 50%, rgba(255, 255, 255, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

tbody tr:hover::before {
  opacity: 1;
}

/* Effetto glow per i buttons */
button:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
}

/* Disabilita click per modelli in training (tranne actions) */
tbody tr[data-status="training"] {
  cursor: default;
}

tbody tr[data-status="training"] td:not(:last-child) {
  pointer-events: none;
}
</style>