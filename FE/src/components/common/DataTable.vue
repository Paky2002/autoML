<template>
  <div class="rounded-2xl overflow-hidden max-h-screen p-[40px] flex flex-col bg-black/20 backdrop-blur-sm">
    <div class="px-2 py-4 border-b border-white/20">
      <h3 class="text-xl font-semibold text-white">Dataset Preview</h3>
      <p class="text-sm text-white/70 mt-1">
        Showing first {{ displayRows.length }} of {{ totalRows }} rows
      </p>
    </div>
    
    <div class="overflow-y-auto flex-grow rounded-2xl mt-4 scrollbar-dark">
      <table class="min-w-full divide-y divide-white/10">
        <thead class="sticky top-0 z-10 bg-black/40 backdrop-blur-md">
          <tr>
            <th
              v-for="header in headers"
              :key="header"
              class="px-6 py-4 text-left text-xs font-semibold text-white/90 uppercase tracking-wider border-b border-white/20"
            >
              {{ header }}
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-white/5">
          <tr
            v-for="(row, index) in displayRows"
            :key="index"
            :class="[
              'transition-all duration-200 hover:bg-white/5',
              index % 2 === 0 ? 'bg-white/2' : 'bg-transparent'
            ]"
          >
            <td
              v-for="(cell, cellIndex) in row"
              :key="cellIndex"
              class="px-6 py-4 whitespace-nowrap text-sm text-white/80 border-r border-white/5 last:border-r-0"
            >
              <span class="font-mono">{{ formatCell(cell) }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  headers: string[];
  previewRows: any[][]; // Cambiato da 'rows' a 'previewRows' per chiarezza
  totalRows: number;
  maxRows?: number;
}

const props = withDefaults(defineProps<Props>(), {
  maxRows: 50
});

// Usa previewRows invece di rows per la visualizzazione
const displayRows = computed(() => 
  props.previewRows.slice(0, props.maxRows)
);

const formatCell = (cell: any): string => {
  if (cell === null || cell === undefined) return '';
  if (typeof cell === 'number') return cell.toLocaleString();
  return String(cell);
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
</style>