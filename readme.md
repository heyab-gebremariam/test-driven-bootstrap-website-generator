# Test-Driven Bootstrap Website Generator

## Overview

`test-driven-bootstrap-website-generator` is a Python-based system that leverages AI agents to generate and validate a static website (HTML + CSS + JS + Bootstrap) using a **test-driven development (TDD)** approach.

Two AI agents interact:
- **Test Agent Service**: Generates tests first.
- **Developer Agent Service**: Implements code to satisfy those tests.

------------------------------------------------------------------------

## Folder Structure

```
test-driven-bootstrap-website-generator/
    ├─ models/
    │  ├─ gemini_response.py
    ├─ services/
    │  ├─ developer_agent_service.py
    │  ├─ test_agent_service.py
    │  └─ gemini_service.py
    ├─ app.py
    ├─ config.py
    ├─ requirements.txt
    └─ README.md
```

------------------------------------------------------------------------

## Models Definition

```python
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class GeminiBaseResponse(BaseModel):
    model: str
    date: datetime
    content: Optional[Any]
    error: Optional[str]

class TestAgentResponse(GeminiBaseResponse):
    tests: list[str]

class DeveloperAgentResponse(GeminiBaseResponse):
    html: str
    css: str
    js: str
```

------------------------------------------------------------------------

## Gemini Service

```python
def pydantic_model_to_json_schema(model_cls: Type[BaseModel]) -> Dict[str, Any]:
    pass

async def ask_gemini(
    prompt: str,
    context: List[Dict],
    response_model: Type[T],
    max_attempts: int = 3,
    timeout_seconds: int = 30
) -> T:
    pass
```

------------------------------------------------------------------------

## Developer Agent Service

```python
async def generate_website_code(tests: List[str], context: List[Dict]) -> DeveloperAgentResponse:
    pass
```

------------------------------------------------------------------------

## Test Agent Service

```python
async def generate_tests(requirements: str, context: List[Dict]) -> TestAgentResponse:
    pass
```

------------------------------------------------------------------------

## Requirements

`requirements.txt`:

```
httpx
pydantic
jsonschema
python-dotenv
```

------------------------------------------------------------------------

## Deployment Steps

1. **Clone the Repository**:
   Clone the project repository to your local machine or server:
   ```bash
   git clone <repository-url>
   cd test-driven-bootstrap-website-generator
   ```

2. **Set Up a Virtual Environment**:
   Create and activate a Python virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install the required Python packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root and add the Gemini API key:
   ```bash
   echo "GEMINI_API_KEY=your-api-key-here" > .env
   ```
   Replace `your-api-key-here` with your actual Gemini API key.

5. **Run the Application**:
   Start the main application by running the `app.py` script:
   ```bash
   python app.py
   ```
