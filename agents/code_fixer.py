"""
Code Fixer Agent - Uses Groq as inference provider with OpenAI-compatible API
"""
import json
import re
from openai import OpenAI
from config.settings import GROQ_API_KEY, GROQ_BASE_URL, MODEL_NAME, TEMPERATURE, MAX_TOKENS

# Initialize Groq client with OpenAI-compatible interface
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL
)

SYSTEM_PROMPT = """You are an expert code debugger and fixer. Your job is to analyze code that contains errors and provide fixes.

When given code with errors, you must:
1. Identify the issue(s) in the code
2. Explain what was wrong in simple, clear terms
3. Provide the corrected code

IMPORTANT: You MUST respond ONLY with valid JSON in this exact format:
{
    "explanation": "A brief, friendly explanation of what was wrong and how you fixed it",
    "fix": "The complete corrected code"
}

Rules for your response:
- Keep the explanation concise and helpful (1-2 sentences)
- The fix should be the complete corrected code, not just the changed parts
- Do not include markdown code blocks in your JSON response
- Do not add any text outside the JSON object
- Ensure the JSON is valid and parseable"""


def fix_code(code: str) -> dict:
    """
    Send code to LLM for analysis and fixing.
    
    Args:
        code: The error code to fix
        
    Returns:
        dict with 'explanation' and 'fix' keys
    """
    try:
        user_message = f"""Please analyze and fix the following code:

```
{code}
```

Remember to respond ONLY with valid JSON containing 'explanation' and 'fix' keys."""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        # Extract the response content
        content = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        result = parse_llm_response(content)
        
        return result
        
    except Exception as e:
        
        return {
            "explanation": f"Error analyzing code: {str(e)}",
            "fix": code 
        }


def parse_llm_response(content: str) -> dict:
    """
    Parse the LLM response, handling potential formatting issues.
    
    Args:
        content: Raw response from LLM
        
    Returns:
        dict with 'explanation' and 'fix' keys
    """
    try:
        
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
  
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    json_match = re.search(r'\{[^{}]*"explanation"[^{}]*"fix"[^{}]*\}', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    return {
        "explanation": "The code has been analyzed. Please review the suggested changes.",
        "fix": content
    }
