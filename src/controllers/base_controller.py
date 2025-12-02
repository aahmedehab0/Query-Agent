from helpers.confog import Settings , get_setings
import os

class BaseController:
    def __init__ (self):
        self.app_Settings = get_setings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        
        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database")
    
    def get_database_path(self, db_name: str):
        database_path = os.path.join(self.database_dir, db_name)
        os.makedirs(database_path , exist_ok= True)
        return database_path
    
    def get_files_path(self):
        files_dir = os.path.join(self.base_dir,
                                     "assets/files")
        os.makedirs(files_dir , exist_ok= True)
        return files_dir