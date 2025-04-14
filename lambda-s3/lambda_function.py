import boto3
import urllib.parse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    source_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Skip if the file is already in the destination folder
    if source_key.startswith('processed/'):
        return {
            'statusCode': 200,
            'body': f"File already processed: {source_key}"
        }

    # Define the destination key (prefix to move to 'processed/' folder)
    destination_key = f"processed/{source_key.split('/')[-1]}"

    try:
        # Copy the object
        s3.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': source_key},
            Key=destination_key
        )

        # Delete the original object
        s3.delete_object(Bucket=bucket_name, Key=source_key)

        return {
            'statusCode': 200,
            'body': f"Moved {source_key} to {destination_key}"
        }

    except Exception as e:
        print(e)
        raise e
