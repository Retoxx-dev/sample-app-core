# from azure.identity import DefaultAzureCredential - to be changed for managed identity later
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from fastapi import UploadFile

import settings

from datetime import datetime, timedelta


class FileManager:
    def __init__(self):
        self.account_url = settings.STORAGE_ACCOUNT_URL
        self.blob_service_client = BlobServiceClient(self.account_url, credential=settings.STORAGE_ACCOUNT_ACCESS_KEY)
        self.container_name = "profiles"
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    async def is_file_type_ok(self, file: UploadFile):
        allowed_file_types = ["image/jpeg", "image/png", "image/jpg"]
        return file.content_type in allowed_file_types

    # async def is_file_size_ok(self, file: UploadFile):
    #     max_file_size = 1024 * 1024 * 2
    #     content = await file.read()
    #     file_size = len(content)
    #     return file_size <= max_file_size

    async def generate_file_name(self, file: UploadFile):
        file_base, file_extension = file.filename.split(".")
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        generated_file_name = f"{current_datetime}.{file_extension}"
        return generated_file_name

    async def upload_file(self, user_id, file: UploadFile):
        file_name = await self.generate_file_name(file)
        async with self.blob_service_client:
            try:
                blob_client = self.container_client.get_blob_client(blob=f"{user_id}/{file_name}")

                f = await file.read()
                await blob_client.upload_blob(f)
                return file_name
            except Exception as e:
                print(e)
            finally:
                await file.close()

    async def get_file_with_sas(self, user_id, file_name):
        async with self.blob_service_client:
            try:
                blob_client = self.container_client.get_blob_client(blob=f"{user_id}/{file_name}")

                sas_token = generate_blob_sas(
                    account_name=blob_client.account_name,
                    container_name=blob_client.container_name,
                    blob_name=blob_client.blob_name,
                    account_key=blob_client.credential.account_key,
                    permission=BlobSasPermissions(read=True),
                    expiry=datetime.utcnow() + timedelta(minutes=30)
                )

                return sas_token
            except Exception as e:
                print(e)
