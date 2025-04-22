import boto3
import time
import json
import concurrent.futures
import asyncio

# class Model:
#     def __init__(self, bucket, document_data):
#         self.textract = boto3.client('textract')
#         self.s3 = boto3.client('s3')

#         self.bucket = bucket
#         self.image = document_data.image
#         self.file_name = document_data.filename
        
#     # Filename: il path locale del file da caricare
#     # Bucket: il nome del bucket S3
#     # Key: il nome del file (e percorso virtuale) in S3
#     def upload_file(self):
#         self.s3.upload_file(self.file_name, self.bucket, 'Test/Test.jpg')

#     def response(self):
#         self.response = self.textract.start_document_analysis( 
#             DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': 'Test/Test.jpg'}},
#             FeatureTypes=["TABLES", "FORMS"]
#         )        

#         self.job_id = self.response['JobId']
#         print(f"Job ID: {self.job_id}")

#     def analyze_document(self):
#         while True:
#             result = self.textract.get_document_analysis(JobId=self.job_id)
        
#             if result['JobStatus'] in ['SUCCEEDED', 'FAILED']:
#                break
        
#             print("In attesa di completamento del lavoro...")
#             time.sleep(5)

#         print("Documento analizzato")    

#         with open('output.json', 'w') as json_file:
#             json.dump(result, json_file, indent=4)
        
class Model:
    def __init__(self, document_data):
        self.textract = boto3.client('textract')
        self.file_name = document_data.filename_image_processed
        self.executor = concurrent.futures.ThreadPoolExecutor()

    async def analyze_document(self):
        loop = asyncio.get_running_loop()

        with open(self.file_name, 'rb') as file:
            document_bytes = file.read()

        result = await loop.run_in_executor(
            self.executor,
            lambda: self.textract.analyze_document(
                Document={'Bytes': document_bytes},
                FeatureTypes=["TABLES", "FORMS"]
            )
        )

        with open('output.json', 'w') as f:
            json.dump(result, f, indent=4)

        print("Analisi completata.")
        return result
