from django.urls import path
from mergintransactions import views


app_name = "mergintransactions"

urlpatterns = [
    path('getnamespaceslist', views.getnamespaceslist),
    path('getprojectslist', views.getprojectslist),
    #path('pullproject', views.pullprojecthistory),
    path('projectinfo', views.projectinfo),
    path('projectfilehistoryinfo', views.projectfilehistoryinfo),
    path('projectversioninfo', views.projectversioninfo),
    path('projectfilechangesetinfo', views.projectfilechangesetinfo),
    path('receiveversions', views.receiveversions),
    path('downloadproject', views.download_project),
    path('pullchanges', views.pullchanges),
    path('doesexist', views.doesExist),
    path('returnfilenames', views.return_file_names),
    path('returnfilecontent', views.return_file_content),
    path('handlewithmap', views.handle_with_map),
#     path('printmap/<filename>/<selected_project>', views.printmap, name='printmap'),
    path('map', views.handleservingmap),
    path('doesmapexist', views.doesmapexist),
    path('filtergpkgfile', views.filter_gpkg_file)

]
