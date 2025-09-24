import httpx
import json
import re
import copy
import logging
from typing import Type, TypeVar, List, Dict, Any
from pydantic import BaseModel
import jsonschema
from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-1.5-flash:generateContent"
)

def pydantic_model_to_json_schema(model_cls: Type[BaseModel]) -> Dict[str, Any]:
    schema = model_cls.model_json_schema()
    return {"type": "object", "allOf": [schema]}

async def ask_gemini(
    prompt: str,
    context: List[Dict],
    response_model: Type[T],
    max_attempts: int = 3,
    timeout_seconds: int = 30
) -> T:
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": settings.GEMINI_API_KEY,
    }

    schema = pydantic_model_to_json_schema(response_model)
    schema_json = json.dumps(schema, indent=2)

    system_instruction = (
        "SYSTEM INSTRUCTION — STRICTLY OBEY THESE RULES:\n"
        "1) Respond with exactly ONE JSON object.\n"
        "2) The JSON MUST validate against the provided schema.\n"
        "3) Include only the fields: 'model', 'date', 'error', and model-specific fields (e.g., 'tests').\n"
        "4) If you cannot produce a valid response, set 'error' to a meaningful message.\n"
        "5) NO commentary, NO markdown, NO code fences — only the JSON object.\n\n"
        f"JSON_SCHEMA:\n{schema_json}"
    )

    payload_template = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"{system_instruction}\n\nContext:\n{json.dumps(context)}\n\nPrompt:\n{prompt}"
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        last_raw = None
        attempt = 0
        while attempt < max_attempts:
            payload = copy.deepcopy(payload_template)
            try:
                resp = await client.post(GEMINI_API_URL, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
            except httpx.HTTPError as e:
                logger.error(f"Attempt {attempt + 1} failed: HTTP error - {e}")
                attempt += 1
                continue

            raw_text = (
                data.get("candidates", [{}])[0]
                    .get("content", {}).get("parts", [{}])[0]
                    .get("text", "")
            )
            last_raw = raw_text
            cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)

            try:
                parsed = json.loads(cleaned)
            except json.JSONDecodeError as e:
                logger.error(f"Attempt {attempt + 1} failed: JSON parsing error - {e}")
                correction_note = (
                    f"Previous output failed JSON parsing: {e}\n"
                    "Return ONLY a single JSON object that validates against the schema."
                )
                payload_template["contents"][0]["parts"][0]["text"] = (
                    f"{system_instruction}\n\n{correction_note}\n\nContext:\n{json.dumps(context)}\n\nPrompt:\n{prompt}"
                )
                attempt += 1
                continue

            if not parsed.get("model"):
                parsed["model"] = data.get("modelVersion", "unknown")

            # Strip fields not defined in the Pydantic model
            expected_fields = response_model.__fields__.keys()
            parsed = {k: v for k, v in parsed.items() if k in expected_fields}

            try:
                jsonschema.validate(instance=parsed, schema=schema)
                return response_model.parse_obj(parsed)
            except jsonschema.ValidationError as ve:
                logger.error(f"Attempt {attempt + 1} failed: Schema validation error - {ve.message}")
                correction_note = (
                    f"Previous output failed schema validation: {ve.message}\n"
                    "Return ONLY a single JSON object that validates against the schema."
                )
                payload_template["contents"][0]["parts"][0]["text"] = (
                    f"{system_instruction}\n\n{correction_note}\n\nContext:\n{json.dumps(context)}\n\nPrompt:\n{prompt}"
                )
                attempt += 1
                continue

        raise RuntimeError(
            f"Failed to obtain valid {response_model.__name__} from Gemini after {max_attempts} attempts. Last raw output:\n{last_raw}"
        )