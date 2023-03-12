from datetime import datetime
import base64
from django.core.files.base import ContentFile

def compare_dates(date1, date2):
    # date in yyyy/-mm-dd hh:mm:ss format
    karon = datetime(date1.year, date1.month, date1.day, date1.hour, date1.minute, date1.second)
    expire_date = datetime(date2.year, date2.month, date2.day, date2.hour, date2.minute, date2.second)
    if karon >= expire_date:
        return False
    else:
        return True
    

def b64toimg(b64):
    print("hello wrodl")
    format, imgstr = b64.split(';base64,')
    ext = format.split('/')[-1] 
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data