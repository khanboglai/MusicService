from fastapi import APIRouter, HTTPException, Form, Request, Depends
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/register', tags=['Reg'])

