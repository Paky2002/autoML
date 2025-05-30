// File: FileUploaderPage.vue
<script lang="ts" setup>
import { ref } from 'vue';
import DatasetParserManager from '@/services/datasetProcessing/DatasetParserManager';
import type { DatasetDTO } from '@/services/datasetProcessing/types';
import DataTable from '../DataTable/DataTable.vue'; // Il tuo componente DataTable
import AutoGluonConfigForm from '../AutoGluonConfigForm/AutoGluonConfigForm.vue'; // Assicurati che il percorso sia corretto e includi .vue

const isLoading = ref<boolean>(false);
const fullResultDTO = ref<DatasetDTO | null>(null);
const uploaderErrorMessage = ref<string | null>(null);
const currentFile = ref<File | null>(null); // Per memorizzare il file caricato
const isAutoGluonTraining = ref<boolean>(false); // Stato per l'addestramento AutoGluon

const handleFileUpload = async (event: any) => {
    isLoading.value = true;
    fullResultDTO.value = null;
    uploaderErrorMessage.value = null;
    currentFile.value = null; // Resetta il file corrente ad ogni nuovo upload

    const inputElement = event.target as HTMLInputElement;
    const file = inputElement.files?.[0] || null;

    if (file) {
        currentFile.value = file; // Memorizza il riferimento al file
        console.log(`[FileUploaderPage] File selezionato: ${file.name}`);
        try {
            const result: DatasetDTO = await DatasetParserManager.parseDataset(file);
            console.log('[FileUploaderPage] DatasetDTO ricevuto:', result);
            fullResultDTO.value = result;
            uploaderErrorMessage.value = null;
        } catch (e: any) {
            uploaderErrorMessage.value = e.message || 'Errore imprevisto durante l\'elaborazione del file.';
            fullResultDTO.value = {
                success: false,
                fileName: file.name,
                data: null,
                error: uploaderErrorMessage.value
            };
        } finally {
            isLoading.value = false;
            // Non resettare inputElement.value qui se vuoi che il nome del file rimanga visibile
            // Se lo resetti, currentFile.value rimane valido ma l'input UI è pulito.
            // Per consistenza, è spesso meglio resettarlo:
            if (inputElement) {
                inputElement.value = '';
            }
        }
    } else {
        isLoading.value = false;
    }
};

const handleStartAutoGluonTraining = async (config: any) => {
    if (!currentFile.value) {
        uploaderErrorMessage.value = "Nessun file dataset selezionato per l'addestramento.";
        alert(uploaderErrorMessage.value);
        return;
    }
    if (!fullResultDTO.value || !fullResultDTO.value.success || !fullResultDTO.value.data || !fullResultDTO.value.data.headers || fullResultDTO.value.data.headers.length === 0) {
        uploaderErrorMessage.value = "Il dataset non è valido o gli header mancano. Impossibile avviare l'addestramento.";
        alert(uploaderErrorMessage.value);
        return;
    }

    isAutoGluonTraining.value = true;
    uploaderErrorMessage.value = null; // Pulisci errori precedenti
    console.log("Configurazione AutoGluon ricevuta per l'addestramento:", config);
    console.log("File da inviare al backend:", currentFile.value.name);

    const formData = new FormData();
    formData.append('file', currentFile.value); // Il file del dataset
    formData.append('config', JSON.stringify(config)); // La configurazione come stringa JSON

    try {
        // QUI VA LA TUA CHIAMATA API AL BACKEND FLASK
        // Esempio:
        // const response = await fetch('/api/train-autogluon', { // Sostituisci con il tuo endpoint Flask
        //   method: 'POST',
        //   body: formData,
        // });

        // if (!response.ok) {
        //   const errorData = await response.json().catch(() => ({ message: response.statusText }));
        //   throw new Error(`Errore dal server: ${errorData.message || response.statusText}`);
        // }
        // const result = await response.json();
        // console.log("Risultato addestramento:", result);
        // alert("Addestramento completato con successo!"); 

        // Simulazione di chiamata API per ora:
        await new Promise(resolve => setTimeout(resolve, 3000));
        console.log("Chiamata API (simulata) al backend per l'addestramento completata.");
        alert(`Addestramento (simulato) avviato con successo per il target: ${config.label}! Controlla la console del backend.`);

    } catch (error: any) {
        console.error("Errore durante l'avvio dell'addestramento AutoGluon:", error);
        uploaderErrorMessage.value = `Errore durante l'addestramento: ${error.message || 'Errore sconosciuto'}`;
        alert(uploaderErrorMessage.value);
    } finally {
        isAutoGluonTraining.value = false;
    }
};
</script>

<template>
    <div class="file-uploader-container p-4 md:p-8 space-y-6">
        <div class="bg-white shadow-md rounded-lg p-6">
            <h2 class="text-xl font-semibold text-gray-700 mb-4">Carica il Tuo Dataset</h2>
            <div class="p-field"> <label for="file-upload"
                    class="block text-sm font-medium text-gray-700 mb-1">Seleziona un file (CSV, Excel, etc.)</label>
                <input id="file-upload" type="file" @change="handleFileUpload"
                    :disabled="isLoading || isAutoGluonTraining"
                    class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 p-2.5" />
            </div>
        </div>

        <div v-if="isLoading" class="mt-4 p-4 text-sm text-blue-700 bg-blue-100 rounded-lg text-center">
            <p>Elaborazione del file in corso...</p>
        </div>

        <div v-if="uploaderErrorMessage"
            class="mt-4 p-4 text-sm text-red-700 bg-red-100 rounded-lg border border-red-300">
            <p><strong>Errore:</strong> {{ uploaderErrorMessage }}</p>
        </div>

        <div v-if="!isLoading && fullResultDTO" class="space-y-8">
            <div class="bg-white shadow-md rounded-lg p-0 md:p-2">
                <h3 class="text-lg font-medium text-gray-800 mb-1 px-4 pt-4 md:px-2 md:pt-2"
                    v-if="fullResultDTO.fileName">Anteprima Dati: {{ fullResultDTO.fileName }}</h3>
                <DataTable :datasetDTO="fullResultDTO" />
            </div>

            <div
                v-if="fullResultDTO.success && fullResultDTO.data && fullResultDTO.data.headers && fullResultDTO.data.headers.length > 0">
                <AutoGluonConfigForm :datasetHeaders="fullResultDTO.data.headers"
                    :isTrainingInProgress="isAutoGluonTraining" @start-training="handleStartAutoGluonTraining" />
            </div>
            <div v-else-if="fullResultDTO.success && fullResultDTO.data && (!fullResultDTO.data.headers || fullResultDTO.data.headers.length === 0)"
                class="mt-4 p-4 text-sm text-yellow-700 bg-yellow-100 rounded-lg border border-yellow-300">
                <p>Il dataset è stato caricato ma non è stato possibile estrarre gli header. Impossibile configurare
                    l'addestramento AutoGluon.</p>
            </div>
        </div>

        <div v-else-if="!isLoading && !fullResultDTO && !uploaderErrorMessage"
            class="mt-6 p-6 bg-white shadow-md rounded-lg text-center text-gray-500">
            <p>Nessun dato da visualizzare. Seleziona un file per iniziare.</p>
        </div>
    </div>
</template>