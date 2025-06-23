<template>
  <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-semibold text-white mb-2 flex items-center gap-3">
          <Zap class="w-6 h-6" />
          Live Prediction Test
        </h2>
        <p class="text-white/70">Upload a test dataset and see real-time predictions</p>
      </div>
      <div v-if="isActive" class="flex items-center gap-3">
        <!-- Real-time Accuracy Badge -->
        <div v-if="accuracyStats.total > 0" 
             :class="[
               'flex items-center gap-2 px-3 py-1 rounded-lg border text-sm font-medium',
               accuracyStats.accuracy >= 0.8 
                 ? 'bg-green-500/20 border-green-500/40 text-green-200' 
                 : accuracyStats.accuracy >= 0.6
                 ? 'bg-yellow-500/20 border-yellow-500/40 text-yellow-200'
                 : 'bg-red-500/20 border-red-500/40 text-red-200'
             ]">
          <Target class="w-4 h-4" />
          {{ (accuracyStats.accuracy * 100).toFixed(1) }}% Accuracy
        </div>
        
        <span class="text-white/70 text-sm">{{ currentRow }}/{{ totalRows }}</span>
        <button
          @click="togglePrediction"
          :class="[
            'flex items-center gap-2 px-4 py-2 rounded-xl font-medium transition-all duration-200',
            isPaused 
              ? 'bg-green-500/20 hover:bg-green-500/30 border border-green-500/50 text-green-200'
              : 'bg-yellow-500/20 hover:bg-yellow-500/30 border border-yellow-500/50 text-yellow-200'
          ]"
        >
          <component :is="isPaused ? Play : Pause" class="w-4 h-4" />
          {{ isPaused ? 'Resume' : 'Pause' }}
        </button>
        <button
          @click="stopPrediction"
          class="flex items-center gap-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 rounded-xl text-red-200 font-medium transition-all duration-200"
        >
          <Square class="w-4 h-4" />
          Stop
        </button>
      </div>
    </div>

    <!-- File Upload Area -->
    <div v-if="!isActive && !testDataset" class="mb-6">
      <div
        @click="triggerFileInput"
        @dragover.prevent="handleDragOver"
        @dragleave.prevent="handleDragLeave"
        @drop.prevent="handleDrop"
        :class="[
          'border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300',
          isDragOver ? 'border-white/60 bg-white/10' : 'border-white/30 hover:border-white/50 hover:bg-white/5'
        ]"
      >
        <input
          ref="fileInput"
          type="file"
          accept=".csv"
          @change="handleFileSelect"
          class="hidden"
        >
        
        <div class="flex flex-col items-center gap-4">
          <div class="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center">
            <Upload class="w-8 h-8 text-white/70" />
          </div>
          <div>
            <p class="text-white font-medium mb-2">Upload Test Dataset</p>
            <p class="text-white/70 text-sm mb-1">CSV file with the same features as training data</p>
            <p class="text-yellow-200 text-xs bg-yellow-500/10 px-3 py-1 rounded-full border border-yellow-500/30">
              ⚠️ Must include <span class="font-mono">{{ targetFeature }}</span> column for accuracy calculation
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Dataset Info -->
    <div v-if="testDataset && !isActive" class="mb-6">
      <div class="bg-white/5 rounded-xl p-6 border border-white/10">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <FileText class="w-5 h-5 text-white/70" />
            <div>
              <h3 class="text-white font-medium">{{ testDataset.filename }}</h3>
              <p class="text-white/70 text-sm">{{ testDataset.totalRows }} rows • {{ testDataset.headers.length }} columns</p>
            </div>
          </div>
          <button
            @click="clearDataset"
            class="p-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/20 transition-all duration-200"
          >
            <X class="w-4 h-4 text-white/70" />
          </button>
        </div>

        <!-- Header Validation -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <h4 class="text-white/90 font-medium mb-2">Required Features</h4>
            <div class="space-y-1">
              <div 
                v-for="feature in props.requiredFeatures" 
                :key="feature"
                class="flex items-center gap-2 text-sm"
              >
                <CheckCircle v-if="testDataset.headers.includes(feature)" class="w-4 h-4 text-green-400" />
                <XCircle v-else class="w-4 h-4 text-red-400" />
                <span :class="testDataset.headers.includes(feature) ? 'text-green-300' : 'text-red-300'">
                  {{ feature }}
                </span>
              </div>
            </div>
          </div>
          <div>
            <h4 class="text-white/90 font-medium mb-2">Target Feature</h4>
            <div class="flex items-center gap-2 text-sm mb-3">
              <CheckCircle v-if="testDataset.headers.includes(props.targetFeature)" class="w-4 h-4 text-green-400" />
              <XCircle v-else class="w-4 h-4 text-red-400" />
              <span :class="testDataset.headers.includes(props.targetFeature) ? 'text-green-300' : 'text-red-300'">
                {{ props.targetFeature }}
              </span>
            </div>
            <div class="text-xs text-white/60">
              {{ datasetValidationMessage }}
            </div>
          </div>
        </div>

        <!-- Speed Control -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <label class="text-white/70 text-sm">Prediction Speed:</label>
            <select 
              v-model="predictionSpeed"
              class="px-3 py-1 bg-white/5 border border-white/20 rounded-lg text-white text-sm"
            >
              <option value="500">Fast (0.5s)</option>
              <option value="1000">Normal (1s)</option>
              <option value="2000">Slow (2s)</option>
            </select>
          </div>
          <button
            @click="startPrediction"
            :disabled="!isDatasetValid"
            :class="[
              'flex items-center gap-2 px-6 py-3 rounded-xl font-medium transition-all duration-200',
              isDatasetValid
                ? 'bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/50 text-blue-200'
                : 'bg-gray-500/20 border border-gray-500/30 text-gray-400 cursor-not-allowed'
            ]"
          >
            <Play class="w-4 h-4" />
            Start Testing
          </button>
        </div>
      </div>
    </div>

    <!-- Prediction Results -->
    <div v-if="isActive" class="space-y-6">
      <!-- Progress Bar with Accuracy -->
      <div class="bg-white/5 rounded-xl p-4 border border-white/10">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Progress Section -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-white/80 text-sm">Progress</span>
              <span class="text-white/80 text-sm">{{ Math.round((currentRow / totalRows) * 100) }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-2">
              <div
                class="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${(currentRow / totalRows) * 100}%` }"
              ></div>
            </div>
            <div class="flex justify-between items-center mt-2 text-xs text-white/60">
              <span>{{ currentRow }} / {{ totalRows }} predictions</span>
              <span v-if="predictions.length > 0">
                Avg time: {{ averagePredictionTime }}ms
              </span>
            </div>
          </div>
          
          <!-- Accuracy Section -->
          <div v-if="accuracyStats.total > 0">
            <div class="flex justify-between items-center mb-2">
              <span class="text-white/80 text-sm">Accuracy</span>
              <span class="text-white/80 text-sm font-bold">{{ (accuracyStats.accuracy * 100).toFixed(1) }}%</span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="bg-green-500/20 rounded-lg p-2 border border-green-500/30">
                <div class="text-green-300 font-medium">Correct</div>
                <div class="text-green-200 text-lg font-bold">{{ accuracyStats.correct }}</div>
              </div>
              <div class="bg-red-500/20 rounded-lg p-2 border border-red-500/30">
                <div class="text-red-300 font-medium">Incorrect</div>
                <div class="text-red-200 text-lg font-bold">{{ accuracyStats.incorrect }}</div>
              </div>
            </div>
            <div class="mt-2 w-full bg-white/10 rounded-full h-1">
              <div
                class="bg-gradient-to-r from-green-500 to-green-400 h-1 rounded-full transition-all duration-500"
                :style="{ width: `${accuracyStats.accuracy * 100}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Prediction -->
      <div v-if="currentPrediction" class="bg-white/5 rounded-xl p-6 border border-white/10">
        <h3 class="text-white font-medium mb-4">Current Prediction</h3>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Input Features -->
          <div>
            <h4 class="text-white/80 text-sm font-medium mb-3">Input Features</h4>
            <div class="space-y-2 max-h-48 overflow-y-auto">
              <div 
                v-for="(value, feature) in currentPrediction.input" 
                :key="feature"
                class="flex justify-between items-center py-1"
              >
                <span class="text-white/70 text-sm">{{ feature }}:</span>
                <span class="text-white font-mono text-sm">{{ formatValue(value) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Prediction Output -->
          <div>
            <h4 class="text-white/80 text-sm font-medium mb-3">Prediction Result</h4>
            <div class="space-y-3">
              <!-- Predicted Value -->
              <div class="bg-blue-500/10 rounded-lg p-4 border border-blue-500/30">
                <div class="flex items-center gap-2 mb-2">
                  <Target class="w-4 h-4 text-blue-400" />
                  <span class="text-blue-200 text-sm font-medium">Predicted {{ targetFeature }}</span>
                </div>
                <div class="text-2xl font-bold text-blue-200 mb-2">
                  {{ formatPrediction(currentPrediction.result) }}
                </div>
                <div v-if="currentPrediction.probabilities" class="space-y-1">
                  <p class="text-blue-300/70 text-xs mb-2">Confidence:</p>
                  <div 
                    v-for="(prob, index) in currentPrediction.probabilities" 
                    :key="index"
                    class="flex justify-between items-center"
                  >
                    <span class="text-blue-300/80 text-xs">Class {{ index }}:</span>
                    <span class="text-blue-200 text-xs font-mono">{{ (prob * 100).toFixed(1) }}%</span>
                  </div>
                </div>
              </div>
              
              <!-- Actual Value (if available) -->
              <div v-if="currentPrediction.actualValue !== undefined" class="bg-green-500/10 rounded-lg p-4 border border-green-500/30">
                <div class="flex items-center gap-2 mb-2">
                  <CheckCircle class="w-4 h-4 text-green-400" />
                  <span class="text-green-200 text-sm font-medium">Actual {{ targetFeature }}</span>
                </div>
                <div class="text-2xl font-bold text-green-200 mb-2">
                  {{ formatPrediction(currentPrediction.actualValue) }}
                </div>
              </div>
              
              <!-- Correctness Indicator -->
              <div v-if="currentPrediction.isCorrect !== undefined" 
                   :class="[
                     'rounded-lg p-3 border text-center',
                     currentPrediction.isCorrect 
                       ? 'bg-green-500/10 border-green-500/30' 
                       : 'bg-red-500/10 border-red-500/30'
                   ]">
                <div class="flex items-center justify-center gap-2">
                  <CheckCircle v-if="currentPrediction.isCorrect" class="w-5 h-5 text-green-400" />
                  <XCircle v-else class="w-5 h-5 text-red-400" />
                  <span :class="currentPrediction.isCorrect ? 'text-green-200' : 'text-red-200'" class="font-medium">
                    {{ currentPrediction.isCorrect ? 'Correct Prediction!' : 'Incorrect Prediction' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Predictions History -->
      <div class="bg-white/5 rounded-xl p-6 border border-white/10">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-white font-medium">Recent Predictions</h3>
          <button
            @click="exportResults"
            class="flex items-center gap-2 px-3 py-1 bg-white/5 hover:bg-white/10 border border-white/20 rounded-lg text-white/80 text-sm transition-all duration-200"
          >
            <Download class="w-4 h-4" />
            Export
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead>
              <tr class="border-b border-white/10">
                <th class="text-left py-2 text-white/70">#</th>
                <th class="text-left py-2 text-white/70">Predicted</th>
                <th class="text-left py-2 text-white/70">Actual</th>
                <th class="text-left py-2 text-white/70">Correct</th>
                <th class="text-left py-2 text-white/70">Confidence</th>
                <th class="text-left py-2 text-white/70">Time</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(pred, index) in predictions.slice(-10)" 
                :key="index"
                class="border-b border-white/5"
              >
                <td class="py-2 text-white/60 font-mono">{{ predictions.length - 10 + index + 1 }}</td>
                <td class="py-2 text-white font-mono">{{ formatPrediction(pred.result) }}</td>
                <td class="py-2 text-white/70 font-mono">
                  {{ pred.actualValue !== undefined ? formatPrediction(pred.actualValue) : '—' }}
                </td>
                <td class="py-2">
                  <span v-if="pred.isCorrect !== undefined" 
                        :class="[
                          'inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium',
                          pred.isCorrect 
                            ? 'bg-green-500/20 text-green-300' 
                            : 'bg-red-500/20 text-red-300'
                        ]">
                    <CheckCircle v-if="pred.isCorrect" class="w-3 h-3" />
                    <XCircle v-else class="w-3 h-3" />
                    {{ pred.isCorrect ? 'Yes' : 'No' }}
                  </span>
                  <span v-else class="text-white/50">—</span>
                </td>
                <td class="py-2 text-white/70">
                  {{ pred.confidence ? (pred.confidence * 100).toFixed(1) + '%' : '—' }}
                </td>
                <td class="py-2 text-white/60 font-mono">{{ pred.duration }}ms</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="bg-red-500/10 rounded-xl p-4 border border-red-500/30">
      <div class="flex items-center gap-3">
        <AlertCircle class="w-5 h-5 text-red-400" />
        <div>
          <p class="text-red-200 font-medium">Prediction Error</p>
          <p class="text-red-300/80 text-sm">{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';
import { 
  Zap, Upload, FileText, X, Play, Pause, Square, CheckCircle, XCircle, 
  Target, Download, AlertCircle 
} from 'lucide-vue-next';
import { useApi } from '../../composables/useApi';
import type { DatasetInfo } from '../../types';

interface Props {
  modelUuid: string;
  targetFeature: string;
  requiredFeatures: string[];
}

interface PredictionResult {
  input: Record<string, any>;
  result: any;
  actualValue?: any;  // Valore reale dal test set
  isCorrect?: boolean;  // Se la predizione è corretta
  probabilities?: number[];
  confidence?: number;
  duration: number;
}

interface AccuracyStats {
  total: number;
  correct: number;
  incorrect: number;
  accuracy: number;
  byClass?: Record<string, { correct: number; total: number; accuracy: number }>;
}

const props = defineProps<Props>();

const { predict } = useApi();

// Component state
const testDataset = ref<DatasetInfo | null>(null);
const isActive = ref(false);
const isPaused = ref(false);
const currentRow = ref(0);
const totalRows = ref(0);
const predictionSpeed = ref(1000);
const predictions = ref<PredictionResult[]>([]);
const currentPrediction = ref<PredictionResult | null>(null);
const error = ref<string | null>(null);
const accuracyStats = ref<AccuracyStats>({ total: 0, correct: 0, incorrect: 0, accuracy: 0 });

// File upload state
const fileInput = ref<HTMLInputElement>();
const isDragOver = ref(false);

// Prediction interval
let predictionInterval: NodeJS.Timeout | null = null;

const isDatasetValid = computed(() => {
  if (!testDataset.value) return false;
  
  // Verifica che ci siano le feature richieste E la target feature
  const hasRequiredFeatures = props.requiredFeatures.every(feature => 
    testDataset.value!.headers.includes(feature)
  );
  const hasTargetFeature = testDataset.value.headers.includes(props.targetFeature);
  
  return hasRequiredFeatures && hasTargetFeature;
});

const averagePredictionTime = computed(() => {
  if (predictions.value.length === 0) return 0;
  const total = predictions.value.reduce((sum, pred) => sum + pred.duration, 0);
  return Math.round(total / predictions.value.length);
});

const datasetValidationMessage = computed(() => {
  if (!testDataset.value) return '';
  
  const missingFeatures = props.requiredFeatures.filter(feature => 
    !testDataset.value!.headers.includes(feature)
  );
  
  const hasTarget = testDataset.value.headers.includes(props.targetFeature);
  
  if (missingFeatures.length > 0 && !hasTarget) {
    return `Missing required features: ${missingFeatures.join(', ')} and target feature: ${props.targetFeature}`;
  } else if (missingFeatures.length > 0) {
    return `Missing required features: ${missingFeatures.join(', ')}`;
  } else if (!hasTarget) {
    return `Missing target feature: ${props.targetFeature}`;
  }
  
  return 'Dataset is valid for testing';
});

// File handling
const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    processFile(file);
  }
};

const handleDragOver = () => {
  isDragOver.value = true;
};

const handleDragLeave = () => {
  isDragOver.value = false;
};

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false;
  const file = event.dataTransfer?.files?.[0];
  if (file) {
    processFile(file);
  }
};

const processFile = async (file: File) => {
  try {
    error.value = null;
    
    if (!file.name.toLowerCase().endsWith('.csv')) {
      throw new Error('Please upload a CSV file');
    }

    // Parse CSV file
    const text = await file.text();
    const lines = text.split('\n').filter(line => line.trim());
    
    if (lines.length < 2) {
      throw new Error('CSV file must have at least headers and one data row');
    }

    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    const rows = lines.slice(1).map(line => 
      line.split(',').map(cell => cell.trim().replace(/"/g, ''))
    );

    testDataset.value = {
      filename: file.name,
      headers,
      rows,
      totalRows: rows.length,
      fileSize: file.size
    };

    totalRows.value = rows.length;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to process file';
  }
};

const clearDataset = () => {
  testDataset.value = null;
  currentRow.value = 0;
  totalRows.value = 0;
  predictions.value = [];
  currentPrediction.value = null;
  error.value = null;
  
  // Reset accuracy stats
  accuracyStats.value = {
    total: 0,
    correct: 0,
    incorrect: 0,
    accuracy: 0
  };
};

// Prediction control
const startPrediction = () => {
  if (!testDataset.value || !isDatasetValid.value) return;
  
  isActive.value = true;
  isPaused.value = false;
  currentRow.value = 0;
  predictions.value = [];
  
  // Reset accuracy stats
  accuracyStats.value = {
    total: 0,
    correct: 0,
    incorrect: 0,
    accuracy: 0
  };
  
  error.value = null;
  
  runPrediction();
};

const togglePrediction = () => {
  isPaused.value = !isPaused.value;
  
  if (!isPaused.value) {
    runPrediction();
  } else if (predictionInterval) {
    clearInterval(predictionInterval);
  }
};

const stopPrediction = () => {
  isActive.value = false;
  isPaused.value = false;
  
  if (predictionInterval) {
    clearInterval(predictionInterval);
    predictionInterval = null;
  }
};

const runPrediction = () => {
  if (!testDataset.value || isPaused.value) return;
  
  predictionInterval = setInterval(async () => {
    if (currentRow.value >= totalRows.value) {
      stopPrediction();
      return;
    }
    
    await makePrediction();
    currentRow.value++;
  }, predictionSpeed.value);
};

const makePrediction = async () => {
  if (!testDataset.value) return;
  
  const startTime = Date.now();
  
  try {
    const rowData = testDataset.value.rows[currentRow.value];
    const input: Record<string, any> = {};
    
    // Create input object excluding target feature
    let actualValue: any = undefined;
    testDataset.value.headers.forEach((header, index) => {
      if (header === props.targetFeature) {
        // Store the actual value for comparison
        actualValue = rowData[index];
      } else {
        // Add to prediction input
        input[header] = rowData[index];
      }
    });
    
    // Make API call for prediction
    const result = await predict(props.modelUuid, [input]);
    
    const duration = Date.now() - startTime;
    
    if (result.success) {
      const predictedValue = result.predictions[0];
      
      // Determine if prediction is correct
      let isCorrect: boolean | undefined = undefined;
      if (actualValue !== undefined) {
        isCorrect = compareValues(predictedValue, actualValue);
      }
      
      const predictionResult: PredictionResult = {
        input,
        result: predictedValue,
        actualValue,
        isCorrect,
        probabilities: result.probabilities?.[0],
        confidence: result.probabilities?.[0] ? Math.max(...result.probabilities[0]) : undefined,
        duration
      };
      
      predictions.value.push(predictionResult);
      currentPrediction.value = predictionResult;
      
      // Update accuracy stats
      updateAccuracyStats(predictionResult);
    } else {
      throw new Error(result.error || 'Prediction failed');
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Prediction failed';
    stopPrediction();
  }
};

const compareValues = (predicted: any, actual: any): boolean => {
  // Convert both values to strings for comparison to handle type mismatches
  const predStr = String(predicted).toLowerCase().trim();
  const actualStr = String(actual).toLowerCase().trim();
  
  // Try numeric comparison first
  const predNum = parseFloat(predStr);
  const actualNum = parseFloat(actualStr);
  
  if (!isNaN(predNum) && !isNaN(actualNum)) {
    // For numeric values, allow small tolerance
    return Math.abs(predNum - actualNum) < 0.0001;
  }
  
  // For categorical values, exact string match
  return predStr === actualStr;
};

const updateAccuracyStats = (predictionResult: PredictionResult) => {
  if (predictionResult.isCorrect === undefined) return;
  
  accuracyStats.value.total++;
  
  if (predictionResult.isCorrect) {
    accuracyStats.value.correct++;
  } else {
    accuracyStats.value.incorrect++;
  }
  
  accuracyStats.value.accuracy = accuracyStats.value.correct / accuracyStats.value.total;
};

// Utility functions
const formatValue = (value: any): string => {
  if (typeof value === 'number') {
    return value.toFixed(3);
  }
  return String(value);
};

const formatPrediction = (prediction: any): string => {
  if (typeof prediction === 'number') {
    return prediction.toFixed(4);
  }
  return String(prediction);
};

const exportResults = () => {
  if (predictions.value.length === 0) return;
  
  const csvHeaders = ['Row', 'Predicted', 'Actual', 'Correct', 'Confidence', 'Duration_ms'];
  const csvRows = [
    csvHeaders,
    ...predictions.value.map((pred, index) => [
      index + 1,
      pred.result,
      pred.actualValue !== undefined ? pred.actualValue : '',
      pred.isCorrect !== undefined ? (pred.isCorrect ? 'Yes' : 'No') : '',
      pred.confidence ? (pred.confidence * 100).toFixed(2) + '%' : '',
      pred.duration
    ])
  ];
  
  // Add accuracy summary at the end
  if (accuracyStats.value.total > 0) {
    csvRows.push([]);
    csvRows.push(['SUMMARY']);
    csvRows.push(['Total Predictions', accuracyStats.value.total, '', '', '', '']);
    csvRows.push(['Correct', accuracyStats.value.correct, '', '', '', '']);
    csvRows.push(['Incorrect', accuracyStats.value.incorrect, '', '', '', '']);
    csvRows.push(['Accuracy', (accuracyStats.value.accuracy * 100).toFixed(2) + '%', '', '', '', '']);
  }
  
  const csv = csvRows.map(row => row.join(',')).join('\n');
  
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `predictions_accuracy_${props.modelUuid}_${Date.now()}.csv`;
  a.click();
  URL.revokeObjectURL(url);
};

// Cleanup
onUnmounted(() => {
  if (predictionInterval) {
    clearInterval(predictionInterval);
  }
});
</script>

<style scoped>
/* Scrollbar styling */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Progress animation */
@keyframes pulse-progress {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse-progress {
  animation: pulse-progress 2s ease-in-out infinite;
}
</style>