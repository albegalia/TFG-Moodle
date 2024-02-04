from dotenv import load_dotenv
import os

load_dotenv()

alberto_storage_connection_str = os.environ["ALBERTO_STORAGE_CONNECTION_STR"]
from square_analytics.container import Container
from square_analytics.events import Events

# list blobs in the capture container
capture_container = Container("capture", alberto_storage_connection_str)
print(capture_container.list_blobs())

# download events

events = Events(capture_container)
print(events.dataframe)
