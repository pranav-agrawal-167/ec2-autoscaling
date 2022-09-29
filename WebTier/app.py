from flask import Flask, request
import boto3
import base64
import uuid
import os
from datetime import datetime

AWS_REGION='us-east-1' #Enter your AWS region here

AWS_ACCESS_KEY="Enter your access key here"
AWS_SECRET_ACCESS_KEY="Enter your secret access key here"

INPUT_QUEUE_URL="Enter your input queue URL here"
INPUT_QUEUE_NAME="InputQueue" #your input queue name

session=boto3.session.Session()
sqs_resource = session.resource("sqs",region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


app = Flask(__name__)

@app.route("/",methods = ['POST'])
def read_image_file():
    input_queue = sqs_resource.get_queue_by_name(QueueName=INPUT_QUEUE_NAME)

    uploaded_file = request.files['image_file']

    if uploaded_file.filename != '':
        uploaded_file.save("requests_files/" + uploaded_file.filename)

        with open("requests_files/" + uploaded_file.filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            image_file.close()

        msg_uuid=str(uuid.uuid4())
        
        try:

            input_queue.send_message(MessageBody=encoded_string, MessageAttributes={
            'ImageName': {
                'StringValue': uploaded_file.filename,
                'DataType': 'String'
            },
            'UID': {
                'StringValue': msg_uuid,
                'DataType': 'String'
            }
        })

        except Exception as e:
            print(f"Exception while sending message to SQS ::: " + uploaded_file.filename + " ::: {repr(e)}")

        print("Message sent for " + uploaded_file.filename + " at : ",datetime.now()) 

        os.system("rm requests_files/" + str(uploaded_file.filename))

    result=None

    while result is None:
        if os.path.exists("requests_files/" + msg_uuid + ".txt"):
            with open("requests_files/" + msg_uuid + ".txt") as file:
                result = file.read()
                print("Result for " + uploaded_file.filename + " : ",result)
            if result:
                os.system("rm requests_files/" + msg_uuid + ".txt")
                return result
        
    print("Exiting...")

if __name__ == "__main__":
    app.run()
