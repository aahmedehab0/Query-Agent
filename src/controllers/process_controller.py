from .base_controller import BaseController
from models.enums import ProcessingEnum

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import  TextLoader
from langchain_chroma import Chroma
import os


class ProcessController(BaseController):
    def __init__(self):
        super().__init__()
        self.project_path = self.get_files_path()
        self.vectos_path = self.get_vectors_path()

    def get_file_extension(self , file_id : str ):
        return os.path.splitext(file_id)[-1]


    def get_file_loader(self , file_id : str ):
        file_path = os.path.join(self.project_path ,
                                 file_id
                                 )
        file_ext = self.get_file_extension (file_id = file_id)

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader (file_path=file_path ,encoding= "utf-8")
        
        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader (file_path=file_path )
        
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
    

    def push_vectors (self  , 
                      file_id : str,
                      chunk_size : int = 512,
                      overlap_size : int = 50,
                      vectorstore : Chroma =  None,
                      ):
        
        chunks = self.process_file_content(
            chunk_size= chunk_size,
            overlap_size= overlap_size,
            file_id= file_id,
            )
        
        if chunks:
            if not vectorstore:
                return None

            try :
                vectorstore.add_documents(chunks)
                return True

            except RuntimeError as e:
                print ("can't push to vector DB " , e )
                raise

        return None
                


