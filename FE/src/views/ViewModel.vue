<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">View Models</h1>
        <p class="text-gray-600">Manage and view your trained models</p>
        
        <div class="mt-12 p-8 bg-white rounded-2xl border border-gray-200">
          <div class="w-16 h-16 bg-gray-100 rounded-full mx-auto mb-4 flex items-center justify-center">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No models yet</h3>
          <p class="text-gray-500 mb-6">Train your first model to see it here</p>
          <router-link
            to="/train"
            class="inline-flex items-center px-6 py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-gray-800 transition-colors"
          >
            Start Training
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// This will be expanded later with actual model management functionality
</script>