from fastapi import APIRouter, HTTPException


from app.grpc_clients.writer_client import WriterClient

router = APIRouter()
writer_client = WriterClient()
    
