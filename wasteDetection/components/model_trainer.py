import os,sys
import yaml
from wasteDetection.utils.main_utils import read_yaml_file
from wasteDetection.logger import logging
from wasteDetection.exception import AppException
from wasteDetection.entity.config_entity import ModelTrainingConfig
from wasteDetection.entity.artifacts_entity import ModelTrainerArtifact

class ModelTrainer:
    def __init__(self,
                 model_trainer_config:ModelTrainingConfig
                 ):
        self.model_trainer_config=model_trainer_config
    
    def initiate_model_trainer(self,)->ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            logging.info("unzipping data")
            import zipfile, shutil
            if os.path.exists("data.zip"):
                with zipfile.ZipFile("data.zip", 'r') as zip_ref:
                    zip_ref.extractall(".")
                if os.path.exists("data.zip"):
                    os.remove("data.zip")
            
            with open("data.yaml",'r') as stream:
                num_classes=str(yaml.safe_load(stream)['nc'])
                
            model_config_file_name=self.model_trainer_config.weight_name.split(".")[0]
            print(model_config_file_name)
            
            config=read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            
            config['nc']=int(num_classes)
            
            os.makedirs("yolov5/models", exist_ok=True)
            with open(f"yolov5/models/custom_{model_config_file_name}.yaml",'w') as f:
                yaml.dump(config,f)
            
            os.system(f'cd yolov5 && "{sys.executable}" train.py --img 416 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_epochs} --data ../data.yaml --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results --cache')
            
            best_weight_src = "yolov5/runs/train/yolov5s_results/weights/best.pt"
            if os.path.exists(best_weight_src):
                shutil.copy(best_weight_src, "yolov5/best.pt")
                os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
                shutil.copy(best_weight_src, os.path.join(self.model_trainer_config.model_trainer_dir, "best.pt"))
            
            shutil.rmtree("yolov5/runs", ignore_errors=True)
            shutil.rmtree("train", ignore_errors=True)
            shutil.rmtree("valid", ignore_errors=True)
            if os.path.exists("data.yaml"):
                os.remove("data.yaml")
            
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path='yolov5/best.pt'
            )
            
            logging.info("Exited initiate model_trainer method pf ModelTrainer class")
            logging.info(f"Model Trainer artifact: {model_trainer_artifact}")
            
            return model_trainer_artifact
        
        except Exception as e:            
            raise AppException(e,sys)