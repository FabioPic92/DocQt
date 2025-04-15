import boto3
import time
import json

class Model:
    def __init__(self, bucket, document_data):
        self.textract = boto3.client('textract')
        self.s3 = boto3.client('s3')

        self.bucket = bucket
        self.image = document_data.image

    # Filename: il path locale del file da caricare
    # Bucket: il nome del bucket S3
    # Key: il nome del file (e percorso virtuale) in S3
    def upload_file(self):
        self.s3.upload_file(self.image, self.bucket, 'Test/Test.jpg')

    def response(self):
        self.response = self.textract.start_document_analysis( 
            DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': 'Test/Test.jpg'}},
            FeatureTypes=["TABLES", "FORMS"]
        )        

        self.job_id = self.response['JobId']
        print(f"Job ID: {self.job_id}")

    def analyze_document(self):
        while True:
            result = self.textract.get_document_analysis(JobId=self.job_id)
        
            if result['JobStatus'] in ['SUCCEEDED', 'FAILED']:
               break
        
            print("In attesa di completamento del lavoro...")
            time.sleep(5)

        print("Documento analizzato")    

        with open('output.json', 'w') as json_file:
            json.dump(result, json_file, indent=4)
        

