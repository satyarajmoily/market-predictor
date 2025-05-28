from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

# Create a router for the API endpoints
router = APIRouter()

class AdditionResponse(BaseModel):
    """Model for the response of the addition endpoint."""
    timestamp: str
    result: float

@router.get("/api/v1/add", response_model=AdditionResponse, status_code=200)
async def add_numbers(
    num1: float = Query(..., description="The first number to add"),
    num2: float = Query(..., description="The second number to add")
) -> AdditionResponse:
    """
    Endpoint to add two numbers and return the result with the current timestamp.

    Args:
        num1 (float): The first number to add.
        num2 (float): The second number to add.

    Returns:
        AdditionResponse: The result of the addition and the current timestamp.
    """
    try:
        logger.debug(f"Received request to add {num1} and {num2}")
        
        # Perform the addition
        result = num1 + num2
        logger.debug(f"Calculated result: {result}")

        # Get the current timestamp in ISO 8601 format
        current_timestamp = datetime.utcnow().isoformat()
        logger.debug(f"Generated timestamp: {current_timestamp}")

        # Return the response
        return AdditionResponse(timestamp=current_timestamp, result=result)

    except Exception as e:
        logger.error(f"Error occurred while processing the request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Note: Ensure that this router is included in the main FastAPI application
# Example:
# from fastapi import FastAPI
# app = FastAPI()
# app.include_router(router)