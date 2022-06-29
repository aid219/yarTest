
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Secrets(Base):
    __tablename__ = "secrets"
    
    id = Column(Integer, primary_key=True)
    encrypted_text = Column(String, unique = True)
    decrypted_text = Column(String)
    created_on = Column(DateTime())

    def __init__(self, enc_text):
        """Constructor"""
        self.encrypted_text = enc_text
        self.created_on = datetime.now()

