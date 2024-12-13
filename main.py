from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import time
import logging
from analysis import OPENAI_API_KEY, nist_analysis
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(),
              logging.FileHandler('nistai.log')])
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/nistai")
async def nistai(file: UploadFile = File(...), ):
    try:
        logger.info("Starting Nist Analysis")
        start_time = time.time()

        # Check if the file has a name
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No file name provided.")

        print("File Name: " + str(file.filename))

        full_path = os.path.join(file.filename)

        # Save the uploaded file to the server
        try:
            with open(full_path, "wb") as buffer:
                buffer.write(await file.read())
        except IOError as e:
            logger.error(f"File I/O error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file.")

        await file.seek(0)

        response = nist_analysis(full_path)

        process_time = time.time() - start_time
        logger.info(f"Nist Analysis Complete - {process_time:.4f}s")

        return {"response": response}

    except HTTPException as e:
        # Re-raise HTTPException to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch any unexpected exceptions
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred.")

@app.post("/nistai_url")
async def nistai_url(pdf_url: str):
    try:
        logger.info("Starting NIST Analysis from URL")
        start_time = time.time()

        # Validate the URL
        if not pdf_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No PDF URL provided."
            )

        logger.info(f"Downloading file from URL: {pdf_url}")

        # Download the PDF
        try:
            response = requests.get(pdf_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to download the file: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to download the file. Ensure the URL is valid."
            )

        # Save the file to a temporary location
        file_name = os.path.basename(pdf_url)
        temp_path = os.path.join("/tmp", file_name)

        with open(temp_path, "wb") as temp_file:
            temp_file.write(response.content)

        logger.info(f"File saved to temporary location: {temp_path}")

        # Perform NIST analysis
        response_data = nist_analysis(temp_path)

        # Calculate process time
        process_time = time.time() - start_time
        logger.info(f"NIST Analysis Complete - {process_time:.4f}s")

        # Return the response
        return {"response": response_data}

    except HTTPException as e:
        # Re-raise HTTPException to be handled by FastAPI
        raise e
    except Exception as e:
        # Catch any unexpected exceptions
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
if __name__ == "__main__":
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY environment variable not set")
    logger.info("Starting FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=8080)
