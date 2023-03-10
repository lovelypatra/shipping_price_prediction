from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
     report_file_path:str
     

@dataclass
class DataTransformationArtifact:
    input_transformer_object_path:str
    transformed_train_path:str
    transformed_test_path:str
    target_transformer_object_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str
    train_r2_score:float
    test_r2_score:float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_score:float

@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str 
    saved_model_dir:str

