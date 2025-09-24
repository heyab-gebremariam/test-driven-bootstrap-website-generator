from typing import List, Dict
from models.gemini_response import DeveloperAgentResponse
from services.gemini_service import ask_gemini

async def generate_website_code(tests: List[str], context: List[Dict]) -> DeveloperAgentResponse:
    """
    Generate HTML, CSS, and JS code for a Bootstrap 5 website that passes the provided test functions.
    
    Args:
        tests (List[str]): List of Python test functions (e.g., 'def test_navbar_exists(driver): ...').
        context (List[Dict]): Contextual information for the Gemini API.
    
    Returns:
        DeveloperAgentResponse: A response containing generated HTML, CSS, and JS code.
    """
    prompt = (
        f"Generate a static website using Bootstrap 5 that passes the following Python test functions:\n"
        f"{'-' * 80}\n"
        f"{'\n\n'.join(tests)}\n"
        f"{'-' * 80}\n\n"
        "Requirements:\n"
        "- Use Bootstrap 5 via CDN for responsive design.\n"
        "- Include a navbar with ID 'navbar', a hero section with ID 'hero', and a contact form with ID 'contact-form'.\n"
        "- The contact form must have fields with IDs 'name', 'email', 'message', and a submit button with ID 'submit'.\n"
        "- Use the 'container' class for layout.\n"
        "- Ensure the website is responsive for mobile (375x667) and desktop (1200x800) resolutions.\n"
        "- Include JavaScript for form validation (e.g., check for empty fields and valid email format).\n"
        "- Set the page title to 'My Website Title' to pass the responsive design test.\n"
        "Return the response in the format defined by the DeveloperAgentResponse model, with:\n"
        "- 'html': A complete HTML file with Bootstrap 5 CDN and responsive design.\n"
        "- 'css': CSS code (without <style> tags) for custom styling.\n"
        "- 'js': JavaScript code (without <script> tags) for interactivity.\n"
        "Ensure the code is clean, valid, and passes all provided tests."
    )
    
    return await ask_gemini(
        prompt=prompt,
        context=context,
        response_model=DeveloperAgentResponse
    )