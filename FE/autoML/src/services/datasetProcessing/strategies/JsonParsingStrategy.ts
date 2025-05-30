import type { ParsingStrategy, DatasetDTO, ParsedData } from '../types';

// Applica esplicitamente l'interfaccia ParsingStrategy
export const JsonParsingStrategy: ParsingStrategy = {
  async parse(file: File): Promise<DatasetDTO> {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (event: ProgressEvent<FileReader>) => {
        try {
          if (!event.target?.result || typeof event.target.result !== 'string') {
            throw new Error('Impossibile leggere il contenuto del file JSON.');
          }
          const jsonData: any[] = JSON.parse(event.target.result);

          if (!Array.isArray(jsonData)) {
            throw new Error('Il JSON non è un array. Necessario un array di oggetti.');
          }
          if (jsonData.length === 0) {
            resolve({
              success: true,
              fileName: file.name,
              data: { headers: [], rows: [], totalRows: 0 },
              error: null
            });
            return;
          }
          
          const firstItem = jsonData[0];
          if (typeof firstItem !== 'object' || firstItem === null) {
            throw new Error('Gli elementi dell\'array JSON non sono oggetti.');
          }

          const headers = Object.keys(firstItem);
          if (headers.length === 0 && jsonData.length > 0) {
             throw new Error('Oggetti JSON vuoti o impossibile determinare gli header.');
          }

          const rows: any[][] = jsonData.map((obj: Record<string, any>) => headers.map(header => obj[header]));
          const parsedData: ParsedData = { headers, rows, totalRows: jsonData.length };

          resolve({
            success: true,
            fileName: file.name,
            data: parsedData,
            error: null
          });
        } catch (e: any) {
          resolve({
            success: false,
            fileName: file.name,
            data: null,
            error: `Errore durante il parsing del JSON: ${e.message}`
          });
        }
      };
      reader.onerror = () => { // L'evento di errore non ha un target.result specifico per il contenuto
        resolve({
          success: false,
          fileName: file.name,
          data: null,
          error: `Errore nella lettura del file JSON: ${reader.error?.message || 'Errore sconosciuto'}`
        });
      };
      reader.readAsText(file);
    });
  }
};