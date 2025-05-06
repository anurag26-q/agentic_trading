from fastapi import FastAPI,UploadFile,File,Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from starlette.responses import JSONResponse
from data_ingestion.data_ingestion_pipeline import DataIngestion
# from agent.work_flow import GrapgBuilder
# from data_models.models import * 


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/upload')
async def upload_files(files:List[UploadFile]=File(...)):
    try:
        ingestion=DataIngestion()
        ingestion.run_pipeline(files)
        return {'messages':'Files successfully processed and stored.'}
    except Exception as e:
        print('meri galti h ',e)
        return JSONResponse(status_code=500,content={'error':str(e)})