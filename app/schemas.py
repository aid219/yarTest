from pydantic import BaseModel, StrictStr

class MyInfo(BaseModel):
    name: StrictStr
    repo_url: StrictStr
