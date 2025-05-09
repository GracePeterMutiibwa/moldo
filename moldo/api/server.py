from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from .. import MoldoParser

app = FastAPI(title="Moldo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

parser = MoldoParser()


class MoldoCode(BaseModel):
    code: str


class CompileResult(BaseModel):
    result: str
    errors: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: str


@app.get("/health", include_in_schema=True)
@app.get("/health/", include_in_schema=False)  # Also match the path with trailing slash
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify API is operating normally.

    Returns:
        HealthResponse with status "OK" and current timestamp
    """
    return HealthResponse(status="OK", timestamp=datetime.now().isoformat())


@app.post("/compile", include_in_schema=True)
@app.post("/compile/", include_in_schema=False)
async def compile_code(moldo_code: MoldoCode) -> Dict[str, str]:
    """
    Compile Moldo code to Python.

    Args:
        moldo_code: The Moldo code to compile

    Returns:
        Dictionary containing the generated Python code
    """

    # print("::", moldo_code.code)
    try:
        python_code, _ = parser.parse(moldo_code.code)

        print("Code:", python_code)

        return {"python_code": python_code}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @app.get("/functions", include_in_schema=True)
# @app.get("/functions/", include_in_schema=False)
async def get_available_functions() -> Dict[str, List[str]]:
    """
    Get a list of all available Moldo functions.

    Returns:
        Dictionary containing the list of available functions
    """
    return {"functions": {}}


# @app.post("/functions/{name}", include_in_schema=True)
# @app.post("/functions/{name}/", include_in_schema=False)
async def execute_function(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a specific Moldo function.

    Args:
        name: The name of the function to execute
        args: The arguments to pass to the function

    Returns:
        Dictionary containing the function result
    """
    try:
        result = parser.execute_function(name, **args)
        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
