// File: SimpleDataDisplayTable.vue
<script setup lang="ts">
import { computed } from 'vue';
import type { DatasetDTO } from '@/services/datasetProcessing/types';

const props = defineProps<{
    datasetDTO: DatasetDTO;
}>();

const currentTableHeaders = computed(() => {
    return props.datasetDTO.data?.headers || [];
});

const currentTableRows = computed(() => {
    if (props.datasetDTO && props.datasetDTO.data && Array.isArray(props.datasetDTO.data.rows)) {
        return props.datasetDTO.data.rows.slice(0, 50);
    }
    return [];
});
</script>
<template>
    <div class="flex justify-center items-start min-h-screen py-8 px-4">
        <div v-if="props.datasetDTO" class="w-full max-w-screen-xl">
            <div v-if="props.datasetDTO.success && props.datasetDTO.data && currentTableHeaders.length > 0">
                <p v-if="props.datasetDTO.fileName" class="mb-2 text-lg font-semibold">
                    File: <strong>{{ props.datasetDTO.fileName }}</strong>
                </p>
                <p v-if="props.datasetDTO.data.totalRows !== undefined" class="mb-4 text-sm text-gray-600">
                    Righe totali nel file: <strong>{{ props.datasetDTO.data.totalRows }}</strong>
                    (Visualizzate: {{ currentTableRows.length }})
                </p>

                <div class="overflow-x-auto overflow-y-auto shadow-md rounded-lg max-h-[50vh]">
                    <table class="min-w-full w-full text-sm text-left text-gray-500">
                        <thead class="text-xs text-gray-700 uppercase bg-gray-100 sticky top-0 z-10">
                            <tr>
                                <th v-for="(header, index) in currentTableHeaders" :key="`header-${index}`" scope="col"
                                    class="px-6 py-3 whitespace-nowrap">
                                    {{ header }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(row, rowIndex) in currentTableRows" :key="`row-${rowIndex}`"
                                class="bg-white border-b hover:bg-gray-50">
                                <td v-for="(cell, cellIndex) in row" :key="`cell-${rowIndex}-${cellIndex}`"
                                    class="px-6 py-4 whitespace-nowrap">
                                    {{ cell }}
                                </td>
                            </tr>
                            <tr v-if="currentTableRows.length === 0">
                                <td :colspan="currentTableHeaders.length" class="px-6 py-4 text-center text-gray-500">
                                    Nessuna riga di dati da visualizzare (le prime 50 sono vuote o non presenti).
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div v-else-if="props.datasetDTO.success === false && props.datasetDTO.error"
                class="mt-4 p-4 text-sm text-red-700 bg-red-100 rounded-lg border border-red-300">
                <p><strong>Errore nel caricamento del dataset:</strong> {{ props.datasetDTO.error }}</p>
            </div>
            <div v-else-if="props.datasetDTO.data && currentTableHeaders.length === 0"
                class="mt-4 p-4 text-sm text-yellow-700 bg-yellow-100 rounded-lg border border-yellow-300">
                <p>Il file è stato processato ma gli header non sono validi o mancanti.</p>
            </div>
            <div v-else class="mt-4 p-4 text-sm text-gray-700 bg-gray-100 rounded-lg border border-gray-300">
                <p>Nessun dato specifico da visualizzare o stato imprevisto per il file caricato.</p>
            </div>
        </div>
        <div v-else class="mt-8 p-4 text-sm text-gray-700 bg-gray-100 rounded-lg shadow-md">
            <p>Nessun dataset caricato. Seleziona un file per iniziare.</p>
        </div>
    </div>
</template>

<style scoped>
/* Stili base per la tabella, personalizzali come preferisci */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

th,
td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f2f2f2;
    font-weight: bold;
}

.p-message {
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
}

.p-message-error {
    border: 1px solid #ff7979;
    background-color: #ffe3e3;
    color: #c0392b;
}

.p-mt-2 {
    margin-top: 0.5rem;
}
</style>