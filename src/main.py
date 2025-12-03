import dspy
from langchain_cohere import ChatCohere ,CohereEmbeddings
from helpers.confog import get_settings 
from stores import SemanticRetriever
from controllers import BaseController , ProcessController
from models.enums import LanguageEnum
from agent import NLToSQLModule , QueryAgent 
from tools import SQLHelper
from langchain_chroma import Chroma
import os
from IPython.display import Image, display

#config settings for .env
settings = get_settings()

#-------------------- load models------------------
# LLm generation model with cohere
llm = ChatCohere(
    model=settings.GENERATION_MODEL,
    temperature = settings.TEMPERATURE , 
    cohere_api_key= settings.CO_API_KEY)

#dspy model 
dspy_model = dspy.LM(
    model=settings.DSPY_MODEL ,
    api_key=settings.CO_API_KEY)
dspy.configure(lm=dspy_model)

# cohere embeding model
embeddings = CohereEmbeddings(
    model=settings.EMBEDIBG_MODEL,
    cohere_api_key= settings.CO_API_KEY)



base_controller = BaseController()
process_controller = ProcessController()

#load database schema and path 
db_path = os.path.join (
    base_controller.database_dir , settings.DATA_BASE_NAME)

schema = SQLHelper().get_db_schema(db_path = db_path )

#loading files will run on RAG 
files_path = base_controller.get_files_path()

#vectorstore to save embeding files
vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=base_controller.get_vectors_path(),
        collection_name= settings.DATA_BASE_NAME.split(".")[0]
    )


for _, _, files in os.walk(files_path):
    for filename in files:
        if filename.endswith('.txt') or filename.endswith('.pdf'):
            validate = process_controller.push_vectors ( 
                        file_id  = filename,
                        chunk_size = settings.CHUNK_SIZE,
                        overlap_size = settings.OVERLAP_SIZE,
                        vectorstore = vectorstore,
                        )
            if not validate :
                raise ValueError("can't push to vector DB ")

            
#load paths of questions files which will train with dspy models
english_questions_path , arabic_questions_path = base_controller.get_questions_path()

#--------------load English question retriever----------
english_questions = SQLHelper().load_dspy_dataset(
    SQLHelper().load_jsonl( path = english_questions_path) )

english_embeding_path = base_controller.get_embeding_path(
    lang =LanguageEnum.ENGLISH.value )

english_retriever = SemanticRetriever(
    cache_path = english_embeding_path,
    examples= english_questions,
    local_device= settings.LOCAL_DEVICE,
    local_emeding_model= settings.QUESTION_EMBEDING_MODEL
    )

#--------------load arabic question retriever----------
arabic_questions = SQLHelper().load_dspy_dataset(
    SQLHelper().load_jsonl(path = arabic_questions_path) )

arabic_embeding_path = base_controller.get_embeding_path(
    lang =LanguageEnum.ARABIC.value )

arabic_retriever = SemanticRetriever(
    cache_path = arabic_embeding_path,
    examples= arabic_questions,
    local_device= settings.LOCAL_DEVICE,
    local_emeding_model= settings.QUESTION_EMBEDING_MODEL
    )


#dspy models to train arabic and english question
nl2sql_arabic = NLToSQLModule(arabic_retriever, schema)
nl2sql_english = NLToSQLModule(english_retriever, schema)

#query agent to get nodes and graph
query_agent =  QueryAgent(
    llm = llm,
    dspy_model = dspy_model,
    vectorstore = vectorstore,
    nl2sql_arabic = nl2sql_arabic,
    nl2sql_english = nl2sql_english,
    db_path = db_path
)

app = query_agent.build_graph()





