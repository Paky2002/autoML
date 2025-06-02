<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-2">
      <span class="text-sm font-medium text-gray-700 capitalize">
        {{ stageText }}
      </span>
      <span class="text-sm text-gray-500">
        {{ percentage }}%
      </span>
    </div>
    
    <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
      <div
        class="bg-gray-600 h-2 rounded-full transition-all duration-300 ease-out"
        :style="{ width: `${percentage}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  percentage: number;
  stage: string;
}

const props = defineProps<Props>();

const stageText = computed(() => {
  switch (props.stage) {
    case 'parsing': return 'Parsing CSV file';
    case 'analyzing': return 'Analyzing data structure';
    case 'complete': return 'Processing complete';
    default: return 'Processing';
  }
});
</script>