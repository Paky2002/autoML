import * as XLSX from 'xlsx';
import type { ParsingStrategy, DatasetDTO, ParsedData } from '../types';

// Applica esplicitamente l'interfaccia ParsingStrategy
export const ExcelParsingStrategy: ParsingStrategy = {
  async parse(file: File): Promise<DatasetDTO> {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (event: ProgressEvent<FileReader>) => {
        try {
          if (!(event.target?.result instanceof ArrayBuffer)) {
            throw new Error('Impossibile leggere il file Excel come ArrayBuffer.');
          }
          const data = event.target.result;
          const workbook: XLSX.WorkBook = XLSX.read(data, { type: 'array' });
          
          const sheetName = workbook.SheetNames[0];
          if (!sheetName) {
            throw new Error('Il file Excel non contiene fogli.');
          }
          const worksheet: XLSX.WorkSheet = workbook.Sheets[sheetName];
          
          const jsonData: any[][] = XLSX.utils.sheet_to_json(worksheet, { header: 1, blankrows: false });

          if (!jsonData || jsonData.length === 0) {
            resolve({
              success: true,
              fileName: file.name,
              data: { headers: [], rows: [], totalRows: 0 },
              error: null
            });
            return;
          }

          const headers: string[] = (jsonData[0] as any[])?.map(String) || [];
          const dataRowsRaw = jsonData.slice(1); 
          
          const rows: any[][] = dataRowsRaw.map(rowArray => 
            headers.map((_, idx) => (rowArray[idx] !== undefined && rowArray[idx] !== null ? rowArray[idx] : null))
          );
          const parsedData: ParsedData = { headers, rows, totalRows: rows.length };
          
          resolve({
            success: true,
            fileName: file.name,
            data: parsedData,
            error: null
          });

        } catch (e: any) {
          console.error("Errore parsing Excel:", e);
          resolve({
            success: false,
            fileName: file.name,
            data: null,
            error: `Errore durante il parsing del file Excel: ${e.message}`
          });
        }
      };
      reader.onerror = () => {
        resolve({
          success: false,
          fileName: file.name,
          data: null,
          error: `Errore nella lettura del file Excel: ${reader.error?.message || 'Errore sconosciuto'}`
        });
      };
      reader.readAsArrayBuffer(file);
    });
  }
};