from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from django.template import TemplateDoesNotExist
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from account import serializers, models
import mergin
import json
import os
from string import Template
import geopandas as gpd
from fiona import listlayers
import folium
from django.views.generic import TemplateView
import re
from django.contrib.auth import get_user_model





# Create your views here.
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def getnamespaceslist(request):
    if request.method == 'GET':
        try:
            mergin.MerginClient(login=request.session["username"], password=request.session["password"])
        except Exception as e:
            return JsonResponse({"exception": e.with_traceback(), "message":"Login or password is not matched with MerginMaps."}, status=401)    
        client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])

        try:
            client.workspaces_list()
        except:
            return JsonResponse({"status": "Error", "message": "An error occured, please try again later or consult to system admin"}, status=500)
        return JsonResponse(client.workspaces_list(), safe=False)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)

'''
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def getprojectslist(request):
    if request.method == 'POST':
        try:
            client = mergin.MerginClient(login="Ofiskontrol1", password="Erhan@2023")
        except:
            return JsonResponse({"status": "Unauthorized", "message":"Login or password is not matched with MerginMaps."}, status=401)
        try:
            
            json_data = json.loads(request.body.decode('UTF-8'))
            value = json_data.get("namespace")
            try:
                projects = client.projects_list(namespace=value)    
                return JsonResponse(projects, safe=False)
            except:
                return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            # return JsonResponse({"status": "ok", "key_value":value})
            # return JsonResponse(value, safe=False)
            
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON Format"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)
    # return JsonResponse(request.POST["name_of_namespace"])
'''


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def getprojectslist(request):
    User = get_user_model()
    
    if request.method == 'POST':
        try:
            client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])

            try:
                namespace = request.data["namespace"]
                if namespace:
                    projects = client.projects_list(namespace=namespace)   
                else:
                    projects = []
                return JsonResponse(projects, safe=False)
            except:
                return JsonResponse({"status": "Missing data", "message": "namespace data is required"}, status=403)
        except:
            return JsonResponse({"status": "Unauthorized", "message":"Login or password is not matched with MerginMaps."}, status=401)

    return JsonResponse(namespace, safe=False)
    # return JsonResponse(request.POST["name_of_namespace"])


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def projectinfo(request):
    if request.method == 'POST':
        try:
            client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])

            try:
                project_path_or_id = request.data["project_path_or_id"]
                try:
                    print(project_path_or_id)
                    res = client.project_info(project_path_or_id=project_path_or_id)   
                    return JsonResponse(res, safe=False)
                except:
                    return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            except:
                return JsonResponse({"status": "Missing data", "message": "namespace data is required"}, status=403)
        except:
            return JsonResponse({"status": "Unauthorized", "message":"Login or password is not matched with MerginMaps."}, status=401)

    
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def projectfilehistoryinfo(request):
    if request.method == 'POST':
        try:
            client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])
            try:
                project_path = request.data["project_path"]
                file_path = request.data["file_path"]
                try:
                    res = client.project_file_history_info(project_path=project_path, file_path=file_path)   
                    return JsonResponse(res, safe=False)
                except:
                    return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            except:
                return JsonResponse({"status": "Missing data", "message": "namespace data is required"}, status=403)
        except:
            return JsonResponse({"status": "Unauthorized", "message":"Login or password is not matched with MerginMaps."}, status=401)





@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def projectversioninfo(request):
    if request.method == 'POST':
        try:
            client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])
            try:
                project_path = request.data["project_path"]
                version_info = request.data["version_info"]
                try:
                    res = client.project_version_info(project_path=project_path, version=version_info)
                    return JsonResponse(res, safe=False)
                except:
                    return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            except:
                return JsonResponse({"status": "Missing data", "message": "namespace data is required"}, status=403)
        except:
            return JsonResponse({"status": "Unauthorized", "message":"Login or password is not matched with MerginMaps."}, status=401)






# resp = client.project_file_changeset_info("ERHAN CALISMALAR/MELIKGAZI", "KAPI.gpkg", "v11") important
'''
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def projectfilechangesetinfo(request):
    if request.method == 'POST':
        try:
            mergin.MerginClient(login="Ofiskontrol1", password="Erhan@2023")
        except:
            return JsonResponse({"status": "Unauthorized", "message":"Login or password is not matched with MerginMaps."}, status=401)        
        try:
            client = mergin.MerginClient(login="Ofiskontrol1", password="Erhan@2023")
            json_data = json.loads(request.body.decode('UTF-8'))
            project_path = json_data.get("project_path")
            file_path = json_data.get("file_path")
            version_info = json_data.get("version_info")
            if not (project_path and version_info and file_path) :
                return JsonResponse({"status": "error", "message": "Project path and file path must be supplied to receive data"})
            try:
                client.project_file_changeset_info(project_path=project_path, file_path=file_path, version=version_info)
            except:
                return JsonResponse({"status": "error", "message": "Not Found"},status=404)
            
            res = client.project_file_changeset_info(project_path=project_path, file_path=file_path, version=version_info)
            return JsonResponse(res, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON Format"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"})
    
'''

'''
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def projectfilechangesetinfo(request):
    if request.method == 'POST':
        try:
            client = mergin.MerginClient(login="Ofiskontrol1", password="Erhan@2023")
            try:
                project_path = request.data["project_path"]
                file_path = request.data["file_path"]
                version_info = request.data["version_info"]
                
                try:
                    res = client.project_file_changeset_info(project_path=project_path, file_path=file_path, version=version_info)
                    
                    return JsonResponse(res, safe=False)
                except:
                    return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            except:
                return JsonResponse({"status": "Missing data", "message": "namespace data is required"}, status=403)
        except:
            return JsonResponse({"status": "Unauthorized", "message":"Login or password is not matched with MerginMaps."}, status=401)
'''


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def projectfilechangesetinfo(request):
    if request.method == 'POST':
        client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])

        project_path = request.data["project_path"]
        file_path = request.data["file_path"]
        version_info = request.data["version_info"]
        res = client.project_file_changeset_info(project_path=project_path, file_path=file_path, version=version_info)
        return JsonResponse(res, safe=False)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def receiveversions(request):
    if request.method == "POST":
        try:
            client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])

            try:
                project_path = request.data["project_path"]
                try:
                    res = client.project_versions(project_path=project_path, since=None, to=None)
                    
                    return JsonResponse(res, safe=False)
                except:
                    return JsonResponse({"status": "error", "message": "Not found"}, status=404)
            except:
                return JsonResponse({"status": "Missing data", "message": "Project path must be specified"})
        except:
            return JsonResponse({"status":"error", "message": "Not Found"}, status=404)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def doesExist(request):
    if request.method == 'POST':
        namespace = request.data["namespace"]
        project_name = request.data["project_name"]
        path = './../projects/'+str(project_name)
        print(path)
        doesExist = os.path.exists(path)
        return JsonResponse({"doesExist": doesExist}, safe=False)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def doesmapexist(request):
    if request.method == "POST":
        res = []
        selected_project = request.data["selected_project"]
        file_name = request.data["file_name"]
        template_path = f"./mergintransactions/templates/{selected_project}/{file_name}.geojson"

        doesExist = os.path.exists(template_path)
        return JsonResponse({"doesExist": doesExist}, safe=False)
        

@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def download_project(request):
    if request.method == 'POST':
        client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])
        namespace = request.data["namespace"]
        project_name = request.data["project_name"]
        path = "./../projects/"+str(project_name)
        project_path = str(namespace+"/"+project_name)
        # res = client.download_project(project_path="ERHAN CALISMALAR/PROJE_ORNEK", directory=path, version=None)
        res = client.download_project(project_path=project_path, directory=path, version=None)
        return JsonResponse(res, safe=False)



@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def pullchanges(request):
    if request.method == 'POST':
        selected_project = request.data['project_name']
        path = "./../projects/"+str(selected_project)

        client = mergin.MerginClient(login=request.session["username"], password=request.session["password"])
        res = client.pull_project(directory=path)
        # in there you have to update ALL geojson files in "correct path"... Maybe delete all files and regenerate them???
        # first, list all of them
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # save_path = os.path.join(BASE_DIR, 'mergintransactions', 'templates', f'{selected_project}' ,f'{file_name}.geojson')
        save_path = os.path.join(BASE_DIR, 'mergintransactions', 'templates', f'{selected_project}')
        # list all geojson files in path
            # Define the path variable
        
        # Resolve the absolute path (optional, for better handling of relative paths)
        resolved_path = os.path.abspath(path)

        # Check if the directory exists
        if os.path.exists(resolved_path) and os.path.isdir(resolved_path):
            # List all .geojson files in the directory
            gpkg_files = [file for file in os.listdir(resolved_path) if file.endswith('.gpkg')]
            for x in range(len(gpkg_files)):
                print(path+'/'+gpkg_files[x])
                gdf = gpd.read_file(path+'/'+gpkg_files[x])
                filen = gpkg_files[x].replace('.gpkg', '.geojson')
                print("file name = ", gpkg_files[x])
                save_path_in_loop = os.path.join(BASE_DIR, 'mergintransactions', 'templates', f'{selected_project}', filen)
                print("save_path_in_loop", save_path_in_loop)
                print("filen = ", filen)
                # now save them with name of filen(to be changed)
                if not os.path.exists(os.path.dirname(save_path_in_loop)):
                    os.makedirs(os.path.dirname(save_path_in_loop))
                gdf.to_file(save_path_in_loop, driver='GeoJSON')
        else:
            print(f"The directory {resolved_path} does not exist or is not accessible.")



        '''
        if os.path.exists(save_path) and os.listdir(save_path):
            geojson_files = [file for file in os.listdir(save_path) if file.endswith('.geojson')]
            print("GeoJSON files: ", geojson_files)
            for file in os.listdir(save_path):
                if file.endswith('.geojson'):
                    print("path = ", path+'/'+file)
        '''
        # ./../projects/PROJE_ORNEK/POTEAU.gpkg
        # add geojson_files to path


        return JsonResponse(res, safe=False)
    




@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def return_file_names(request):
    if request.method == "POST":
        path = request.data["path"]
        # list to store files
        res = []
        # Iterate directory
        for file in os.listdir(path):
            # check only text files
            if file.endswith('.gpkg'):
                res.append(file)
        print(res)
        return JsonResponse({"files": res}, safe=False)

@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def return_file_content(request):
    if request.method == "POST":
        path = request.data["path"]
        gdf = gpd.read_file(path)
        # Dictionary to hold GeoDataFrames for each layer
        print("Inreturnfilecontent\n")
        print(path)
        try:
            layers = listlayers(path)
            data = {}
            json_data = {}

            # Loop through each layer and read it into a GeoDataFrame
            for layer_name in layers:
                    gdf = gpd.read_file(path, layer=layer_name)
    
                    # Convert GeoDataFrame to GeoJSON format
                    json_str = gdf.to_json()
                    
                    # Store the JSON string in the dictionary
                    json_data[layer_name] = json.loads(json_str) 
            return JsonResponse({"data":json_data}, safe=False)
        except:
            return JsonResponse({"status": "false"}, safe=False)


@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def filter_gpkg_file(request):
    if request.method == "POST":
        path = request.data["path"]
        filename = request.data["filename"]
        filtered_data = request.data["filtered_data"]
        gdf = gpd.read_file(path)
        # Dictionary to hold GeoDataFrames for each layer

        try:
            if not path or not filtered_data:
                raise ValueError("Missing required fields: 'path' or 'filtered_data'")

            layers = listlayers(path)
            data = {}
            json_data = {}
            filtered_data_as_json_array = json.loads(filtered_data)


            # Loop through each layer and read it into a GeoDataFrame
            for layer_name in layers:
                    gdf = gpd.read_file(path, layer=layer_name)
    
                    # Convert GeoDataFrame to GeoJSON format
                    json_str = gdf.to_json()
                    
                    # Store the JSON string in the dictionary
                    json_data[layer_name] = json.loads(json_str) 
            # print(json_data[filename.replace(".gpkg", "")]['features'])    
            '''
            for data in json_data[filename.replace(".gpkg", "")]['features']:
                print(data['properties'])
            '''
            print("SSS")
            num = 0
            for data in json_data[filename.replace(".gpkg", "")]['features']:
                for icd in filtered_data_as_json_array:
                    if icd == data['properties']:
                        num += 1
            # print(num)
            # print(filename)
            names_to_remove = [item for item in filtered_data_as_json_array]
            filtered_records = [record for record in json_data[filename.replace(".gpkg", "")]['features'] if record["properties"] in names_to_remove]
            # print(len(filtered_records))
            json_data[filename.replace(".gpkg", "")]['features'] = filtered_records
            # print(names_to_remove)
            return JsonResponse({"data":json_data}, safe=False)
        except Exception as e:
                # Return detailed exception message for debugging
            return JsonResponse({"status": "false", "error": str(e)}, safe=False)
        # return JsonResponse({"path": path, "filename": filename, "filtered_data": filtered_data}, safe=False)
    
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def handle_with_map(request):
    if request.method == "POST":
        
        path = request.data["path"]
        file_name= request.data["file_name"]
        partial_path = request.data["partial_path"]
        selected_project = request.data["selected_project"]
        gdf = gpd.read_file(path)
        print("In handle_with_map\n")
        print(path)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # save_path = os.path.join(BASE_DIR, 'client', 'public', 'static', f'{selected_project}',f'{file_name}.html')
        save_path = os.path.join(BASE_DIR, 'mergintransactions', 'templates', f'{selected_project}' ,f'{file_name}.geojson')
        # Ensure the directory exists
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        gdf.to_file(save_path, driver='GeoJSON')
        return JsonResponse({"status": "Generated!"})

    
'''
@rest_decorators.api_view(["POST"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def printmap(request):
    # Get the filename from the request data
    filename = request.GET.get('filename')
    selected_project = request.GET.get('selected_project')    


    if filename:
        template_path = f'maps/{selected_project}/{filename}.html'
        
        try:
            # Render the corresponding HTML file
            return render(request, template_path)
        except TemplateDoesNotExist:
            raise Http404(f"Template '{template_path}' not found.")
    else:
        return HttpResponse("Filename not provided.", status=400)




'''

@rest_decorators.api_view(["POST"])
# @rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def handleservingmap(request):

    selected_project = request.data["selected_project"]
    file_name = request.data["file_name"]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gpkg_file_path = os.path.join(BASE_DIR, 'mergintransactions', 'templates', f'{selected_project}' ,f'{file_name}.geojson')

    try:
        print("In handleservingmap\n")
        print(gpkg_file_path)
        # Load the GPKG file into a GeoDataFrame
        gdf = gpd.read_file(gpkg_file_path)

        # Convert the GeoDataFrame to GeoJSON format
        geojson_str = gdf.to_json()

        # Convert the GeoJSON string to a Python dict
        geojson_data = json.loads(geojson_str)

        # Return the GeoJSON as a JsonResponse
        return JsonResponse(geojson_data, safe=False)

    except Exception as e:
            # Handle errors and return an error message
            return JsonResponse({"error": str(e)}, status=400)
    