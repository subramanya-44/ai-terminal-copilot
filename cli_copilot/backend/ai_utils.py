import os
import google.generativeai as genai
from typing import Dict, Any

# Configure Gemini API
GEMINI_API_KEY = 'AIzaSyCmq4SUVpa7lfmNsUgYJi7bCl98L2AIX7c'
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def analyze_command(command: str) -> Dict[str, Any]:
    """Analyze a shell command using Gemini AI and return structured suggestions."""
    
    # Clean the command from any comments or trailing spaces
    command = command.split('#')[0].strip()
    
    prompt = f"""
    You are an AI-powered Terminal Assistant. Analyze this command: {command}

    If the command has typos (like 'cl' instead of 'cd'), provide the correction.
    If the command is valid, suggest any better approaches.
    Pay special attention to security risks and dangerous operations.

    Format your response exactly like this:
    1️⃣ Command Status: [Valid/Invalid]
    2️⃣ Correction (if needed): [suggested correction]
    3️⃣ Better Approach: [better way to achieve the same goal]
    4️⃣ Explanation: [what the command does]
    5️⃣ Tips: [any relevant tips or warnings]
    """

    try:
        response = model.generate_content(prompt)
        if not response.text:
            raise ValueError("Empty response from AI model")
        return {
            "success": True,
            "analysis": response.text,
            "command": command
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error analyzing command: {str(e)}",
            "command": command
        }