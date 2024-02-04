import azure.functions as func
import logging
import os
from azure.storage.blob import BlobServiceClient
import fastavro
import io
from tfg_functions import create_student_html, create_course_html

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="userlogins")
def userlogins(req: func.HttpRequest) -> func.HttpResponse:

    # Parametro que requiere el endpoint. ID del alumno
    id = req.params.get('id')
    if not id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            id = req_body.get('id')

    if id:
        try:
            alberto_storage_connection_str = os.environ["AzureWebJobsStorage"]
            blob_service_client = BlobServiceClient.from_connection_string(alberto_storage_connection_str)
            container_client = blob_service_client.get_container_client("aggregate")

            archivo = container_client.get_blob_client(f"users/{id}/aggregate.avro").download_blob().readall()
            reader = fastavro.reader(io.BytesIO(archivo))
            record_list = []
            for record in reader:
                record_list.append(record)

            html_respuesta = create_student_html(record_list)

            return func.HttpResponse(
                html_respuesta,
                status_code=200
            )
        except Exception as e:
            return func.HttpResponse(
                f"Ocurrió un error\n: {str(e)}", 
                status_code=500)
    else:
        return func.HttpResponse(
             f"Es necesario introducir el campo 'id' del usuario",
             status_code=400
        )

@app.route(route="courselogins")
def courselogins(req: func.HttpRequest) -> func.HttpResponse:

    # Parametro que requiere el endpoint. ID del curso
    id = req.params.get('id')

    if not id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            id = req_body.get('id')

    if id:
        try:
            alberto_storage_connection_str = os.environ["AzureWebJobsStorage"]
            blob_service_client = BlobServiceClient.from_connection_string(alberto_storage_connection_str)
            container_client = blob_service_client.get_container_client("aggregate")

            archivo = container_client.get_blob_client(f"courses/{id}/aggregate.avro").download_blob().readall()
            reader = fastavro.reader(io.BytesIO(archivo))
            record_list = []
            for record in reader:
                record_list.append(record)

            html_respuesta = create_course_html(record_list)

            return func.HttpResponse(
                html_respuesta,
                status_code=200
            )
        except Exception as e:
            return func.HttpResponse(
                f"Ocurrió un error\n: {str(e)}", 
                status_code=500)
    else:
        return func.HttpResponse(
             f"Es necesario introducir el campo 'id' del curso",
             status_code=400
        )