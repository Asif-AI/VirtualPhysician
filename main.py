import base64
import io
from PIL import Image
import requests
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError('GROQ_API_KEY is not set in .env file')


def process_image(image_path, query):
    try:    
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()
            base64.b64encode(image_content).decode("utf-8")

        try:
            image.open(io.BytesIO(image_content))
        except Exception as e:
            logger.error(f"invalid image format: {str(e)}")
            return {"error": f"invalid image format: {str(e)}"}
               
    except Exception as e:
        logger.error(f"An unexpected error occured : {str(e)}")
        return {"error": f"An unexpected error occured : {str(e)}"}

        messages=[
            {
                "role": "user",
                "content":[
                    {"type":"text", "text": query},
                    {"type":"image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]

        def make_api_request(model):
            requestes.post(
                GROQ_API_URL,
                json={
                    "model":model,
                    "message": messages,
                    "max_tokens": 1000
                },
                headers={
                    "Authorization":f"Bearer{GROQ_API_KEY}",
                    "Content-Type": "application/json"

                },
                timeout=30
            )
            return response

    llama_11b_response = make_api_request("llama-3.2-11b-vision-preview")
    llama_90b_response == make_api_request("llama-3.2-90b-vision-preview")

    llama_90b_response == make_api_request("llama-3.2-90b-vision-preview")
    
    responses={}
    for model, response in [("llama11b", llama_11b_response), ("llama90b", llama_90b_response)]:
        if response.status_code==200:
            result=response.json()
            answer=result["choices"][0]["message"]["content"]
            logger.info(f"Processed response from {model} API: {answer}")
            responses[model]=answer
        else:
            logger.error(f"Error from {model} API: {response.status_code}-{response.text}")
            responses[model]=f"Error from {model} API: {response.status_code}"
    return responses




if __name__ == "__main__":
    image_path = "acne.jpg"
    query="what is available in this picture"
    result = process_image(image_path, query)
    print(result)


