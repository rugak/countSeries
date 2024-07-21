from typing import Optional
from datetime import datetime

class Exercice:
    def __init__(self, 
                 date: Optional[str] = None, 
                 niveau: int = 0, 
                 allonge: bool = False, 
                 assis: bool = False, 
                 session_id: Optional[str] = None, 
                 formatted_date: Optional[datetime] = None, 
                 serie: int = 0,
                 vie :int = 0):
        self.date = date
        self.niveau = niveau
        self.allonge = allonge
        self.assis = assis
        self.session_id = session_id
        self.formatted_date = formatted_date if formatted_date else datetime.now()
        self.serie = serie
        self.vie = vie

    def __repr__(self):
        return (f"Exercice(date={self.date}, niveau={self.niveau}, allonge={self.allonge}, "
                f"assis={self.assis}, session_id={self.session_id}, "
                f"formatted_date={self.formatted_date}, serie={self.serie})")
