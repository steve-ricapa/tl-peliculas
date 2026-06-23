import boto3
import json
import uuid
import os

def lambda_handler(event, context):
    try:
        body = event['body']
        if isinstance(body, str):
            body = json.loads(body)

        print(json.dumps({
            "tipo": "INFO",
            "log_datos": event
        }))

        tenant_id = body['tenant_id']
        pelicula_datos = body['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        print(json.dumps({
            "tipo": "INFO",
            "log_datos": pelicula
        }))

        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    except Exception as e:
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "error": str(e)
            }
        }))

        return {
            'statusCode': 500,
            'error': str(e)
        }
