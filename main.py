from fastapi import Depends, FastAPI, Request
from ChatCSV.chatcsvservices import get_chatcsv_query, ingest_csv, import_csv

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")


@app.get("/")
def version(reg: Request):
    return "Chat-CSV API"

# --------------------- For ChatCSV -----------------------#

@app.post("/execute-sql")
async def generate_csv(req_info: dict):
    table = req_info["type"]
    return import_csv(table)


@app.post("/ingest")
async def ingest(req_info: dict):
    type = req_info["type"]
    return ingest_csv(type)


@app.post("/query")
async def ask_query(req_info: dict):
    query = req_info["question"]
    type = req_info["type"]
    chat_obj = get_chatcsv_query(type)
    return chat_obj.query_chat(query)
