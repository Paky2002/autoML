<template>
  <nav class="w-full bg-transparent backdrop-blur-sm border-b border-white/10 px-6 py-4">
    <div class="flex items-center justify-between relative">
      <!-- View Model Button (Left) -->
      <button
        @click="$emit('view-model')"
        class="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white/90 hover:text-white transition-all duration-200 backdrop-blur-sm group"
      >
        <Eye class="w-4 h-4 group-hover:scale-110 transition-transform duration-200" />
        <span class="font-medium">View Model</span>
      </button>

      <!-- ProjectAura Logo (Center) -->
      <div class="absolute left-1/2 transform -translate-x-1/2">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-500 via-blue-400 via-purple-500 to-fuchsia-400 bg-clip-text text-transparent tracking-tight">
          ProjectAura
        </h1>
      </div>

      <!-- GitHub Button (Right) -->
      <button
        @click="$emit('go-to-github')"
        class="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/20 rounded-xl text-white/90 hover:text-white transition-all duration-200 backdrop-blur-sm group"
      >
        <Github class="w-4 h-4 group-hover:scale-110 transition-transform duration-200" />
        <span class="font-medium">Go to GitHub</span>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { Eye, Github } from 'lucide-vue-next';

defineEmits<{
  'view-model': []
  'go-to-github': []
}>();
</script>

<style scoped>
/* Effetto glow per il gradiente del logo */
h1 {
  filter: drop-shadow(0 0 10px rgba(168, 85, 247, 0.3));
}

/* Animazione subtile per i button */
button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
}

/* Gradiente animato per il logo */
@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

h1 {
  background-size: 200% 200%;
  animation: gradient-shift 6s ease-in-out infinite;
}
</style>