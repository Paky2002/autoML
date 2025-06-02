// csvParser.worker.ts
import Papa from 'papaparse';

// Definisci i tipi inline per evitare problemi di import
interface DatasetDTO {
  filename: string;
  headers: string[];
  rows: any[][];
  totalRows: number;
  fileSize: number;
  columns: ColumnInfo[];
  preview: any[];
}

interface ColumnInfo {
  name: string;
  type: 'numeric' | 'categorical' | 'datetime' | 'text';
  nullCount: number;
  uniqueCount: number;
  sampleValues: any[];
}

self.onmessage = function(event) {
  console.log("Worker: Message received from main script");

  const { file, filename } = event.data;
  
  const updateProgress = (stage: string, percentage: number) => {
    self.postMessage({
      type: 'progress',
      data: { stage, percentage }
    });
  };

  try {
    updateProgress('parsing', 10);
    
    Papa.parse(file, {
      header: false,
      skipEmptyLines: true,
      complete: (results: any) => {
        try {
          updateProgress('analyzing', 50);
          
          const rawData = results.data as any[][];
          if (!rawData || rawData.length === 0) {
            throw new Error('No data found in CSV file');
          }
          
          const headers = rawData[0] as string[];
          const rows = rawData.slice(1);
          
          updateProgress('analyzing', 70);
          
          // Analyze columns
          const columns: ColumnInfo[] = headers.map((header, index) => {
            const columnData = rows
              .map(row => row[index])
              .filter(val => val !== null && val !== undefined && val !== '');
            
            const uniqueValues = new Set(columnData);
            const numericValues = columnData.filter(val => !isNaN(Number(val)));
            
            let type: ColumnInfo['type'] = 'text';
            if (numericValues.length > columnData.length * 0.8) {
              type = 'numeric';
            } else if (uniqueValues.size < columnData.length * 0.1) {
              type = 'categorical';
            }
            
            return {
              name: header,
              type,
              nullCount: rows.length - columnData.length,
              uniqueCount: uniqueValues.size,
              sampleValues: Array.from(uniqueValues).slice(0, 5)
            };
          });
          
          updateProgress('complete', 90);
          
          const dataset: DatasetDTO = {
            filename,
            headers,
            rows: rows.slice(0, 50),
            totalRows: rows.length,
            fileSize: file.size,
            columns,
            preview: rows.slice(0, 10).map(row => {
              const obj: any = {};
              headers.forEach((header, index) => {
                obj[header] = row[index];
              });
              return obj;
            })
          };
          
          updateProgress('complete', 100);
          
          self.postMessage({
            type: 'success',
            data: dataset
          });
        } catch (analysisError) {
          self.postMessage({
            type: 'error',
            data: analysisError instanceof Error ? analysisError.message : 'Analysis failed'
          });
        }
      },
      error: (parseError: any) => {
        self.postMessage({
          type: 'error',
          data: parseError?.message || 'Failed to parse CSV'
        });
      }
    });
  } catch (error) {
    self.postMessage({
      type: 'error',
      data: error instanceof Error ? error.message : 'Unknown error occurred'
    });
  }
};

// Evita errori se il modulo viene importato direttamente
export {};