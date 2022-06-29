from fastapi import HTTPException, Depends, APIRouter, Request
from app.database import session
import json
from app.schemas import MyInfo
from sqlalchemy import exc, select
import requests
from app.models import Secrets
from pydantic import parse_obj_as
from requests.auth import HTTPBasicAuth
from distutils.log import ERROR
from fastapi.security import HTTPBasic, HTTPBasicCredentials
security = HTTPBasic()

router = APIRouter(prefix='/api/vagina1')

@router.get("/getData", status_code=201, response_model=list[str])
async def get_encrypted_data():
   '''Берет вонючие носки из коробки'''
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
async def get_decrypted_data(encry_text: list[str], credentials: HTTPBasicCredentials = Depends(security)):
   '''Стирает вонючие носки'''
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

@router.post("/result", status_code=201)
async def send_result(my_info: MyInfo):
   '''Ну вот твои чистые носки, теперь можешь снова в них дрочить'''
   auth = HTTPBasicAuth('qummy', 'GiVEmYsecReT!')
   results = session.query(Secrets.decrypted_text)
   name = my_info.name
   repo_url = my_info.repo_url
   decrypted_list = []
   for i in results:
      decrypted_list.append(i[0])
   out_data = {"name": name, "repo_url": repo_url, "result": decrypted_list}
   response = requests.post("http://yarlikvid.ru:9999/api/result", data = json.dumps(out_data), auth= auth)
   return
