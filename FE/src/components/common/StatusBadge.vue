<template>
  <span 
    :class="[
      'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium capitalize transition-all duration-200',
      statusClasses,
      size === 'sm' ? 'px-2 py-0.5 text-xs' : '',
      size === 'lg' ? 'px-4 py-2 text-base' : ''
    ]"
  >
    <component 
      :is="statusIcon" 
      :class="[
        'mr-2',
        size === 'sm' ? 'w-3 h-3' : 'w-4 h-4',
        size === 'lg' ? 'w-5 h-5' : '',
        iconClass
      ]" 
    />
    {{ statusText }}
    <span v-if="showProgress && status === 'training'" class="ml-2">
      <div class="flex space-x-1">
        <div class="w-1 h-1 bg-current rounded-full animate-pulse"></div>
        <div class="w-1 h-1 bg-current rounded-full animate-pulse delay-75"></div>
        <div class="w-1 h-1 bg-current rounded-full animate-pulse delay-150"></div>
      </div>
    </span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { CheckCircle, Clock, XCircle, Trash2, AlertTriangle } from 'lucide-vue-next';

interface Props {
  status: 'training' | 'completed' | 'failed' | 'deleted' | string;
  size?: 'sm' | 'md' | 'lg';
  showProgress?: boolean;
  customText?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showProgress: true
});

const statusClasses = computed(() => {
  switch (props.status) {
    case 'completed':
      return 'bg-green-500/20 text-green-300 border border-green-500/30 shadow-green-500/10';
    case 'training':
      return 'bg-blue-500/20 text-blue-300 border border-blue-500/30 shadow-blue-500/10';
    case 'failed':
      return 'bg-red-500/20 text-red-300 border border-red-500/30 shadow-red-500/10';
    case 'deleted':
      return 'bg-gray-500/20 text-gray-300 border border-gray-500/30 shadow-gray-500/10';
    default:
      return 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30 shadow-yellow-500/10';
  }
});

const statusIcon = computed(() => {
  switch (props.status) {
    case 'completed':
      return CheckCircle;
    case 'training':
      return Clock;
    case 'failed':
      return XCircle;
    case 'deleted':
      return Trash2;
    default:
      return AlertTriangle;
  }
});

const iconClass = computed(() => {
  switch (props.status) {
    case 'completed':
      return 'text-green-400';
    case 'training':
      return 'text-blue-400 animate-pulse';
    case 'failed':
      return 'text-red-400';
    case 'deleted':
      return 'text-gray-400';
    default:
      return 'text-yellow-400';
  }
});

const statusText = computed(() => {
  if (props.customText) return props.customText;
  
  switch (props.status) {
    case 'completed':
      return 'Completed';
    case 'training':
      return 'Training';
    case 'failed':
      return 'Failed';
    case 'deleted':
      return 'Deleted';
    default:
      return props.status;
  }
});
</script>

<style scoped>
/* Glow effect per i badge */
.shadow-green-500\/10 {
  box-shadow: 0 0 15px rgba(34, 197, 94, 0.1);
}

.shadow-blue-500\/10 {
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.1);
}

.shadow-red-500\/10 {
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.1);
}

.shadow-gray-500\/10 {
  box-shadow: 0 0 15px rgba(107, 114, 128, 0.1);
}

.shadow-yellow-500\/10 {
  box-shadow: 0 0 15px rgba(234, 179, 8, 0.1);
}

/* Animation per i punti di caricamento */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

.delay-75 {
  animation-delay: 75ms;
}

.delay-150 {
  animation-delay: 150ms;
}
</style>