from typing import List, Dict
from models.gemini_response import TestAgentResponse
from services.gemini_service import ask_gemini

async def generate_tests(requirements: str, context: List[Dict]) -> TestAgentResponse:
    """
    Generate Python test functions for a website based on user requirements using the Gemini API.
    
    Args:
        requirements (str): User-provided requirements (e.g., "Create a responsive landing page with a navbar").
        context (List[Dict]): Contextual information for the Gemini API.
    
    Returns:
        TestAgentResponse: A response containing Python test function strings.
    """
    prompt = (
        f"Generate a list of Python test functions (using pytest) for a static website based on the following requirements:\n"
        f"{requirements}\n\n"
        "Each test function should:\n"
        "- Be a valid Python function using pytest conventions (e.g., start with 'test_').\n"
        "- Test a specific aspect of the website's functionality, appearance, or responsiveness.\n"
        "- Use libraries like selenium or playwright for browser-based testing where appropriate.\n"
        "- Include assertions to validate the requirement.\n"
        "- Be returned as a string containing the complete function code.\n"
        "Examples:\n"
        "- 'def test_navbar_visible(driver):\\n    driver.get(\"index.html\")\\n    navbar = driver.find_element_by_class(\"navbar\")\\n    assert navbar.is_displayed()'\n"
        "- 'def test_form_validation(driver):\\n    driver.get(\"index.html\")\\n    form = driver.find_element_by_id(\"contact-form\")\\n    submit = form.find_element_by_tag(\"button\")\\n    submit.click()\\n    assert \"required\" in driver.page_source'\n"
        "Return the response in the format defined by the TestAgentResponse model, with 'tests' as a list of test function strings."
    )
    
    return await ask_gemini(
        prompt=prompt,
        context=context,
        response_model=TestAgentResponse
    )