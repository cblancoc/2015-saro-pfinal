import datetime
from django.db import models

# Create your models here.
    
class Table_User_Data(models.Model):
    page_title = models.TextField() 
    user = models.CharField(max_length=32)
    date = models.DateTimeField()
    description = models.TextField()
    FCMenu = models.TextField(default='#FFF')
    BCMenu = models.TextField(default='#0000FF')
    FSMenu = models.TextField(default='12px')
    FCLogin = models.TextField(default='#999999')
    BCLogin = models.TextField(default='#FFF')
    FSLogin = models.TextField(default='11px')
    FCFooter = models.TextField(default='#484848')
    BCFooter = models.TextField(default='#f4f4f4')
    FSFooter = models.TextField(default='10px')
        
class Table_Activity_Data(models.Model):
    act_title = models.TextField()
    event_type = models.TextField()
    price = models.TextField()
    date = models.DateTimeField()
    time = models.DateTimeField()
    duration_days = models.IntegerField()
    is_long_term = models.TextField() 
    url = models.TextField()  

class Table_Last_Refresh(models.Model):
    date = models.DateTimeField()
   
#Tabla que servira para asociar las noticias que estan en una revista a dicha revista
class Table_Selected_Acts(models.Model):
    act = models.IntegerField()
    user = models.TextField()
    selection_date = models.DateTimeField()
    
#Tabla que se usara para la parte opcional de poder poner comentarios en las revistas   
class Table_Comments(models.Model):
    act = models.IntegerField()
    user = models.TextField()
    date = models.DateTimeField()
    comment = models.TextField()
    
#Tabla que se usara para la parte opcional de poder sumar +1 a una noticia
class Table_Likes(models.Model):
    act = models.IntegerField()
    user = models.TextField()
