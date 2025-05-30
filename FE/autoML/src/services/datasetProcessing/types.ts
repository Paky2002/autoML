// src/services/datasetProcessing/types.ts

export interface ParsedData {
  headers: string[];
  rows: any[][];
  totalRows: number;
}

export interface DatasetDTO {
  success: boolean;
  fileName: string | null;
  data: ParsedData | null;
  error: string | null;
}

export interface ParsingStrategy { 
  parse(file: File): Promise<DatasetDTO>;
}