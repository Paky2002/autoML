// src/services/datasetProcessing/strategies/CsvParsingStrategy.ts

import Papa from 'papaparse';
import type { ParsingStrategy, DatasetDTO, ParsedData } from '../types';

export const CsvParsingStrategy: ParsingStrategy = {
  async parse(fileInput: File): Promise<DatasetDTO> {
    return new Promise((resolve) => {
      Papa.parse<Record<string, any>>(fileInput, {
        header: true,
        skipEmptyLines: true,
        dynamicTyping: true,
        complete: (results: Papa.ParseResult<Record<string, any>>) => {
          if (results.errors && results.errors.length > 0) {
            const errorMessages: string = results.errors.map((err: Papa.ParseError) => {
              let msg: string = err.message;
              if (err.row !== undefined) msg += ` (riga file: ${err.row + 2})`;
              return msg;
            }).join('; ');
            resolve({
              success: false,
              fileName: fileInput.name,
              data: null,
              error: `Errori nel parsing del CSV: ${errorMessages}`
            });
            return;
          }

          if (!results.data) {
             resolve({
              success: false,
              fileName: fileInput.name,
              data: null,
              error: 'Risultato del parsing non valido (results.data è undefined).'
            });
            return;
          }

          const headers: string[] = results.meta.fields || [];
          
          if (headers.length === 0 && results.data.length > 0 && results.data.some(r => Object.keys(r).length > 0)) {
             resolve({
                success: false,
                fileName: fileInput.name,
                data: null,
                error: 'Impossibile determinare gli header del CSV, ma sono presenti dati. Controlla la prima riga del file.'
            });
            return;
          }
          
          if (headers.length === 0 && results.data.length === 0) {
             resolve({
                success: true,
                fileName: fileInput.name,
                data: { headers: [], rows: [], totalRows: 0 },
                error: null
            });
            return;
          }

          const rows: any[][] = results.data.map((rowObject: Record<string, any>) => {
            return headers.map(header => (rowObject[header] !== undefined ? rowObject[header] : null));
          });
          
          const parsedData: ParsedData = { headers, rows, totalRows: results.data.length };
          
          resolve({
            success: true,
            fileName: fileInput.name,
            data: parsedData,
            error: null
          });
        },
        error: (error: Error) => {
          console.error('Errore Papa Parse:', error, 'File processato:', fileInput.name);
          resolve({
            success: false,
            fileName: fileInput.name, 
            data: null,
            error: `Errore critico durante il parsing del CSV: ${error.message}`
          });
        }
      });
    });
  }
};