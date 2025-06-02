<template>
  <div class="w-[70vw] h-[60vh] mx-auto flex items-center justify-center">
    <div
      @click="triggerFileInput"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
      :class="[
        'relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 w-full h-full',
        'bg-transparent backdrop-blur-sm',
        isDragOver ? 'border-white/60 bg-white/10' : 'border-white/40 hover:border-white/60 hover:bg-white/5'
      ]"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".csv"
        @change="handleFileSelect"
        class="hidden"
      >
      
      <div class="flex flex-col items-center justify-center gap-6 h-full">
        <div class="w-20 h-20 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
          <Upload class="w-10 h-10 text-white" />
        </div>
        
        <div>
          <h3 class="text-2xl font-medium text-white mb-3">
            Upload your dataset
          </h3>
          <p class="text-white/80 text-base mb-2">
            Drag and drop your CSV file here, or click to browse
          </p>
          <p class="text-white/60 text-sm">
            Maximum file size: 100MB
          </p>
        </div>
      </div>
    </div>

    <!-- Progress -->
    <div v-if="isUploading" class="absolute inset-0 flex items-center justify-center">
      <div class="bg-black/50 backdrop-blur-sm rounded-2xl p-8 min-w-[300px]">
        <ProgressBar 
          :percentage="progressPercentage"
          :stage="currentStage"
        />
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="absolute bottom-4 left-1/2 transform -translate-x-1/2 max-w-md">
      <div class="p-4 bg-red-900/80 backdrop-blur-sm border border-red-700/50 rounded-xl">
        <p class="text-red-200 text-sm text-center">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Upload } from 'lucide-vue-next';
import ProgressBar from './ProgressBar.vue';

interface Props {
  isUploading: boolean;
  progressPercentage: number;
  currentStage: string;
  error: string | null;
}

interface Emits {
  (e: 'file-selected', file: File): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

const fileInput = ref<HTMLInputElement>();
const isDragOver = ref(false);

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    emit('file-selected', file);
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
    emit('file-selected', file);
  }
};
</script>