<template>
  <div class="bg-black/20 backdrop-blur-sm border border-white/10 rounded-2xl p-8">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-semibold text-white mb-2 flex items-center gap-3">
          <Code class="w-6 h-6" />
          API Integration Code
        </h2>
        <p class="text-white/70">Copy and use these code examples in your applications</p>
      </div>
    </div>

    <!-- Language Tabs -->
    <div class="flex gap-1 mb-6 bg-white/5 p-1 rounded-xl">
      <button
        v-for="lang in languages"
        :key="lang.id"
        @click="activeLanguage = lang.id"
        :class="[
          'flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200',
          activeLanguage === lang.id
            ? 'bg-white/15 text-white shadow-lg'
            : 'text-white/70 hover:text-white hover:bg-white/10'
        ]"
      >
        <component :is="lang.icon" class="w-4 h-4" />
        {{ lang.name }}
      </button>
    </div>

    <!-- Code Sections -->
    <div class="space-y-6">
      <!-- Single Prediction -->
      <div class="bg-white/5 rounded-xl border border-white/10 overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-white/10">
          <h3 class="text-white font-medium flex items-center gap-2">
            <Zap class="w-4 h-4" />
            Single Prediction
          </h3>
          <button
            @click="copyCode('single')"
            :class="[
              'flex items-center gap-2 px-3 py-1 rounded-lg text-sm transition-all duration-200',
              copiedCode === 'single'
                ? 'bg-green-500/20 text-green-300 border border-green-500/40'
                : 'bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-white/20'
            ]"
          >
            <component :is="copiedCode === 'single' ? Check : Copy" class="w-4 h-4" />
            {{ copiedCode === 'single' ? 'Copied!' : 'Copy' }}
          </button>
        </div>
        <div class="relative">
          <pre class="overflow-x-auto p-4 text-sm"><code :class="getLanguageClass()" v-html="highlightCode(getSinglePredictionCode())"></code></pre>
        </div>
      </div>

      <!-- Batch Prediction -->
      <div class="bg-white/5 rounded-xl border border-white/10 overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-white/10">
          <h3 class="text-white font-medium flex items-center gap-2">
            <Database class="w-4 h-4" />
            Batch Prediction
          </h3>
          <button
            @click="copyCode('batch')"
            :class="[
              'flex items-center gap-2 px-3 py-1 rounded-lg text-sm transition-all duration-200',
              copiedCode === 'batch'
                ? 'bg-green-500/20 text-green-300 border border-green-500/40'
                : 'bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-white/20'
            ]"
          >
            <component :is="copiedCode === 'batch' ? Check : Copy" class="w-4 h-4" />
            {{ copiedCode === 'batch' ? 'Copied!' : 'Copy' }}
          </button>
        </div>
        <div class="relative">
          <pre class="overflow-x-auto p-4 text-sm"><code :class="getLanguageClass()" v-html="highlightCode(getBatchPredictionCode())"></code></pre>
        </div>
      </div>

      <!-- Model Info -->
      <div class="bg-white/5 rounded-xl border border-white/10 overflow-hidden">
        <div class="flex items-center justify-between px-4 py-3 border-b border-white/10">
          <h3 class="text-white font-medium flex items-center gap-2">
            <Info class="w-4 h-4" />
            Get Model Information
          </h3>
          <button
            @click="copyCode('info')"
            :class="[
              'flex items-center gap-2 px-3 py-1 rounded-lg text-sm transition-all duration-200',
              copiedCode === 'info'
                ? 'bg-green-500/20 text-green-300 border border-green-500/40'
                : 'bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-white/20'
            ]"
          >
            <component :is="copiedCode === 'info' ? Check : Copy" class="w-4 h-4" />
            {{ copiedCode === 'info' ? 'Copied!' : 'Copy' }}
          </button>
        </div>
        <div class="relative">
          <pre class="overflow-x-auto p-4 text-sm"><code :class="getLanguageClass()" v-html="highlightCode(getModelInfoCode())"></code></pre>
        </div>
      </div>

      <!-- Configuration -->
      <div class="bg-blue-500/10 rounded-xl p-4 border border-blue-500/30">
        <h3 class="text-blue-200 font-medium mb-3 flex items-center gap-2">
          <Settings class="w-4 h-4" />
          Configuration
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <p class="text-blue-300/70 mb-1">Model UUID:</p>
            <code class="text-blue-200 bg-blue-500/20 px-2 py-1 rounded font-mono">{{ modelUuid }}</code>
          </div>
          <div>
            <p class="text-blue-300/70 mb-1">API Base URL:</p>
            <code class="text-blue-200 bg-blue-500/20 px-2 py-1 rounded font-mono">{{ apiBaseUrl }}</code>
          </div>
          <div>
            <p class="text-blue-300/70 mb-1">Target Feature:</p>
            <code class="text-blue-200 bg-blue-500/20 px-2 py-1 rounded font-mono">{{ targetFeature }}</code>
          </div>
          <div>
            <p class="text-blue-300/70 mb-1">Required Features:</p>
            <div class="space-y-1">
              <code 
                v-for="feature in requiredFeatures.slice(0, 3)" 
                :key="feature"
                class="block text-blue-200 bg-blue-500/20 px-2 py-1 rounded font-mono text-xs"
              >
                {{ feature }}
              </code>
              <span v-if="requiredFeatures.length > 3" class="text-blue-300/60 text-xs">
                +{{ requiredFeatures.length - 3 }} more...
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Usage Examples -->
      <div class="bg-yellow-500/10 rounded-xl p-4 border border-yellow-500/30">
        <h3 class="text-yellow-200 font-medium mb-3 flex items-center gap-2">
          <Lightbulb class="w-4 h-4" />
          Usage Tips
        </h3>
        <ul class="space-y-2 text-sm text-yellow-300/80">
          <li class="flex items-start gap-2">
            <span class="text-yellow-400 mt-0.5">•</span>
            <span>Ensure your input data has the exact same feature names as used during training</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-yellow-400 mt-0.5">•</span>
            <span>For batch predictions, use the CSV upload endpoint for better performance</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-yellow-400 mt-0.5">•</span>
            <span>Handle errors gracefully and check the response status before using predictions</span>
          </li>
          <li class="flex items-start gap-2">
            <span class="text-yellow-400 mt-0.5">•</span>
            <span>For classification models, check the probabilities array for confidence scores</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Code, Copy, Check, Zap, Database, Info, Settings, Lightbulb, ChevronDown } from 'lucide-vue-next';

// Proper icon components
const PythonIcon = {
  template: `
    <div class="flex items-center gap-1">
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none">
        <path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.2v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09-.33.22zM21.1 6.11l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.19V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08-.33.23z" fill="#306998"/>
        <path d="M21.1 6.11l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.04.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.25-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.19V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08-.33.23z" fill="#FFD43B"/>
      </svg>
      <span class="text-xs font-semibold text-yellow-400">Python</span>
    </div>
  `
};

const TypeScriptIcon = {
  template: `
    <div class="flex items-center gap-1">
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none">
        <rect x="1" y="1" width="22" height="22" rx="6" fill="#3178C6"/>
        <path d="M12.5 15.8V22h2.9v-6.2c.7 0 1.2.4 1.2 1.1V22h2.8v-5.4c0-2-.9-2.9-2.4-2.9-.9 0-1.6.4-2.1 1.1l-.1-1h-2.3zm-5.4-1.9h-2v2.3h-1.3v1.8h1.3V22h2.1v-4.8h1.5v-1.8h-1.5v-2.3z" fill="white"/>
        <path d="M15.9 10.5c0 .6-.4 1-1 1s-1-.4-1-1 .4-1 1-1 1 .4 1 1zM12.4 7.5c-.5 0-.9.2-1.3.4l.4.8c.2-.1.5-.2.8-.2s.6.1.8.2l.4-.8c-.4-.3-.8-.4-1.1-.4zM8.1 7.5c-.5 0-.9.2-1.3.4l.4.8c.2-.1.5-.2.8-.2s.6.1.8.2l.4-.8c-.4-.3-.8-.4-1.1-.4z" fill="white"/>
      </svg>
      <span class="text-xs font-semibold text-blue-400">TypeScript</span>
    </div>
  `
};

interface Props {
  modelUuid: string;
  targetFeature: string;
  requiredFeatures: string[];
}

const props = defineProps<Props>();

const activeLanguage = ref<'python' | 'typescript'>('python');
const copiedCode = ref<string | null>(null);
const openSection = ref<'single' | 'batch' | 'info'>('single');

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

const languages = [
  { id: 'python', name: 'Python', icon: PythonIcon },
  { id: 'typescript', name: 'TypeScript', icon: TypeScriptIcon }
];

const getLanguageClass = () => {
  return activeLanguage.value === 'python' ? 'language-python' : 'language-typescript';
};

const getLanguageIcon = () => {
  return activeLanguage.value === 'python' ? PythonIcon : TypeScriptIcon;
};

const toggleSection = (section: 'single' | 'batch' | 'info') => {
  openSection.value = openSection.value === section ? 'single' : section;
};

const getSinglePredictionCode = () => {
  if (activeLanguage.value === 'python') {
    return `import requests
import json

# Configuration
API_BASE_URL = "${apiBaseUrl}"
MODEL_UUID = "${props.modelUuid}"

def predict_single(data):
    """
    Make a single prediction using the trained model
    
    Args:
        data (dict): Dictionary with feature values
    
    Returns:
        dict: Prediction result
    """
    url = f"{API_BASE_URL}/api/predictions/{MODEL_UUID}/predict"
    
    payload = {
        "data": [data]  # API expects an array
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        if result["success"]:
            return {
                "prediction": result["predictions"][0],
                "probabilities": result.get("probabilities", [None])[0],
                "model_name": result["model_name"],
                "target_feature": result["target_feature"]
            }
        else:
            raise Exception(f"Prediction failed: {result['error']}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Sample input data (adjust features according to your model)
    sample_data = {${props.requiredFeatures.slice(0, 3).map(feature => `
        "${feature}": 1.0`).join(',')},
        # Add more features as needed...
    }
    
    try:
        result = predict_single(sample_data)
        print(f"Prediction: {result['prediction']}")
        print(f"Target: {result['target_feature']}")
        
        if result['probabilities']:
            print(f"Confidence: {max(result['probabilities']):.2%}")
            
    except Exception as e:
        print(f"Error: {e}")`;
  } else {
    return `interface PredictionData {
  [key: string]: number | string;
}

interface PredictionResult {
  success: boolean;
  predictions: any[];
  probabilities?: number[][];
  model_name: string;
  target_feature: string;
  error?: string;
}

class ModelPredictor {
  private apiBaseUrl: string;
  private modelUuid: string;

  constructor(apiBaseUrl = "${apiBaseUrl}", modelUuid = "${props.modelUuid}") {
    this.apiBaseUrl = apiBaseUrl;
    this.modelUuid = modelUuid;
  }

  /**
   * Make a single prediction using the trained model
   */
  async predictSingle(data: PredictionData): Promise<any> {
    const url = \`\${this.apiBaseUrl}/api/predictions/\${this.modelUuid}/predict\`;
    
    const payload = {
      data: [data] // API expects an array
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(\`HTTP error! status: \${response.status}\`);
      }

      const result: PredictionResult = await response.json();

      if (result.success) {
        return {
          prediction: result.predictions[0],
          probabilities: result.probabilities?.[0],
          modelName: result.model_name,
          targetFeature: result.target_feature
        };
      } else {
        throw new Error(\`Prediction failed: \${result.error}\`);
      }
    } catch (error) {
      throw new Error(\`API request failed: \${error instanceof Error ? error.message : 'Unknown error'}\`);
    }
  }
}

// Example usage
async function main() {
  const predictor = new ModelPredictor();
  
  // Sample input data (adjust features according to your model)
  const sampleData: PredictionData = {${props.requiredFeatures.slice(0, 3).map(feature => `
    "${feature}": 1.0`).join(',')},
    // Add more features as needed...
  };

  try {
    const result = await predictor.predictSingle(sampleData);
    console.log(\`Prediction: \${result.prediction}\`);
    console.log(\`Target: \${result.targetFeature}\`);
    
    if (result.probabilities) {
      const confidence = Math.max(...result.probabilities);
      console.log(\`Confidence: \${(confidence * 100).toFixed(1)}%\`);
    }
  } catch (error) {
    console.error(\`Error: \${error}\`);
  }
}

main();`;
  }
};

const getBatchPredictionCode = () => {
  if (activeLanguage.value === 'python') {
    return `import requests
import pandas as pd
import json

def predict_batch(data_list):
    """
    Make batch predictions using the trained model
    
    Args:
        data_list (list): List of dictionaries with feature values
    
    Returns:
        dict: Batch prediction results
    """
    url = f"{API_BASE_URL}/api/predictions/{MODEL_UUID}/predict/batch"
    
    payload = {
        "data": data_list
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        if result["success"]:
            return {
                "predictions": result["predictions"],
                "probabilities": result.get("probabilities"),
                "batch_info": result.get("batch_info"),
                "model_name": result["model_name"]
            }
        else:
            raise Exception(f"Batch prediction failed: {result['error']}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

def predict_from_csv(csv_file_path):
    """
    Make predictions from a CSV file
    
    Args:
        csv_file_path (str): Path to CSV file
    
    Returns:
        pd.DataFrame: DataFrame with predictions
    """
    url = f"{API_BASE_URL}/api/predictions/{MODEL_UUID}/predict/batch"
    
    try:
        with open(csv_file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            
            result = response.json()
            
            if result["success"]:
                # Load original CSV and add predictions
                df = pd.read_csv(csv_file_path)
                df['prediction'] = result["predictions"]
                
                if result.get("probabilities"):
                    # Add confidence scores for classification
                    confidences = [max(probs) if probs else None 
                                 for probs in result["probabilities"]]
                    df['confidence'] = confidences
                
                return df
            else:
                raise Exception(f"CSV prediction failed: {result['error']}")
                
    except Exception as e:
        raise Exception(f"CSV processing failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Method 1: Batch prediction with data list
    batch_data = [
        {${props.requiredFeatures.slice(0, 2).map(feature => `"${feature}": 1.0`).join(', ')}},
        {${props.requiredFeatures.slice(0, 2).map(feature => `"${feature}": 2.0`).join(', ')}},
        # Add more samples...
    ]
    
    try:
        result = predict_batch(batch_data)
        print(f"Batch predictions: {result['predictions']}")
        print(f"Total samples: {len(result['predictions'])}")
    except Exception as e:
        print(f"Batch prediction error: {e}")
    
    # Method 2: Prediction from CSV file
    try:
        df_with_predictions = predict_from_csv("test_data.csv")
        print(df_with_predictions.head())
        
        # Save results
        df_with_predictions.to_csv("predictions_output.csv", index=False)
    except Exception as e:
        print(f"CSV prediction error: {e}")`;
  } else {
    return `interface BatchPredictionResult {
  success: boolean;
  predictions: any[];
  probabilities?: number[][];
  batch_info?: {
    total_samples: number;
    processing_time?: number;
  };
  model_name: string;
  error?: string;
}

class BatchPredictor extends ModelPredictor {
  /**
   * Make batch predictions using the trained model
   */
  async predictBatch(dataList: PredictionData[]): Promise<any> {
    const url = \`\${this.apiBaseUrl}/api/predictions/\${this.modelUuid}/predict/batch\`;
    
    const payload = {
      data: dataList
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(\`HTTP error! status: \${response.status}\`);
      }

      const result: BatchPredictionResult = await response.json();

      if (result.success) {
        return {
          predictions: result.predictions,
          probabilities: result.probabilities,
          batchInfo: result.batch_info,
          modelName: result.model_name
        };
      } else {
        throw new Error(\`Batch prediction failed: \${result.error}\`);
      }
    } catch (error) {
      throw new Error(\`Batch API request failed: \${error instanceof Error ? error.message : 'Unknown error'}\`);
    }
  }

  /**
   * Make predictions from a CSV file
   */
  async predictFromCsv(csvFile: File): Promise<any> {
    const url = \`\${this.apiBaseUrl}/api/predictions/\${this.modelUuid}/predict/batch\`;
    
    const formData = new FormData();
    formData.append('file', csvFile);

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(\`HTTP error! status: \${response.status}\`);
      }

      const result: BatchPredictionResult = await response.json();

      if (result.success) {
        return {
          predictions: result.predictions,
          probabilities: result.probabilities,
          batchInfo: result.batch_info,
          modelName: result.model_name
        };
      } else {
        throw new Error(\`CSV prediction failed: \${result.error}\`);
      }
    } catch (error) {
      throw new Error(\`CSV processing failed: \${error instanceof Error ? error.message : 'Unknown error'}\`);
    }
  }
}

// Example usage
async function batchExample() {
  const predictor = new BatchPredictor();
  
  // Method 1: Batch prediction with data array
  const batchData: PredictionData[] = [
    {${props.requiredFeatures.slice(0, 2).map(feature => `"${feature}": 1.0`).join(', ')}},
    {${props.requiredFeatures.slice(0, 2).map(feature => `"${feature}": 2.0`).join(', ')}},
    // Add more samples...
  ];

  try {
    const result = await predictor.predictBatch(batchData);
    console.log(\`Batch predictions: \${result.predictions}\`);
    console.log(\`Total samples: \${result.predictions.length}\`);
  } catch (error) {
    console.error(\`Batch prediction error: \${error}\`);
  }

  // Method 2: Prediction from CSV file (in browser)
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = '.csv';
  
  fileInput.onchange = async (event) => {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      try {
        const result = await predictor.predictFromCsv(file);
        console.log('CSV predictions:', result.predictions);
        
        // Download results as JSON
        const dataStr = JSON.stringify(result, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'predictions.json';
        link.click();
      } catch (error) {
        console.error(\`CSV prediction error: \${error}\`);
      }
    }
  };
}

batchExample();`;
  }
};

const getModelInfoCode = () => {
  if (activeLanguage.value === 'python') {
    return `def get_model_info():
    """
    Get detailed information about the trained model
    
    Returns:
        dict: Model information and metadata
    """
    url = f"{API_BASE_URL}/api/models/{MODEL_UUID}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        result = response.json()
        
        if result["success"]:
            model_info = result["model"]
            return {
                "name": model_info["name"],
                "status": model_info["status"],
                "problem_type": model_info["problem_type"],
                "target_feature": model_info["target_feature"],
                "best_score": model_info.get("best_score"),
                "feature_columns": model_info.get("feature_columns", []),
                "created_at": model_info["created_at"],
                "training_config": {
                    "time_limit": model_info["time_limit"],
                    "presets": model_info["presets"],
                    "eval_metric": model_info["eval_metric"]
                }
            }
        else:
            raise Exception(f"Failed to get model info: {result['error']}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

def get_prediction_sample():
    """
    Get a sample of the expected input format for predictions
    
    Returns:
        dict: Sample request format
    """
    url = f"{API_BASE_URL}/api/predictions/{MODEL_UUID}/predict/sample"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        result = response.json()
        
        if result["success"]:
            return {
                "required_features": result["required_features"],
                "sample_request": result["sample_request"],
                "target_feature": result["target_feature"]
            }
        else:
            raise Exception(f"Failed to get sample: {result['error']}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Get model information
        model_info = get_model_info()
        print("Model Information:")
        print(f"  Name: {model_info['name']}")
        print(f"  Status: {model_info['status']}")
        print(f"  Problem Type: {model_info['problem_type']}")
        print(f"  Best Score: {model_info['best_score']}")
        print(f"  Features: {len(model_info['feature_columns'])} total")
        
        # Get prediction sample format
        sample_info = get_prediction_sample()
        print("\\nRequired Features:")
        for feature in sample_info['required_features']:
            print(f"  - {feature}")
            
    except Exception as e:
        print(f"Error: {e}")`;
  } else {
    return `interface ModelInfo {
  success: boolean;
  model: {
    name: string;
    status: string;
    problem_type: string;
    target_feature: string;
    best_score?: number;
    feature_columns?: string[];
    created_at: string;
    time_limit: number;
    presets?: string;
    eval_metric?: string;
  };
}

interface PredictionSample {
  success: boolean;
  required_features: string[];
  sample_request: any;
  target_feature: string;
}

class ModelInfoService {
  private apiBaseUrl: string;
  private modelUuid: string;

  constructor(apiBaseUrl = "${apiBaseUrl}", modelUuid = "${props.modelUuid}") {
    this.apiBaseUrl = apiBaseUrl;
    this.modelUuid = modelUuid;
  }

  /**
   * Get detailed information about the trained model
   */
  async getModelInfo(): Promise<any> {
    const url = \`\${this.apiBaseUrl}/api/models/\${this.modelUuid}\`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(\`HTTP error! status: \${response.status}\`);
      }

      const result: ModelInfo = await response.json();

      if (result.success) {
        const model = result.model;
        return {
          name: model.name,
          status: model.status,
          problemType: model.problem_type,
          targetFeature: model.target_feature,
          bestScore: model.best_score,
          featureColumns: model.feature_columns || [],
          createdAt: model.created_at,
          trainingConfig: {
            timeLimit: model.time_limit,
            presets: model.presets,
            evalMetric: model.eval_metric
          }
        };
      } else {
        throw new Error('Failed to get model info');
      }
    } catch (error) {
      throw new Error(\`API request failed: \${error instanceof Error ? error.message : 'Unknown error'}\`);
    }
  }

  /**
   * Get a sample of the expected input format for predictions
   */
  async getPredictionSample(): Promise<any> {
    const url = \`\${this.apiBaseUrl}/api/predictions/\${this.modelUuid}/predict/sample\`;

    try {
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(\`HTTP error! status: \${response.status}\`);
      }

      const result: PredictionSample = await response.json();

      if (result.success) {
        return {
          requiredFeatures: result.required_features,
          sampleRequest: result.sample_request,
          targetFeature: result.target_feature
        };
      } else {
        throw new Error('Failed to get prediction sample');
      }
    } catch (error) {
      throw new Error(\`API request failed: \${error instanceof Error ? error.message : 'Unknown error'}\`);
    }
  }
}

// Example usage
async function modelInfoExample() {
  const infoService = new ModelInfoService();

  try {
    // Get model information
    const modelInfo = await infoService.getModelInfo();
    console.log('Model Information:');
    console.log(\`  Name: \${modelInfo.name}\`);
    console.log(\`  Status: \${modelInfo.status}\`);
    console.log(\`  Problem Type: \${modelInfo.problemType}\`);
    console.log(\`  Best Score: \${modelInfo.bestScore}\`);
    console.log(\`  Features: \${modelInfo.featureColumns.length} total\`);

    // Get prediction sample format
    const sampleInfo = await infoService.getPredictionSample();
    console.log('\\nRequired Features:');
    sampleInfo.requiredFeatures.forEach((feature: string) => {
      console.log(\`  - \${feature}\`);
    });

  } catch (error) {
    console.error(\`Error: \${error}\`);
  }
}

modelInfoExample();`;
  }
};

const highlightCode = (code: string): string => {
  // Basic syntax highlighting
  return code
    .replace(/(".*?")/g, '<span style="color: #a3e635;">$1</span>') // strings
    .replace(/\b(import|from|def|class|if|else|try|except|return|async|await|function|const|let|var|interface|type)\b/g, '<span style="color: #8b5cf6;">$1</span>') // keywords
    .replace(/\b(True|False|None|null|undefined)\b/g, '<span style="color: #f59e0b;">$1</span>') // constants
    .replace(/(#.*$)/gm, '<span style="color: #6b7280;">$1</span>') // comments
    .replace(/(\/\/.*$)/gm, '<span style="color: #6b7280;">$1</span>') // comments
    .replace(/\b(\d+\.?\d*)\b/g, '<span style="color: #06b6d4;">$1</span>'); // numbers
};

const copyCode = async (type: 'single' | 'batch' | 'info') => {
  let code = '';
  
  switch (type) {
    case 'single':
      code = getSinglePredictionCode();
      break;
    case 'batch':
      code = getBatchPredictionCode();
      break;
    case 'info':
      code = getModelInfoCode();
      break;
  }
  
  try {
    await navigator.clipboard.writeText(code);
    copiedCode.value = type;
    setTimeout(() => {
      copiedCode.value = null;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy code:', err);
  }
};
</script>

<style scoped>
/* Code styling */
pre {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
  line-height: 1.5;
}

code {
  color: #e5e7eb;
  font-size: 13px;
}

/* Scrollbar for code blocks */
pre::-webkit-scrollbar {
  height: 8px;
}

pre::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

pre::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

pre::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Tab animations */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}
</style>