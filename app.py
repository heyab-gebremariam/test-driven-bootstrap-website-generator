import asyncio
import os
import json
from datetime import datetime
from typing import List, Dict
from services.test_agent_service import generate_tests
from services.developer_agent_service import generate_website_code
from models.gemini_response import TestAgentResponse, DeveloperAgentResponse

async def main(output_dir: str = "output"):
    """
    Generate test functions and website code for a Bootstrap 5 website based on user input.
    
    Args:
        output_dir (str): Directory to save generated test and website files.
    """
    # Prompt user for requirements
    requirements = input("Enter the website requirements (e.g., 'Create a responsive landing page with a navbar, hero section, and contact form using Bootstrap 5'): ")
    if not requirements.strip():
        print("Error: Requirements cannot be empty.")
        return

    os.makedirs(output_dir, exist_ok=True)
    context: List[Dict] = []

    # Step 1: Generate test functions
    print("Generating test functions...")
    test_response: TestAgentResponse = await generate_tests(requirements, context)
    if test_response.error:
        print(f"Error generating tests: {test_response.error}")
        return

    print("Generated test functions:")
    for i, test in enumerate(test_response.tests, 1):
        print(f"Test {i}:\n{test}\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_path = os.path.join(output_dir, f"test_website_{timestamp}.py")
    with open(test_path, "w") as f:
        f.write("# Generated test functions\n\n")
        for test in test_response.tests:
            f.write(f"{test}\n\n")
    print(f"Test functions saved to: {test_path}")

    # Step 2: Generate website code
    print("Generating website code...")
    context.append({"role": "user", "content": f"Test functions: {json.dumps(test_response.tests)}"})
    dev_response: DeveloperAgentResponse = await generate_website_code(test_response.tests, context)
    if dev_response.error:
        print(f"Error generating website code: {dev_response.error}")
        return

    # Step 3: Save website files in a timestamped folder
    timestamp_dir = os.path.join(output_dir, timestamp)
    os.makedirs(timestamp_dir, exist_ok=True)

    html_path = os.path.join(timestamp_dir, "index.html")
    css_path = os.path.join(timestamp_dir, "styles.css")
    js_path = os.path.join(timestamp_dir, "script.js")

    with open(html_path, "w") as f:
        f.write(dev_response.html)
    with open(css_path, "w") as f:
        f.write(dev_response.css)
    with open(js_path, "w") as f:
        f.write(dev_response.js)

    print(f"Website files saved to: {html_path}, {css_path}, {js_path}")

if __name__ == "__main__":
    asyncio.run(main())