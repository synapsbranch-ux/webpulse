import asyncio
from app.config import settings
import boto3

async def test_nova():
    try:
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            aws_access_key_id=settings.AWS_KEY_ID,
            aws_secret_access_key=settings.AWS_KEY_SECRET,
            region_name=settings.AWS_REGION
        )
        
        prompt = "Hello, are you Amazon Nova?"
        
        response = bedrock.converse(
            modelId="amazon.nova-micro-v1:0",
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "maxTokens": 100,
                "temperature": 0.5
            }
        )
        
        text = response['output']['message']['content'][0]['text']
        print(f"Success! Response from Nova: {text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_nova())
