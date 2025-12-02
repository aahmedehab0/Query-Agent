from .base_controller import BaseController
from models.enums import ProcessingEnum

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import  TextLoader

from dataclasses import dataclass
import os


@dataclass
class Document:
    page_content: str
    metadata: dict

class ProcessController(BaseController):
    def __init__(self , project_id : str):
        super().__init__()
        self.project_id = project_id
        self.project_path = BaseController().get_files_path()

    def get_file_extension(self , file_id : str ):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self , file_id : str ):
        file_path = os.path.join(self.project_path ,
                                 file_id
                                 )
        file_ext = self.get_file_extension (file_id = file_id)

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader (file_path ,encoding= "utf-8")
        
        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader (file_path , encoding= "utf-8")
        
        return None
    
    def get_file_content(self , file_id:str):
        loader = self.get_file_loader(file_id = file_id)
        if not loader :
            return None
        return loader.load()  
        
    
def process_file_content (self ,  file_id :str,
                              chunk_size : int=100 , overlap_size : int=20 
    ): 

    file_contents = self.get_file_content(file_id = file_id) 

    if not file_contents:
        return None
    
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = overlap_size,
        length_function = len
    )

    file_content_texts = [ 
        rec.page_content for  
        rec in file_contents
    ]

    file_metadata_texts = [ 
        rec.metadata for  
        rec in file_contents
    ]

    chunks = text_spliter.create_documents(
        texts= file_content_texts,
        metadatas= file_metadata_texts
    )
    return chunks