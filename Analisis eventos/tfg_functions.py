import mariadb
import pandas as pd
import fastavro
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import os

load_dotenv()
alberto_storage_connection_str = os.environ["ALBERTO_STORAGE_CONNECTION_STR"]

def assign_not_submitted_list(courseid: int, assignmentid: str, events: pd.DataFrame):
    """
    Lista de alumnos que no han subido tarea en el curso y tarea especificados.

    :param courseid: ID del curso
    :param assignmentid: Instancia de la ID de la tarea (no confundir con su ID real)
    :param events: Lista de eventos de Moodle
    :returns: Dataframe con la información de los alumnos sin subir la tarea
    """

    event = '\\assignsubmission_file\\event\\submission_created'

    conn = mariadb.connect(
        user="root", host="localhost", database="bitnami_moodle"
    )
    cur = conn.cursor()
    cur.execute(
        f"SELECT u.id, u.firstname, u.lastname, u.email FROM mdl_user_enrolments ue JOIN mdl_user u ON ue.userid = u.id JOIN mdl_enrol e ON ue.enrolid = e.id WHERE e.courseid = {courseid}"
    )
    results = cur.fetchall()
    cur.close()

    df_users_course = pd.DataFrame(
        results, 
        columns=['userid', 'firstname', 'lastname', 'email']
    )

    df_tareas_subidas = events.loc[
        (events['eventname'] == event) & 
        (events['contextinstanceid'] == assignmentid)
    ]

    studentslist = df_users_course.loc[
        ~df_users_course['userid'].isin(
            df_tareas_subidas['userid'].astype('int64')
        )
    ]
    
    return studentslist

def assign_not_submitted(userid: str, assignmentid: str, events: pd.DataFrame):
    """
    Alumno que no ha subido la tarea especificada.

    :param userid: 
    :param courseid: ID del curso
    :param assignmentid: Instancia de la ID de la tarea (no confundir con su ID real)
    :param events: Lista de eventos de Moodle
    :returns: Si el alumno ha subido o no la tarea
    """

    event = '\\assignsubmission_file\\event\\submission_created'

    tarea_alumnodf = events.loc[
        (events['userid'] == userid) & 
        (events['eventname'] == event) &
        (events['contextinstanceid'] == assignmentid)
    ]

    if tarea_alumnodf.empty:
        return (f'El alumno con ID {userid} no ha subido la tarea')
    else:
        return (f'El alumno con ID {userid} ha subido la tarea')

def students_not_logged(courseid: int, n_days: int, events: pd.DataFrame):
    """
    Lista de alumnos que no han iniciado sesión en los {n_days} últimos días.

    :param courseid: ID del curso
    :param n_days: Numero de días que queremos comprobar
    :param events: Lista de eventos de Moodle
    :returns: Dataframe con la información de los alumnos sin logearse en dos días
    """

    event = '\\core\\event\\user_loggedin'

    conn = mariadb.connect(
        user="root", host="localhost", database="bitnami_moodle"
    )
    cur = conn.cursor()
    cur.execute(
        f"SELECT u.id, u.firstname, u.lastname, u.email FROM mdl_user_enrolments ue JOIN mdl_user u ON ue.userid = u.id JOIN mdl_enrol e ON ue.enrolid = e.id WHERE e.courseid = {courseid}"
    )
    results = cur.fetchall()
    cur.close()

    df_users_course = pd.DataFrame(
        results, 
        columns=['userid', 'firstname', 'lastname', 'email']
    )

    days_ago = int(
        (pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=n_days)).timestamp()
    )

    df_logins = events.loc[
        (events['eventname'] == event) & 
        (events['timecreated'] > days_ago)
    ]

    studentslist = df_users_course.loc[
        ~df_users_course['userid'].isin(df_logins['userid'].astype('int64'))
    ]
    
    return studentslist

def last_login_date(userid: str, events: pd.DataFrame):
    """
    Fecha del último login del alumno especificado.

    :param userid: ID del curso
    :param events: Lista de eventos de Moodle
    :returns: La fecha con tz='UTC' del último login del alumno especificado
    """

    event = '\\core\\event\\user_loggedin'

    last_login = events.loc[
        (events['userid'] == userid) & (events['eventname'] == event)
    ]['timecreated'].max()

    fecha = pd.to_datetime(last_login, unit='s').strftime('%d-%m-%Y %H:%M:%S')
    
    return (f'Último login del alumno con ID {userid}: {fecha}')

def create_user_avro(schema: dict, daily_visits: pd.DataFrame, id: str):
    """
    Crea archivo avro a partir de un esquema y datos correspondientes.

    :param schema: Diccionario con el esquema del archivo avro
    :param user_info: Datos con los que rellenar dicho diccionario
    :returns: El avro creado en forma de lista
    """

    info_test = {}
    info_test["daily_visits"] = daily_visits.to_dict("records")
    info_test["id"] = id

    with open("aggregate.avro", "wb") as f:
        fastavro.writer(f, schema, [info_test])

    with open("aggregate.avro", "rb") as f:
        reader = fastavro.reader(f)
        # Iterate over the records and print them
        record_list = []
        for record in reader:
            record_list.append(record)
    return(record_list)

def create_course_avro(schema: dict, tasks: pd.DataFrame):
    """
    Crea archivo avro a partir de un esquema y datos correspondientes.

    :param schema: Diccionario con el esquema del archivo avro
    :param user_info: Datos con los que rellenar dicho diccionario
    :returns: El avro creado en forma de lista
    """

    info_test = {}
    info_test["tasks"] = tasks.to_dict("records")

    with open("aggregate.avro", "wb") as f:
        fastavro.writer(f, schema, [info_test])

    with open("aggregate.avro", "rb") as f:
        reader = fastavro.reader(f)
        # Iterate over the records and print them
        record_list = []
        for record in reader:
            record_list.append(record)
    return(record_list)

def upload_avro(is_user: bool, id: str):

    blob_service_client = BlobServiceClient.from_connection_string(alberto_storage_connection_str)

    # Nombre del contenedor
    container_name = "aggregate"
    # Ruta del archivo .avro (relativa desde este archivo python)
    file_path = "aggregate.avro"
    # Nombre del archivo .avro que vamos a subir al contenedor
    file_name = "aggregate.avro"
    # Directorio en el que se cargará el archivo .avro en el contenedor
    if is_user:
        directory_name = f"users/{id}/"
    else:
        directory_name = f"courses/{id}/"

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=directory_name + file_name)

    # Cargar el archivo .avro en el contenedor
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)