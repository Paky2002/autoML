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
  modelName: string;
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

export interface TrainedModel {
  id: number;
  uuid: string;
  name: string;
  model_path: string;
  target_feature: string;
  problem_type: string;
  time_limit: number;
  eval_metric?: string;
  presets?: string;
  verbosity: number;
  dataset_filename?: string;
  status: 'training' | 'completed' | 'failed' | 'deleted';
  best_score?: number;
  best_model_name?: string;
  error_message?: string;
  created_at: string;
  updated_at?: string;
  
  // Additional ML info (populated by API when available)
  feature_columns?: string[];
  feature_importance?: Record<string, number>;
  detailed_leaderboard?: any[];
}