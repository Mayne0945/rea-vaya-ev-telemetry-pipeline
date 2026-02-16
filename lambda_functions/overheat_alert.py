import json
import boto3
import awswrangler as wr
import pandas as pd
from datetime import datetime

# Initialize S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # 1. Get Source Info
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print(f"📥 Processing New File: s3://{bucket}/{key}")
        
        # 2. Read Raw JSON
        response = s3_client.get_object(Bucket=bucket, Key=key)
        raw_content = response['Body'].read().decode('utf-8')
        json_content = json.loads(raw_content)
        
        # 3. UNWRAP THE SHADOW STATE
        if 'state' in json_content and 'reported' in json_content['state']:
            clean_data = json_content['state']['reported']
        else:
            # Fallback if you send flat data later
            clean_data = json_content

        # 4. Convert to Flat DataFrame
        # This turns 'telemetry': {'rpm': 3000} into column 'telemetry.rpm'
        df = pd.json_normalize(clean_data)
        
        # 5. Add Partition Column
        df['date'] = datetime.now().strftime('%Y-%m-%d')
        
        # 6. Write to Parquet
        # prevents the "Overwrite" loop and registers the table automatically.
        wr.s3.to_parquet(
            df=df,
            path="s3://ev-telemetry-vault-mayne/Silver/",
            dataset=True,
            mode="append",      # adds to existing data
            database="ev_sentimel_db",
            table="inclusive_ev_fleet",
            partition_cols=["date"]
        )
        
        print(f"🚀 Success! Appended to inclusive_ev_fleet.")
        return "Success"

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise e