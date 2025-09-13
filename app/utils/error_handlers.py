from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from typing import Union
import logging

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    """
    Custom handler for Pydantic validation errors.
    Converts technical validation errors into user-friendly messages.
    """
    errors = []
    
    for error in exc.errors():
        field_name = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        error_type = error["type"]
        error_msg = error["msg"]
        input_value = error.get("input", "")
        
        # Create user-friendly error messages based on error type
        if error_type == "int_parsing":
            friendly_msg = f"Field '{field_name}' must be a valid integer, received: '{input_value}'"
        elif error_type == "string_type":
            friendly_msg = f"Field '{field_name}' must be a text string, received: '{input_value}'"
        elif error_type == "missing":
            friendly_msg = f"Field '{field_name}' is required but was not provided"
        elif error_type == "value_error":
            friendly_msg = f"Field '{field_name}' has invalid value: {error_msg}"
        elif error_type == "type_error":
            friendly_msg = f"Field '{field_name}' has incorrect data type: {error_msg}"
        elif error_type == "greater_than_equal":
            friendly_msg = f"Field '{field_name}' must be greater than or equal to the minimum allowed value"
        elif error_type == "less_than_equal":
            friendly_msg = f"Field '{field_name}' must be less than or equal to the maximum allowed value"
        elif error_type == "string_too_short":
            friendly_msg = f"Field '{field_name}' is too short, minimum length required"
        elif error_type == "string_too_long":
            friendly_msg = f"Field '{field_name}' is too long, maximum length exceeded"
        else:
            # Fallback for unknown error types
            friendly_msg = f"Field '{field_name}': {error_msg}"
        
        errors.append({
            "field": field_name,
            "message": friendly_msg,
            "received_value": str(input_value) if input_value != "" else None
        })
    
    # Log the validation error for debugging
    logger.warning(f"Validation error on {request.url}: {errors}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "The request contains invalid data. Please check the fields below and try again.",
            "details": errors
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Custom handler for HTTP exceptions.
    Provides consistent error response format.
    """
    logger.warning(f"HTTP exception on {request.url}: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": get_error_name(exc.status_code),
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

def get_error_name(status_code: int) -> str:
    """Get user-friendly error name based on HTTP status code."""
    error_names = {
        400: "Bad Request",
        401: "Unauthorized", 
        403: "Forbidden",
        404: "Not Found",
        409: "Conflict",
        422: "Validation Error",
        500: "Internal Server Error"
    }
    return error_names.get(status_code, "Error")
