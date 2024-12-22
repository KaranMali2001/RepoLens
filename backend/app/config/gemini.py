import google.generativeai as genai
import os


class Gemini:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={"response_mime_type": "application/json"},
            )
            print("Gemini configured successfully")
        except Exception as e:
            print("Error configuring Gemini:", e)
            raise ValueError("Error configuring Gemini")

    def get_model(self) -> genai.GenerativeModel:
        return self.model
