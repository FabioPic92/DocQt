import boto3
import time

#Sistemare Path File
class Model:
    def __init__(self, bucket):
        self.textract = boto3.client('textract')
        self.s3 = boto3.client('s3')

        self.bucket = bucket

    # Filename: il path locale del file da caricare
    # Bucket: il nome del bucket S3
    # Key: il nome del file (e percorso virtuale) in S3
    def upload_file(self, file):
        self.s3.upload_file(file, self.bucket, pathTest)

    def response(self):
        response = self.textract.start_document_analysis( 
            DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': pathTest}},
            FeatureTypes=["TABLES", "FORMS"]
        )        

        print(response)

        self.job_id = response['JobId']
        print(f"Job ID: {self.job_id}")

    def analyze_document(self):
        while True:
            result = textract.get_document_analysis(JobId=job_id)
        
            if result['JobStatus'] in ['SUCCEEDED', 'FAILED']:
               break
        
            print("In attesa di completamento del lavoro...")
            time.sleep(5)

        print("Documento analizzato")    

        text = ''
        if result['JobStatus'] == 'SUCCEEDED':
            for item in result['Blocks']:
                if item['BlockType'] == 'LINE':
                    text = text + " " + item['Text']

        else:
            print(f"Analisi fallita: {result.get('ErrorMessage', 'Nessun errore specificato')}")

        if not fileTest.lower().endswith('.pdf') and not fileTest.lower().endswith('.png'):
            draw_boxes_on_image(TestImage, result)


        comprehend_client = boto3.client('comprehend')

        responseCom = comprehend_client.detect_entities(Text=text, LanguageCode='it')

        TestCsv = os.path.join(pathCsv, 'Test.csv')  

        df = pd.DataFrame(responseCom['Entities'])
        df.to_csv(TestCsv, index=False)

        fileJson = pathTest + '.json'

        TestJson = os.path.join(pathJson, fileJson)

        with open(TestJson, 'w') as json_file:
            json.dump(result, json_file, indent=4)
        

        TestPath = os.path.join(pathData, pathTest)
        AnalyzeDocument(TestPath, pathTest)

        execution_time = time.time() - start_time
        print(f"Tempo di esecuzione: {execution_time} secondi")

