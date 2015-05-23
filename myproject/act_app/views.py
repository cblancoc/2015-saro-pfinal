# -*- coding: utf-8 -*-
# Autor: Cristina Blanco Carrasco (cblancoc)

from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from BeautifulSoup import BeautifulSoup
import datetime
from datetime import timedelta
import feedparser
import time
from time import gmtime, strftime
import re
import string
import sys
import urllib
import urllib2
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from models import Table_User_Data, Table_Activity_Data, Table_Last_Refresh
from models import Table_Selected_Acts, Table_Comments, Table_Likes
# Create your views here.

@csrf_exempt
def slash(request):
    if request.user.is_authenticated():
        init_user(request.user.username)
    pages = Table_User_Data.objects.all()
    out1 = ""
    out2 = ""
    for page in pages:
        if page.page_title:
            page_url = "<html><body>" + "<a href=\"http://localhost:1234/" + page.user + '">' + page.page_title + '</a></body></html>' + "\r\n"
        else:
            page_url = "<html><body>" + "<a href=\"http://localhost:1234/" + page.user + ">Pagina de " + page.user + '</a></body></html>' + "\r\n"
        out1 += page_url + "</br>" + "Usuario: " + page.user + "</br>"
        out1 += "Descripcion: "
        if page.description and page.description != "()":
             out1 += page.description
        else:
            out1 += "Pagina con las actividades de culturales y de ocio seleccionadas por " + page.user
        out1 += "</br></br>"
    out2 += show_last_act()
    if request.user.is_authenticated():
        user = request.user.username
        init_user(user)
        dict_css = {'newcss': pass_css(request,user),"Titulo1": "PAGINAS", "Titulo2": "ACTIVIDADES", "Contenido1": out1  ,"Contenido2": out2  , "usuario": request.user.username}
        dict_css.update(csrf(request))
        return render_to_response("slash_auth.html", dict_css) 
    else:
        dict_css = {"Titulo1": "PAGINAS", "Titulo2": "ACTIVIDADES", "Contenido1": out1  ,"Contenido2": out2  , "Redirect": ''}
        dict_css.update(csrf(request))
        return render_to_response("slash_noauth.html", dict_css)

def show_last_act():
    out = ""
    acts = Table_Activity_Data.objects.filter().order_by("date")
    n = 0
    now = timezone.now()
    now = now + timedelta(hours=2)
    for act in acts: 
        if (act.date > now):  
            if (n < 10):
                out += show_activity(act.id)
                n += 1
    return out

def show_all_act(request, item_filter, sort_filter):
    out_show = ""
    n = 0
    acts = Table_Activity_Data.objects.all()
    if (sort_filter == "Date"):
        for act in acts:
            if (str(act.date)[5:7] == str(item_filter)):
                out_show += show_activity(act.id)
                if request.user.is_authenticated():
                    out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                n += 1
        acts = None            
    elif (sort_filter == "Title"):
        upper_l = string.ascii_uppercase
        for act in acts:
            if (item_filter in upper_l):
                if (act.act_title[0] == item_filter):
                    out_show += show_activity(act.id)
                    if request.user.is_authenticated():
                        out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                    n += 1
            if (item_filter == "0"):
                if (act.act_title[0] not in upper_l):
                    out_show += show_activity(act.id)
                    if request.user.is_authenticated():
                        out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                    n += 1
        acts = None
    elif (sort_filter == "Duration"):
        if (item_filter == "1"):
            acts = Table_Activity_Data.objects.filter(duration_days = 1)
            for act in acts:
                 out_show += show_activity(act.id)
                 if request.user.is_authenticated():
                    out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                 n += 1
        else:
            for act in acts:
                write = False 
                if (item_filter == "2"):
                    if (act.duration_days > 1) and (act.duration_days < 8):
                        write = True
                elif (item_filter == "3"):
                    if (act.duration_days > 7) and (act.duration_days < 21):
                        write = True
                elif (item_filter == "4"):
                    if (act.duration_days > 20):
                        write = True
                if write:
                    out_show += show_activity(act.id)
                    if request.user.is_authenticated():
                        out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                    n += 1               
        acts = None
    elif (sort_filter == "Price"):
        if (item_filter == "1"):
            acts = Table_Activity_Data.objects.all().filter(price = "Gratis") 
            for act in acts:
                 out_show += " PRICE: " + act.price
                 out_show += show_activity(act.id)
                 if request.user.is_authenticated():
                    out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                 n += 1
        elif (item_filter == "5"):
            acts = Table_Activity_Data.objects.all().filter(price = "Precio a consultar") 
            for act in acts:
                 out_show += show_activity(act.id)
                 if request.user.is_authenticated():
                    out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                 n += 1
        else:
            acts = Table_Activity_Data.objects.all()
            for act in acts:
                write = False 
                if (item_filter == "2"):
                    try:
                        if (act.price[0] > "0") and (act.price[0] < "6"):
                            try:
                                if (act.price[1] == " "):
                                    write = True
                            except:
                                write = True
                    except:
                        pass
                elif (item_filter == "3"):
                    if (act.price[0] == 1):
                        try:
                            if (act.price[1] == " "):
                                write = True
                        except:
                            write = True
                    else:
                        if (act.price[0] > "5" and act.price[0] <= "9"):
                            write = True
                elif (item_filter == "4"):
                    try:
                        if (act.price[1] == "0" and act.price[0] > "1"):
                            write = True
                        elif (act.price[1] > "0" and act.price[1] <= "9"):
                            write = True
                    except:
                        pass
                if write:
                    out_show += show_activity(act.id)
                    if request.user.is_authenticated():
                        out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
                    n += 1 
        acts = None  
    else:
        acts = Table_Activity_Data.objects.all()
    if acts:
        for act in acts:
            out_show += show_activity(act.id)
            if request.user.is_authenticated():
                    out_show += "<html><body><a href='http://localhost:1234/actividad/add/" + str(act.id) + "'" + ">Elegir esta actividad</a></body></html></br>"
            n += 1    
    return n, out_show 

@csrf_exempt
def all_act_general(request, item_filter, sort_filter):
    if request.user.is_authenticated():
        init_user(request.user.username)
    if request.method == "POST":
        if not request.body:
            refresh_act()
        else:
            pass          
    out = " "
    [n_act,out_show] = show_all_act(request, item_filter, sort_filter)
    out += out_show
    refresh = 0
    if request.user.is_authenticated():
        user = request.user.username
        init_user(user)
        dict_css = {'newcss': pass_css(request,user),"Titulo": "ACTIVIDADES", "Contenido": out  , "usuario": request.user.username, "refresh_date": str(Table_Last_Refresh.objects.get(id=1).date)[0:19], "n_act": n_act }
        dict_css.update(csrf(request))
        return dict_css
    else:
        dict_css = {"Titulo": "PAGINAS", "Contenido": out, "Redirect": ''}
        dict_css.update(csrf(request))
        return dict_css     

@csrf_exempt
def all_act(request):
    item_filter = None
    sort_filter = None
    dict_css = all_act_general(request, item_filter, sort_filter)
    if request.user.is_authenticated():
        return render_to_response("all_act_auth.html", dict_css)
    else:
        return render_to_response("all_act_noauth.html", dict_css)

@csrf_exempt      
def all_act_title(request, item_filter):
    sort_filter = "Title"
    dict_css = all_act_general(request, item_filter, sort_filter)
    if request.user.is_authenticated():
        return render_to_response("all_act_auth.html", dict_css)
    else:
        return render_to_response("all_act_noauth.html", dict_css)

@csrf_exempt      
def all_act_duration(request, item_filter):
    sort_filter = "Duration"
    dict_css = all_act_general(request, item_filter, sort_filter)
    if request.user.is_authenticated():
        return render_to_response("all_act_auth.html", dict_css)
    else:
        return render_to_response("all_act_noauth.html", dict_css)
 
@csrf_exempt      
def all_act_date(request, item_filter):
    sort_filter = "Date"
    dict_css = all_act_general(request, item_filter, sort_filter)
    if request.user.is_authenticated():
        return render_to_response("all_act_auth.html", dict_css)
    else:
        return render_to_response("all_act_noauth.html", dict_css)
        
@csrf_exempt      
def all_act_price(request, item_filter):
    sort_filter = "Price"
    dict_css = all_act_general(request, item_filter, sort_filter)
    if request.user.is_authenticated():
        return render_to_response("all_act_auth.html", dict_css)
    else:
        return render_to_response("index.html", dict_css)
         
def refresh_act():

    Table_Activity_Data.objects.all().delete()
    url = "http://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.xml"
    bSoup = BeautifulSoup(urllib.urlopen(url).read())
    soup_cont = bSoup.findAll('contenido')
    n = 0
    
    for row in soup_cont:
        try:
            title = row.find('atributo', {'nombre':'TITULO'})
            title = str(title).split(">")[1].split("<")[0]
            act_type = row.find('atributo', {'nombre':'TIPO'})
            act_type = str(act_type).split(">")[1].split("<")[0]
            act_type = str(act_type).split("/contenido/actividades/")[-1]
            act_type = re.sub(r"(?<=\w)([A-Z])", r" \1", act_type)
            precio = row.find('atributo', {'nombre':'PRECIO'})
            if precio:
                price = str(precio).split("[")[2].split("]")[0]
            else:
                free = row.find('atributo', {'nombre':'GRATUITO'})
                free = str(free).split(">")[1].split("<")[0]
                if (free == "1"):
                    price = "Gratis"
                else:
                    price = "Precio a consultar"
            date = row.find('atributo', {'nombre':'FECHA-EVENTO'})
            date = str(date).split(">")[1].split("<")[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
            end_date = row.find('atributo', {'nombre':'FECHA-FIN-EVENTO'})
            end_date = str(end_date).split(">")[1].split("<")[0]
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S.%f')
            duration = end_date - date
            duration_days = duration.days + 1
            time = row.find('atributo', {'nombre':'HORA-EVENTO'})
            time = str(time).split(">")[1].split("<")[0]
            time = datetime.datetime.strptime(time, '%H:%M')
            long_term = row.find('atributo', {'nombre':'EVENTO-LARGA-DURACION'})
            long_term = str(long_term).split(">")[1].split("<")[0]
            if (long_term == '0'):
                long_term = "No"
            elif (long_term == '1'):
                long_term = "Si"
            link = row.find('atributo', {'nombre':'CONTENT-URL'})
            link = str(link).split(">")[1].split("<")[0]
            table = Table_Activity_Data(id = n,
                                       act_title = str(title).decode('utf8'),
                                       event_type = str(act_type).decode('utf8'),
                                       price = str(price).decode('utf8'),
                                       date = date,
                                       duration_days = duration_days,
                                       time = time,
                                       is_long_term = str(long_term).decode('utf8'),
                                       url = str(link).decode('utf8'))
            table.save()
            n += 1
        except:
            pass
    now = datetime.datetime.now()
    now += timedelta(hours=2)
    now = str(now)[0:19]
    now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    table = Table_Last_Refresh(id = 1, date = now)
    table.save()
            

def show_activity(act_id):
    out = "</br>"
    act = Table_Activity_Data.objects.get(id=act_id)
    out += "</br>" 
    out += "<html><body>" + "<a href=http://localhost:1234/actividad/" + str(act.id) + '>' + "TITULO: " + act.act_title + '</a></body></html></br>'
    out += "TIPO: " + act.event_type + "</br>"
    out += "PRECIO: " + act.price + "</br>"
    out += "FECHA: " + str(act.date).split(" ")[0] + "</br>"
    out += "DURACION: " + str(act.duration_days)
    if act.duration_days == 1:
        out += " dia"
    else: 
        out += " dias"
    out += "</br>"
    out += "HORA: " + str(act.time)[11:16] + "</br>"
    out += "LARGA DURACION: " + str(act.is_long_term) + "</br>"
    out += "LINK: " + "<html><body><a href='" + act.url + "'>Acceder</a></body></html></br>"
    "<html><body><a href='http://localhost:1234/actividad/" + str(act.id) + "/add'" + ">Elegir esta actividad</a></body></html></br>"
    return out

@csrf_exempt              
def activities(request, act_id):
    if request.user.is_authenticated():
        init_user(request.user.username)

    out = ""
    try:
        out += show_activity(act_id)
    except:
        out += "Actividad no encontrada"
    try:    
        act = Table_Activity_Data.objects.get(id = int(act_id))
        url = str(act.url).replace("amp;", "")
        bSoup = BeautifulSoup(urllib.urlopen(url).read())
        soup_cont = bSoup.find('a', {'class':'punteado'})
        bSoup = "http://www.madrid.es"
        url2 = bSoup + str(soup_cont).decode('utf8').split('"')[3].replace("amp;", "")
        bSoup2 = BeautifulSoup(urllib.urlopen(url2).read())
        soup_cont2 = bSoup2.find('div', {'class':'parrafo'})
        out += "<h3> Informacion adicional </h3>"
        out += str(soup_cont2).decode('utf8')
    except:
        pass
    if request.user.is_authenticated():
        user = request.user.username
        init_user(user)
        out += put_form(str(act_id)) + '</br>'
        dict_css = {'newcss': pass_css(request,user),"Titulo": "ACTIVIDAD", "Contenido": out  , "usuario": request.user.username, "activity": str(act_id)}
        dict_css.update(csrf(request))
        return render_to_response("activities_auth.html", dict_css) 
    else:
        dict_css = {"Titulo": "ACTIVIDAD", "Contenido": out, "Redirect": ''}
        dict_css.update(csrf(request))
        return render_to_response("activities_noauth.html", dict_css)
        
def activities_add(request, act_id):
    if request.user.is_authenticated():
        init_user(request.user.username)
        now = datetime.datetime.now()
        now += timedelta(hours=2)
        table = Table_Selected_Acts(act = act_id, user = request.user.username, selection_date = now)
        table.save()
        red_page = "/actividad/" + str(act_id)
    return HttpResponseRedirect(red_page)
    
    
@csrf_exempt   
def user(request, user):
    owner = 0   
    user_visitor = request.user.username
    if request.method == 'POST':
        body = request.body
        title = body.split('content=')[1]
        table = Table_User_Data.objects.get(user=user_visitor)
        table.page_title = title
        table.save()
  
    try:    
        table = Table_User_Data.objects.get(user=user)       
        if user_visitor == user:           
            owner = 1
        else:
            owner = 0
        title = table.page_title       
        pages = Table_Selected_Acts.objects.filter(user=user).order_by("-selection_date")

        if len (pages) == 0:
            content = 'Este usuario todavia no tiene actividades seleccionadas' + "</br>" + "</br>" + "</br>"
        else:
            content = ' '
            n = 0
            if n < 10:
                for activities in pages:
                    n += 1
                    activity = Table_Activity_Data.objects.get(id = int(activities.id))
                    content += "<h1>" + activity.act_title + "</h1></br>"
                    content += "Fecha de la actividad: " + str(activity.date)[0:10] + "</br>"
                    content += "Elegida en: " + str(activities.selection_date)[0:19] + "</br>"
                    content += "<html><body>" + "<a href=http://localhost:1234/actividad/" + str(activities.id) + '>' + "Pagina de la actividad" + '</a></body></html>' + "</br>"
                    content += "</br>" + "</br>"
                    if request.user.is_authenticated():
                        try:
                            new = Table_Likes.objects.get(act = str(activities.id), user = user_visitor)
                            content += 'Ya has sumado +1 a esta actividad</br>'
                        except Table_Likes.DoesNotExist:
                            content += put_like_form(str(activities.id), user) + '</br>'
                    like_list = Table_Likes.objects.filter(act = activities.id)
                    content += 'Esta actividad le gusta a ' + str(len(like_list))
                    if len(like_list) == 1:
                        content += ' persona.</br>'
                    else:
                        content += ' personas.</br>'
                    content += "</br>" + "</br>"                       
        comments = Table_Comments.objects.filter(user= user).order_by("-date")
        if len(comments) == 0:
            pass
        else:            
            content += '<html><body>'
            content += ('</br></br><h1>COMENTARIOS DE: ' + user + '</h1></br>')  
            for comment in comments:
                act = comment.act
                act = Table_Activity_Data.objects.get(id = act)
                content += '<h2>Actividad: </h2><h3>' + act.act_title + '</h3></br>'
                content += 'Publicado en: ' + str(comment.date) + '</br>'
                content += '<h3>COMENTARIO: </br>' + comment.comment + '</h3></br></br>'
            content += '</body></html>'
                        
        
    except Table_User_Data.DoesNotExist:
        title = "Pagina no encontrada " 
        content = "No existe una pagina con ese nombre"
    
    if request.user.is_authenticated():
        init_user(user_visitor)
        dict_css = {'newcss': pass_css(request,user),'Titulo': title ,'Contenido': content, 'usuario': user_visitor, 'act': owner, 'user': user}
        dict_css.update(csrf(request))
        return render_to_response("user_auth.html", dict_css)

            
    else:
        dict_css = {"Titulo": title, "Contenido": content,"Redirect": user}
        dict_css.update(csrf(request))
        return render_to_response("user_noauth.html", dict_css)

@csrf_exempt
def init_user(user):
    try:
        out = Table_User_Data.objects.get(user=user).page_title            
    except Table_User_Data.DoesNotExist:
        page_title = "Pagina de " + user
        now = datetime.datetime.now()
        now += timedelta(hours=2)
        table = Table_User_Data(user = user, page_title = page_title, date = now, FCMenu = '#fff',BCMenu ='#7fa71f' ,FSMenu = '12px',FCLogin ='#999999' ,BCLogin ='#FFF' ,FSLogin ='11px' ,FCFooter = '#484848',BCFooter = '#f4f4f4',FSFooter ='10px' )
        table.save()

def pass_css(request, user):
    table = Table_User_Data.objects.get(user = user)
    dict_user = {'FCMenu' : table.FCMenu, 'BCMenu' : table.BCMenu ,'FSMenu' : table.FSMenu, 'FCLogin' : table.FCLogin ,'BCLogin' : table.BCLogin ,'FSLogin' : table.FSLogin ,'FCFooter' : table.FCFooter, 'BCFooter' : table.BCFooter, 'FSFooter' : table.FSFooter}
    dict_user.update(csrf(request))
    newcss = render_to_response('style.css', dict_user)
    return newcss
    
@csrf_exempt
def changecss(request):
    if request.user.is_authenticated():
        body = request.body
        dict_css = {}
        user = request.user.username
        if request.method == 'POST':
            dict_css = body.split('&content=')
          
            user_id = Table_User_Data.objects.get(user = user)
            first = dict_css[0]
            first = first.split('=')[1]
            list_css = []
            if first == '':
                list_css.append(user_id.BCMenu)
            else:
                list_css.append(first)               
            n = 0
            for num in dict_css:
                if n == 0:
                    pass
                else:                                                      
                    if n == 1:
                        if num == '':
                            list_css.append(user_id.FCMenu)
                        else:
                            list_css.append(num)                           
                    elif n == 2:
                        if num == '':
                            list_css.append(user_id.FSMenu)
                        else:
                            list_css.append(num)                         
                    elif n == 3:
                        if num == '':
                            list_css.append(user_id.BCLogin)
                        else:
                            list_css.append(num)
                    elif n == 4:
                        if num == '':
                            list_css.append(user_id.FCLogin)
                        else:
                            list_css.append(num)
                    elif n == 5:
                        if num == '':
                            list_css.append(user_id.FSLogin)
                        else:
                            list_css.append(num)
                    elif n == 6:
                        if num == '':
                            list_css.append(user_id.BCFooter)
                        else:
                            list_css.append(num)
                    elif n == 7:
                        if num == '':
                            list_css.append(user_id.FCFooter)
                        else:
                            list_css.append(num)
                    elif n == 8:
                        if num == '':
                            list_css.append(user_id.FSFooter)
                        else:
                            list_css.append(num)                
                n = n + 1
            
            table = Table_User_Data(id = user_id.id, user = user, page_title = user_id.page_title,date = user_id.date, BCMenu = list_css[0],FCMenu = list_css[1] ,FSMenu = list_css[2],BCLogin = list_css[3] ,FCLogin = list_css[4] ,FSLogin = list_css[5] ,BCFooter = list_css[6],FCFooter = list_css[7],FSFooter = list_css[8])
            table.save()
                               
    return HttpResponseRedirect('http://localhost:1234/' + user)
    
    
def help(request):       
    content = '<html><body>'
    content +=  "Las paginas disponibles en esta pagina web son: </br></br>"
    content += "<li> (localhost:1234/) La pagina principal, que muestra las diez actividades mas proximas y el listado de las paginas personales disponibles. <a href=http://localhost:1234/>Acceder.</a></li></br></br>"
    content += "<li> (localhost:1234/usuario) La pagina personal de un usuario, que muestra las actividades seleccionadas por el. Si es tu propia pagina puedes personalizar algunos aspectos de la web </li></br></br>"
    content += "<li> (localhost:1234/todas) En esta pagina se muestran todas las actividades disponibles, las cuales se pueden filtrar segun varios criterios. Ademas, se puede actualizar el listado de actividades. <a href=http://localhost:1234/todas>Acceder.</a></li></br></br>"
    content += "<li> (localhost:1234/actividad/id) La pagina de una actividad, en ella se puede encontrar tanto informacion basica de ella como adicional.</li></br></br>"
    content += "<li> (localhost:1234/rss, localhost:1234/usuario/rss) Los canales RSS de la pagina principal y de las paginas personales, se acceden al poner /rss al final de la url. <a href=http://localhost:1234/rss>Acceder al de la pagina principal.</a></li></br></br>"
    
    content += '</html></body>'
    
    
    if request.user.is_authenticated():
        user = request.user.username
        init_user(user)
        dict_css = {'newcss': pass_css(request,user),"Titulo": "AYUDA", "Contenido": content  , "usuario": user}
        dict_css.update(csrf(request))
        return render_to_response("help_auth.html", dict_css) 
    else:
        dict_css = {"Titulo": "AYUDA", "Contenido": content,"Redirect": 'ayuda'}
        dict_css.update(csrf(request))
        return render_to_response("help_noauth.html", dict_css)
    
def put_like_form(activity, url):
    form ='<form name="input" action="http://localhost:1234/like/' + url + '" method="POST" enctype="text/plain">'
    form += '<p><h3> <input type="hidden" name="content" value=' + activity +'></h3></p>'
    form += '<input type="submit" value="+1"></p>'
    form += '</form>'
    form = '<html><body>' + form + '</body></html>'
    return form

def put_form(activity):
    form ='<form name="input" action="" method="POST" enctype="text/plain">'
    form += '<p><h3> <input type="hidden" name="content" value=' + activity +'></h3></p>'
    form += '<input type="submit" value="Agregar a mi pagina"></p>'
    form += '</form>'
    form = '<html><body>' + form + '</body></html>'
    return form
    
@csrf_exempt 
def likes(request, url):
    user = request.user.username
    body = request.body
    act_id = str(body.split('content=')[1])
    table = Table_Likes(act = int(act_id) , user = user)
    table.save()
    return HttpResponseRedirect('http://localhost:1234/' + url)

@csrf_exempt 
def comments(request, url):
    user = request.user.username
    body = request.body
    body = re.split(r"[~\r\n]+", body)
    act_id = str(body[0].split('content=')[1])
    act_id = act_id.split("'\r'")[0]
    comment = body[1].split('comment=')[1]
    comment = comment.split("'\r'")[0]
    now = datetime.datetime.now()
    now += timedelta(hours=2)
    table = Table_Comments(act = str(act_id) , user = user, date = now, comment = comment)
    table.save()
    return HttpResponseRedirect('http://localhost:1234/actividad/' + act_id)
    
def slash_rss(request):
    pages = Table_User_Data.objects.all()
    content = '<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0"><channel><title>Paginas</title><description>Paginas de usuarios</description><link>http://localhost:1234/</link><ttl>1800</ttl>'
    for page in pages:
        try:
            content += '<item>'
            content += '<title><![CDATA[' + page.page_title + ']]></title>'
            content += '<description><![CDATA[' + 'Esta es la pagina de ' + page.user + '<br><br>Fecha de ultima modificacion: ' + str(page.date)[0:19] + '<br>' + '<br>' + "<a href=\"http://localhost:1234/" + page.user + '/rss">Pincha aqui' + '</a>' + ' para acceder al canal rss de este usuario]]></description>'
            content += '<link>http://localhost:1234/' + page.user + '</link>' 
            content += '</item>'
        except:
            pass
    acts = Table_Activity_Data.objects.filter().order_by("date")
    n = 0
    content += '<item><title><![CDATA[Actividades:]]></title>''<description><![CDATA[Listado de las diez proximas actividades]]></description></item>'
    for act in acts:
        if n < 10:
            try:
                content += '<item>'
                content += '<title><![CDATA[' + act.act_title + ']]></title>'
                content += '<description><![CDATA[' + '<br>Titulo: ' + act.act_title + '<br>Tipo: ' + act.event_type + '<br>Precio: ' + act.price + '<br>Fecha: ' + str(act.date)[0:10] + '<br>Hora: ' + str(act.time)[11:16] + '<br>Larga duracion: ' + act.is_long_term + ']]></description>'
                content += '<link>' + act.url + '</link>'
                content += '</item>'
            except:
                pass
            n += 1
    content += '</channel></rss>'
    return HttpResponse(content, content_type="application/rss+xml")

def user_rss(request, user):
    try:    
        table = Table_User_Data.objects.get(user=user)
        pages = Table_Selected_Acts.objects.filter(user=user).order_by("-selection_date")
        title = Table_User_Data.objects.get(user=user).page_title
        content = '<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0"><channel><title>' + title + '</title><description>Canal RSS de ' + user + '</description><link>http://localhost:1234/</link><ttl>1800</ttl>'
        for activities in pages:
            try:

                content += '<item>'
                act = Table_Activity_Data.objects.get(id = int(activities.act))
                content += '<title><![CDATA[' + act.act_title + ']]></title>'
                '<description><![CDATA[' + '<br>Titulo: ' + act.act_title + '<br>Tipo: ' + act.event_type + '<br>Precio: ' + act.price + '<br>Fecha: ' + str(act.date)[0:10] + '<br>Hora: ' + str(act.time)[11:16] + '<br>Larga duracion: ' + act.is_long_term + ']]></description>'
                content += '<link>' + act.url + '</link>'
                content += '</item>'
                content += '<item>'
                content += '<title><![CDATA[Mas Datos:]]></title>''<description><![CDATA[' + '<br>Fecha de la actividad: ' + str(act.date)[0:10] + '<br>Elegida en: ' + str(activities.selection_date)[0:19] + ']]></description>'
                content += '</item>'
                like_list = Table_Likes.objects.filter(act = activities.id)
                content += '<item>'
                content += '<title><![CDATA[Likes:]]></title>''<description><![CDATA[' + '<br>Esta actividad le gusta a ' + str(len(like_list)) + ' personas.]]></description>'
                content += '</item>'
            except:
                pass
        content += '</channel></rss>'
        return HttpResponse(content, content_type="application/rss+xml")
        
    except Table_User_Data.DoesNotExist:
        title = "Pagina no encontrada " 
        content = "No existe una pagina con ese nombre"
    
    if request.user.is_authenticated():
        init_user(user_visitor)
        dict_css = {'newcss': pass_css(request,user),'Titulo': title ,'Contenido': content, 'usuario': user_visitor, 'act': owner, 'comment': found_page, 'user': user}
        dict_css.update(csrf(request))
        return render_to_response("rss_auth.html", dict_css)

            
    else:
        dict_css = {"Titulo": title, "Contenido": content,"Redirect": user}
        dict_css.update(csrf(request))
        return render_to_response("rss_noauth.html", dict_css)
