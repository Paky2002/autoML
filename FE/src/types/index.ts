export interface DatasetDTO {
  filename: string;
  headers: string[];
  rows: any[][];
  totalRows: number;
  fileSize: number;
  columns: ColumnInfo[];
  preview: any[];
}

export interface ColumnInfo {
  name: string;
  type: 'numeric' | 'categorical' | 'datetime' | 'text';
  nullCount: number;
  uniqueCount: number;
  sampleValues: any[];
}

export interface TrainingConfig {
  targetFeature: string;
  problemType: 'regression' | 'binary' | 'multiclass';
  timeLimit: number;
  evalMetric?: string;
  presets?: 'best_quality' | 'good_quality_faster' | 'optimize_for_deployment';
  verbosity: number;
}

export interface TrainingRequest {
  dataset: DatasetDTO;
  config: TrainingConfig;
}

export interface FileUploadProgress {
  loaded: number;
  total: number;
  percentage: number;
  stage: 'uploading' | 'parsing' | 'analyzing' | 'complete';
}