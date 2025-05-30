// src/services/datasetProcessing/DatasetParserManager.ts
import { CsvParsingStrategy } from './strategies/CsvParsingStrategy';
import { JsonParsingStrategy } from './strategies/JsonParsingStrategy';
import { ExcelParsingStrategy } from './strategies/ExcelParsingStrategy';
import type { ParsingStrategy, DatasetDTO } from './types';

class DatasetParserManager {
  private readonly strategies: Record<string, ParsingStrategy>;

  constructor() {
    // Assegna direttamente gli oggetti strategy, non le classi
    this.strategies = {
      'text/csv': CsvParsingStrategy,
      'application/json': JsonParsingStrategy,
      'application/vnd.ms-excel': ExcelParsingStrategy,
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ExcelParsingStrategy,
      'csv': CsvParsingStrategy,
      'json': JsonParsingStrategy,
      'xls': ExcelParsingStrategy,
      'xlsx': ExcelParsingStrategy,
    };
  }

  private getStrategy(file: File): ParsingStrategy | null {
    if (!file) return null;
    
    const mimeType = file.type?.toLowerCase();
    if (mimeType && this.strategies[mimeType]) {
      return this.strategies[mimeType];
    }

    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    if (fileExtension && this.strategies[fileExtension]) {
      return this.strategies[fileExtension];
    }
    return null;
  }

  async parseDataset(file: File | null): Promise<DatasetDTO> {
    if (!file) {
      return {
        success: false,
        fileName: null,
        data: null,
        error: 'Nessun file fornito per il parsing.'
      };
    }

    const strategy = this.getStrategy(file);

    // Rimuovi il controllo typeof, dato che strategy è già un oggetto con il metodo parse
    if (strategy) {
      return strategy.parse(file);
    } else {
      return {
        success: false,
        fileName: file.name,
        data: null,
        error: `Tipo di file non supportato o strategia non trovata per: ${file.name} (Tipo: ${file.type || 'sconosciuto'}).`
      };
    }
  }
}

export default new DatasetParserManager();