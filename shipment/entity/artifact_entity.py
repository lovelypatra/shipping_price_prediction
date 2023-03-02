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

    