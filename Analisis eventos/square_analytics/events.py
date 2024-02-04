import pandas as pd
import numpy as np
import os
from azure.storage.blob import ContainerClient
from fastavro import reader, writer, parse_schema
import io
import json

MAX_EVENTS = int(os.environ["MAX_EVENTS"])


class Events:
    def __init__(self, events_container, bin_container=None, after=""):
        self.__retrieve_events(events_container, bin_container, after)
        self.dataframe = pd.DataFrame(self.__events)

    def __retrieve_events(self, events_container, bin_container, after):
        blob_list = [blob for blob in events_container.container.list_blobs()]
        blob_list.sort(key=lambda b: b.name)

        self.__events = []

        events_number = 0

        for i_blob, blob in enumerate(blob_list):
            if blob.size > 508:

                blob_client = ContainerClient.get_blob_client(
                    events_container.container, blob=blob.name
                )
                fileReader = blob_client.download_blob().readall()
                print("Downloaded a non empty blob: " + blob.name)

                events_list = self.__process_blob(fileReader)

                events_number += len(events_list)

                if (events_number > MAX_EVENTS) & (i_blob > 1):

                    break

                self.__events += events_list

                if bin_container is not None:
                    ContainerClient.upload_blob(
                        bin_container.container,
                        name=blob.name,
                        data=fileReader,
                        overwrite=True,
                    )
                    events_container.container.delete_blob(blob.name)

        print(f"Number of downloaded events: {len(self.__events)}")
        events_container.container.close()

        if bin_container is not None:
            bin_container.container.close()

    def __process_blob(self, filename):
        with io.BytesIO(filename) as f:
            events_list = []

            avro_reader = reader(f)

            for reading in avro_reader:
                parsed_json = json.loads(reading["Body"])

                events_list.append(parsed_json)

        return events_list
