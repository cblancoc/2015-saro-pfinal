from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
                          {'next_page': 'http://localhost:1234/'}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': 'static'}),
    url(r'^(.*)/rss$', 'act_app.views.user_rss'),
    url(r'^ayuda$', 'act_app.views.help'),
    url(r'^ayuda/$', 'act_app.views.help'),
    url(r'^todas$', 'act_app.views.all_act'),
    url(r'^todas/$', 'act_app.views.all_act'),
    url(r'^todas/date/(.*)$', 'act_app.views.all_act_date'),
    url(r'^todas/title/(.*)$', 'act_app.views.all_act_title'),
    url(r'^todas/duration/(.*)$', 'act_app.views.all_act_duration'),
    url(r'^todas/price/(.*)$', 'act_app.views.all_act_price'),
    #Parte opcional: generar rss de la pagina principal
    url(r'^rss$', 'act_app.views.slash_rss'),
    url(r'^rss/$', 'act_app.views.slash_rss'),
    #Parte opcional: poder comentar las revistas
    url(r'^comentarios/(.*)$', 'act_app.views.comments'),
    #Parte opcional: poder dar +1 a una noticia
    url(r'^like/(.*)$', 'act_app.views.likes'),
    url(r'^actividad/add/(.*)$', 'act_app.views.activities_add'),
    url(r'^actividad/(.*)$', 'act_app.views.activities'),
    url(r'^$', 'act_app.views.slash'),
    #URL que uso para recibir el formulario para cambiar la apariencia de la pagina (css)
    url(r'^css$', 'act_app.views.changecss'),
    url(r'^(.*)$', 'act_app.views.user'),
)
