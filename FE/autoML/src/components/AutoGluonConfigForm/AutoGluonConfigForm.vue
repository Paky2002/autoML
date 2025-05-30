// src/components/AutoGluonConfigForm.vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue';

// Props
const props = defineProps<{
    datasetHeaders: string[]; // Array degli header del dataset caricato
    isTrainingInProgress: boolean; // Per disabilitare il form durante l'addestramento
}>();

// Emits
const emit = defineEmits(['start-training']);

// --- Stato Reattivo per gli Input del Form ---
const selectedTargetColumn = ref<string | null>(null);
const selectedProblemType = ref<string | null>(null); // 'binary', 'multiclass', 'regression'
const selectedEvalMetric = ref<string | null>(null); // Opzionale, AutoGluon sceglie un default
const trainingTimeLimit = ref<number>(3600); // Default: 1 ora (in secondi)
const selectedPreset = ref<string>('medium_quality'); // Default: 'medium_quality'

// --- Opzioni per i Dropdown (Computed e Ref) ---
const targetColumnOptions = computed(() => {
    if (!props.datasetHeaders) return [];
    return props.datasetHeaders.map(header => ({ label: header, value: header }));
});

const problemTypeOptions = ref([
    { label: 'Classificazione Binaria (es. Sì/No)', value: 'binary' },
    { label: 'Classificazione Multi-classe (es. Categoria A, B, C)', value: 'multiclass' },
    { label: 'Regressione (Prevedere un valore numerico)', value: 'regression' },
]);

const evaluationMetricsOptions = computed(() => {
    // Le metriche qui sono esempi comuni; AutoGluon ne supporta molte altre
    // Se selectedEvalMetric rimane null, AutoGluon usa la sua metrica di default per il tipo di problema
    if (!selectedProblemType.value) return [];
    switch (selectedProblemType.value) {
        case 'binary':
            return [
                { label: 'Accuracy', value: 'accuracy' },
                { label: 'AUC (Area Under ROC Curve)', value: 'roc_auc' },
                { label: 'F1 Score', value: 'f1' },
                { label: 'Precision', value: 'precision' },
                { label: 'Recall', value: 'recall' },
            ];
        case 'multiclass':
            return [
                { label: 'Accuracy', value: 'accuracy' },
                { label: 'F1 Macro', value: 'f1_macro' },
                { label: 'F1 Micro', value: 'f1_micro' },
                // { label: 'Log Loss', value: 'log_loss' }, // AutoGluon potrebbe non esporla direttamente come scelta primaria ma la usa
            ];
        case 'regression':
            return [
                { label: 'Root Mean Squared Error (RMSE)', value: 'root_mean_squared_error' },
                { label: 'Mean Absolute Error (MAE)', value: 'mean_absolute_error' },
                { label: 'R-squared (R2)', value: 'r2' },
            ];
        default:
            return [];
    }
});

const presetOptions = ref([
    { label: 'Migliore Qualità (Addestramento più lungo)', value: 'best_quality' },
    { label: 'Alta Qualità', value: 'high_quality' },
    { label: 'Buona Qualità (Bilanciato)', value: 'good_quality' },
    { label: 'Media Qualità (Default, buon bilanciamento)', value: 'medium_quality' },
    { label: 'Ottimizza per Deployment (Più veloce, può sacrificare qualità)', value: 'optimize_for_deployment' },
]);

// --- Watcher per resettare la metrica se cambia il tipo di problema ---
watch(selectedProblemType, () => {
    selectedEvalMetric.value = null; // Resetta la metrica, l'utente può riselezionare o lasciare Auto
});

// --- Validazione del Form (semplice) ---
const isFormValid = computed(() => {
    return selectedTargetColumn.value !== null &&
        selectedProblemType.value !== null &&
        trainingTimeLimit.value !== null && trainingTimeLimit.value >= 60; // Esempio: tempo minimo 60s
});

// --- Metodo per Inviare il Form ---
const handleSubmit = () => {
    if (!isFormValid.value) {
        // Potresti mostrare un avviso più elaborato
        alert("Per favore, compila tutti i campi richiesti correttamente.");
        return;
    }
    const trainingConfig = {
        label: selectedTargetColumn.value,
        problem_type: selectedProblemType.value,
        eval_metric: selectedEvalMetric.value, // Può essere null, AutoGluon sceglierà il default
        time_limit: trainingTimeLimit.value,
        presets: selectedPreset.value,
    };
    emit('start-training', trainingConfig);
};

// Funzione per resettare il form, può essere esposta al genitore se necessario
const resetForm = () => {
    selectedTargetColumn.value = null;
    selectedProblemType.value = null;
    selectedEvalMetric.value = null;
    trainingTimeLimit.value = 3600;
    selectedPreset.value = 'medium_quality';
};
defineExpose({ resetForm });

</script>

<template>
    <div class="p-6 md:p-8 bg-white shadow-xl rounded-lg w-full max-w-2xl mx-auto">
        <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b pb-3">
            Configura Addestramento AutoGluon
        </h2>

        <form @submit.prevent="handleSubmit" class="space-y-6">

            <div class="partial-section">
                <label for="target-column" class="block text-sm font-medium text-gray-700 mb-1">
                    Colonna Target (Variabile da predire) <span class="text-red-500">*</span>
                </label>
                <select id="target-column" v-model="selectedTargetColumn"
                    class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    :disabled="props.isTrainingInProgress">
                    <option disabled :value="null">-- Seleziona la colonna target --</option>
                    <option v-for="opt in targetColumnOptions" :key="opt.value" :value="opt.value">
                        {{ opt.label }}
                    </option>
                </select>
            </div>

            <div class="partial-section">
                <label for="problem-type" class="block text-sm font-medium text-gray-700 mb-1">
                    Tipo di Problema <span class="text-red-500">*</span>
                </label>
                <select id="problem-type" v-model="selectedProblemType"
                    class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    :disabled="props.isTrainingInProgress">
                    <option disabled :value="null">-- Seleziona il tipo di problema --</option>
                    <option v-for="opt in problemTypeOptions" :key="opt.value" :value="opt.value">
                        {{ opt.label }}
                    </option>
                </select>
            </div>

            <div v-if="selectedProblemType" class="partial-section">
                <label for="eval-metric" class="block text-sm font-medium text-gray-700 mb-1">
                    Metrica di Valutazione (Opzionale - AutoGluon sceglierà un default)
                </label>
                <select id="eval-metric" v-model="selectedEvalMetric"
                    class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    :disabled="props.isTrainingInProgress || evaluationMetricsOptions.length === 0">
                    <option :value="null">-- Auto (Default per tipo di problema) --</option>
                    <option v-for="opt in evaluationMetricsOptions" :key="opt.value" :value="opt.value">
                        {{ opt.label }}
                    </option>
                </select>
            </div>

            <fieldset class="partial-section border border-gray-300 p-4 rounded-md">
                <legend class="text-base font-medium text-gray-800 px-2">Impostazioni Addestramento</legend>
                <div class="space-y-4 md:space-y-0 md:grid md:grid-cols-2 md:gap-6 mt-2">
                    <div>
                        <label for="time-limit" class="block text-sm font-medium text-gray-700 mb-1">
                            Limite di Tempo (secondi) <span class="text-red-500">*</span>
                        </label>
                        <input type="number" id="time-limit" v-model.number="trainingTimeLimit" min="60"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                            :disabled="props.isTrainingInProgress" />
                    </div>
                    <div>
                        <label for="preset" class="block text-sm font-medium text-gray-700 mb-1">
                            Preset di Qualità
                        </label>
                        <select id="preset" v-model="selectedPreset"
                            class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                            :disabled="props.isTrainingInProgress">
                            <option v-for="opt in presetOptions" :key="opt.value" :value="opt.value">
                                {{ opt.label }}
                            </option>
                        </select>
                    </div>
                </div>
            </fieldset>

            <div class="pt-4">
                <button type="submit" :disabled="!isFormValid || props.isTrainingInProgress"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2"
                    :class="(!isFormValid || props.isTrainingInProgress) ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500'">
                    {{ props.isTrainingInProgress ? 'Addestramento in corso...' : 'Avvia Addestramento' }}
                </button>
            </div>
        </form>
    </div>
</template>

<style scoped>
/* Eventuali stili specifici del componente, se Tailwind non basta. 
   Per ora, Tailwind dovrebbe essere sufficiente. */
.partial-section {
    /* Puoi aggiungere stili comuni ai partials qui se necessario, 
     ma le classi di utilità di Tailwind sono preferibili direttamente nel template. */
}
</style>