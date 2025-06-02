<template>
  <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
    <h3 class="text-xl font-semibold text-white mb-6">Training Configuration</h3>
    
    <form @submit.prevent="handleSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Target Feature -->
      <div>
        <label class="block text-sm font-medium text-white/90 mb-2">
          Target Feature *
        </label>
        <select
          v-model="form.targetFeature"
          required
          class="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-white/50 focus:ring-2 focus:ring-white/30 focus:border-white/40 transition-all duration-200 backdrop-blur-sm"
        >
          <option value="" class="bg-gray-800 text-white">Select target feature</option>
          <option
            v-for="column in availableColumns"
            :key="column.name"
            :value="column.name"
            class="bg-gray-800 text-white"
          >
            {{ column.name }} ({{ column.type }})
          </option>
        </select>
      </div>

      <!-- Problem Type -->
      <div>
        <label class="block text-sm font-medium text-white/90 mb-2">
          Problem Type *
        </label>
        <select
          v-model="form.problemType"
          required
          class="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-white/50 focus:ring-2 focus:ring-white/30 focus:border-white/40 transition-all duration-200 backdrop-blur-sm"
        >
          <option value="" class="bg-gray-800 text-white">Auto-detect</option>
          <option value="regression" class="bg-gray-800 text-white">Regression</option>
          <option value="binary" class="bg-gray-800 text-white">Binary Classification</option>
          <option value="multiclass" class="bg-gray-800 text-white">Multiclass Classification</option>
        </select>
      </div>

      <!-- Time Limit -->
      <div>
        <label class="block text-sm font-medium text-white/90 mb-2">
          Time Limit (seconds)
        </label>
        <input
          v-model.number="form.timeLimit"
          type="number"
          min="60"
          max="7200"
          class="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-white/50 focus:ring-2 focus:ring-white/30 focus:border-white/40 transition-all duration-200 backdrop-blur-sm"
        >
      </div>

      <!-- Presets -->
      <div>
        <label class="block text-sm font-medium text-white/90 mb-2">
          Quality Preset
        </label>
        <select
          v-model="form.presets"
          class="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-white/50 focus:ring-2 focus:ring-white/30 focus:border-white/40 transition-all duration-200 backdrop-blur-sm"
        >
          <option value="best_quality" class="bg-gray-800 text-white">Best Quality</option>
          <option value="good_quality_faster" class="bg-gray-800 text-white">Good Quality (Faster)</option>
          <option value="optimize_for_deployment" class="bg-gray-800 text-white">Optimize for Deployment</option>
        </select>
      </div>

      <!-- Evaluation Metric -->
      <div>
        <label class="block text-sm font-medium text-white/90 mb-2">
          Evaluation Metric
        </label>
        <input
          v-model="form.evalMetric"
          type="text"
          placeholder="Auto-select based on problem type"
          class="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-white/50 focus:ring-2 focus:ring-white/30 focus:border-white/40 transition-all duration-200 backdrop-blur-sm"
        >
      </div>

      <!-- Verbosity -->
      <div>
        <label class="block text-sm font-medium text-white/90 mb-2">
          Verbosity Level
        </label>
        <select
          v-model.number="form.verbosity"
          class="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-white/50 focus:ring-2 focus:ring-white/30 focus:border-white/40 transition-all duration-200 backdrop-blur-sm"
        >
          <option :value="0" class="bg-gray-800 text-white">Silent</option>
          <option :value="1" class="bg-gray-800 text-white">Minimal</option>
          <option :value="2" class="bg-gray-800 text-white">Standard</option>
          <option :value="3" class="bg-gray-800 text-white">Verbose</option>
        </select>
      </div>

      <div class="md:col-span-2">
        <button
        type="submit"
        :disabled="!isFormValid || isTraining"
        :class="[
          'w-full py-3 px-6 rounded-xl font-medium transition-all duration-200',
          'bg-white/10 hover:bg-white/20 text-white border border-white/30',
          'backdrop-blur-sm',
          'disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white/10',
          'focus:ring-2 focus:ring-white/30 focus:outline-none',
          !isFormValid || isTraining ? '' : 'hover:shadow-lg hover:shadow-white/10'
        ]"
      >
        <span class="flex items-center justify-center gap-2">
          <span v-if="isTraining" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          {{ isTraining ? 'Starting Training...' : 'Start Training' }}
        </span>
      </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import type { ColumnInfo, TrainingConfig } from '../../types';

interface Props {
  columns: ColumnInfo[];
  isTraining: boolean;
}

interface Emits {
  (e: 'submit', config: TrainingConfig): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const form = ref<TrainingConfig>({
  targetFeature: '',
  problemType: 'regression',
  timeLimit: 600,
  presets: 'best_quality',
  evalMetric: '',
  verbosity: 2
});

const availableColumns = computed(() => 
  props.columns.filter(col => col.type === 'numeric' || col.type === 'categorical')
);

const isFormValid = computed(() => 
  form.value.targetFeature && form.value.problemType
);

const handleSubmit = () => {
  if (!isFormValid.value) return;
  emit('submit', { ...form.value });
};
</script>

<style scoped>
/* Personalizzazione degli input per il tema scuro */
select option {
  background-color: #1f2937;
  color: white;
}

/* Stili per browser webkit */
select::-webkit-scrollbar {
  width: 8px;
}

select::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

select::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

select::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Animazione per il focus */
input:focus, select:focus {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px rgba(255, 255, 255, 0.1);
}

/* Effetto glow per il button hover */
button:not(:disabled):hover {
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}
</style>