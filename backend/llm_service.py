import os
import json
import litellm

# Use a default model, e.g. gpt-4o, 'ollama/llama3', 'claude-3-5-sonnet-20240620', 'gemini/gemini-pro'
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o")


def get_system_prompt() -> str:
    """Loads the Coursework Analyzer Prompt v7."""
    # We will assume the prompt is available in the docs folder, or we can hardcode it here.
    # For now, let's load it from where we saved it.
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "docs", "system_prompt.md")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are the Coursework Analyzer. (Prompt not found)"

def generate_chat_response(messages: list, learner_profile: dict = None) -> str:
    """
    Calls the LLM with the injected system prompt and learner profile history.
    """
    # 1. Start with the system prompt
    system_content = get_system_prompt()
    
    # 2. Inject Learner Profile Context
    if learner_profile:
        profile_context = f"\n\n--- CURRENT LEARNER PROFILE ---\n{json.dumps(learner_profile, indent=2)}\n-------------------------------"
        system_content += profile_context

    formatted_messages = [{"role": "system", "content": system_content}]
    
    # 3. Append history
    formatted_messages.extend(messages)
    
    try:
        response = litellm.completion(
            model=MODEL_NAME,
            messages=formatted_messages,
            temperature=0.7,
            api_base=os.environ.get("OPENAI_BASE_URL") if os.environ.get("OPENAI_BASE_URL") else None
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}"
