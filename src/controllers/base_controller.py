from helpers.confog import Settings , get_settings
from models.enums import LanguageEnum
import os

class BaseController:
    def __init__ (self):
        self.app_Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        
        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database")
    
    
    def get_files_path(self):
        files_dir = os.path.join(self.base_dir,
                                     "assets/files")
        os.makedirs(files_dir , exist_ok= True)
        return files_dir
    
    def get_vectors_path(self):
        files_dir = os.path.join(self.base_dir,
                                "assets/vector_db")
        os.makedirs(files_dir , exist_ok= True)
        return files_dir
    
    def get_questions_path (self ):

        files_dir = os.path.join(self.base_dir,
                                "assets/examples")
        os.makedirs(files_dir , exist_ok= True)
        english_file = os.path.join(files_dir ,"english_questions.jsonl" ) 
        arabic_file = os.path.join(files_dir ,"arabic_questions.jsonl" ) 

        if os.path.exists (english_file) and os.path.exists (arabic_file):
            return english_file , arabic_file
        return None
    
    def get_embeding_path (self , lang : str ):
        files_dir = os.path.join(self.base_dir,
                                "assets/embeding_cache")
        english_file = os.path.join(files_dir ,"english.npy" )
        arabic_file = os.path.join(files_dir ,"arabic.npy" )

        if lang == LanguageEnum.ARABIC.value:
            return arabic_file

        else:
            return english_file