
from fastapi import HTTPException, Depends, APIRouter
from app.models import Secrets
from app.database import session
import json
from sqlalchemy import exc, select
import requests
from pydantic import parse_obj_as
from requests.auth import HTTPBasicAuth
from distutils.log import ERROR
from fastapi.security import HTTPBasic, HTTPBasicCredentials
security = HTTPBasic()

router = APIRouter()

@router.get("/getData", status_code=201, response_model=list[str])
async def get_encrypted_data():
   global encry_text
   response = requests.get('http://yarlikvid.ru:9999/api/top-secret-data')
   encry_text = parse_obj_as(list[str], response.json())
   for i in encry_text:
      session.add(Secrets(i))
   try:
      session.commit()
   except exc.SQLAlchemyError as e:
      raise HTTPException(
      status_code=400, 
      detail=f"oi pizda nahui blya, vse poplilo nahui, trechit po shvam, nehui mne pihat v bazu vot eti stroki, yak ya uze sto raz videl, i bez odezhdi"
      )
   return encry_text

@router.post("/decryptData", status_code=201, response_model=list[str])
async def get_decrypted_data(credentials: HTTPBasicCredentials = Depends(security)):
   global encry_text, decry_text
   if credentials.username == "qummy" and credentials.password == "1121":
      auth = HTTPBasicAuth('qummy', 'GiVEmYsecReT!')
      response = requests.post("http://yarlikvid.ru:9999/api/decrypt", data = json.dumps(encry_text), auth= auth)
      decry_text = parse_obj_as(list[str], response.json())
      for i in range(0, len(encry_text)):
         ss2 = session.execute(select(Secrets).filter_by(encrypted_text=encry_text[i])).scalar_one()
         ss2.decrypted_text = decry_text[i]
      session.commit()
   else:
      raise HTTPException(
         status_code=400, detail=f"kuda ti rozu svoyu suesh, hareck ti ebanii, ti kto takoi, ya vas ne zval, idite nahui"
      )
   return decry_text

@router.post("/result", status_code=201, response_model=list[str])
async def send_result():
   pass