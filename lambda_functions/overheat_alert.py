import json
import boto3

# Initialize the SNS client (Simple Notification Service)
sns = boto3.client('sns')

CRITICAL_TEMP_THRESHOLD = 60.0 
TOPIC_ARN = "arn:aws:sns:eu-west-1:YOUR_ACCOUNT_ID:EV_Overheat_Alerts" # We will get this ARN from AWS Console later

def lambda_handler(event, context):
    # 1. Parse the incoming data from IoT Core
    # (AWS passes the data in the 'event' object)
    try:
        vehicle_id = event['vehicle_id']
        battery_temp = float(event['battery_temp'])
        timestamp = event['timestamp']
        
        print(f"Analyzing data for {vehicle_id}: Temp is {battery_temp}°C")

        # 2. Check logic: Is it too hot?
        if battery_temp > CRITICAL_TEMP_THRESHOLD:
            message = (
                f"⚠️ CRITICAL ALERT: Vehicle {vehicle_id} is OVERHEATING!\n"
                f"Current Temp: {battery_temp}°C\n"
                f"Time: {timestamp}\n"
                f"Action: Immediate cooldown required."
            )
            
            # 3. Trigger the SNS Alert (Send Email/SMS)
            response = sns.publish(
                TopicArn=TOPIC_ARN,
                Message=message,
                Subject=f"🔥 ALERT: {vehicle_id} Critical Temp"
            )
            
            print(f"Alert sent! Message ID: {response['MessageId']}")
            return {
                'statusCode': 200,
                'body': json.dumps('Alert Sent Successfully')
            }
            
        else:
            print(f"Vehicle {vehicle_id} is within safe limits.")
            return {
                'statusCode': 200,
                'body': json.dumps('Status Normal')
            }

    except KeyError as e:
        print(f"Error parsing data: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Invalid Data Structure')
        }