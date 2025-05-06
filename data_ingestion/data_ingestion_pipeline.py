import os 
import tempfile


from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from utils.model_loader import ModelLoader
from utils.model_loader import load_config
from pinecone import ServerlessSpec
from pinecone import Pinecone
from uuid import uuid4





class DataIngestion:

    def __init__(self):
        '''
        Initilize the environment variable,embedding model,and config.
        '''
        print('Initilizing DataIngestion Pipeline ...')
        self.model_loader=ModelLoader()
        self._load_env_variable()
        self.config=load_config()

    def _load_env_variable(self):
        '''
        load and validate requried environment varibales
        '''
        load_dotenv()
        requried_var=[
            'GOOGLE_API_KEY','PINECONE_API_KEY'
        ]
        missing_vas=[var for var in requried_var if os.getenv(var) is None]

        if missing_vas:
            raise EnvironmentError(f'Missing environment variable : {missing_vas}')
        
        self.google_api_key=os.getenv('GOOGLE_API_KEY')
        self.pinecone_api_key=os.getenv('PINECONE_API_KEY')

    def load_documnets(self,uploaded_files)-> list[Document]:
        '''
        Load documnets from uploaded PDF and Docs file
        '''
        documnets =[]
        for uploaded_file in  uploaded_files:
            if uploaded_file.name.endswith('.pdf'):
                with tempfile.NamedTemporaryFile(delete=False,suffix='.pdf') as tempfile:
                    tempfile.write(uploaded_file.read())
                    loader=PyPDFLoader(tempfile.name)
                    documnets.extend(loader.load())
            
            elif uploaded_file.name.endswith('.docx'):
                with tempfile.NamedTemporaryFile(delete=False,suffix=',docs')as tempfile:
                    tempfile.write(uploaded_file.read())
                    loader=Docx2txtLoader(tempfile.name)
                    documnets.extend(loader.load())
            else:
                print(f'Unsupported file format type :{uploaded_file.name}')
            return documnets

    def store_in_vector_db(self,documents:list[Document]):
        '''
        Split documents and create vectore store with embeddings.
        '''

        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        documents=text_splitter.split_documents(documents)

        # pc ==> pinecone client 
        pc=Pinecone(api_key=self.pinecone_api_key)

        if not pc.has_index(self.config['vectore_db']['index_name']):
            pc.create_index(
                name=self.config['vectore_dv']['index_name'],
                dimension=768,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws',region='us-east-1')
            )
        index=pc.Index(self.config['vectore_db']['index_name'])

        vectore_store=PineconeVectorStore(index=index,embedding=self.model_loader.load_embeddings( ))
        uuids=[str(uuid4()) for _ in range(len(documents))]
        vectore_store.add_documents(documents=documents,ids=uuids)


    def run_pipeline(self,uploaded_files):
        '''
        Run full data ingestion: load files,split,embed and store
        '''

        documents=self.load_documnets(uploaded_files)
        if not documents:
            print('no valid documents found .')
            return 
        self.store_in_vector_db(documents)
