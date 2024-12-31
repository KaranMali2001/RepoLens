import google.generativeai as genai
import os


class Gemini:
    def __init__(self, model_name):
        api_key = os.environ.get("GEMINI_API_KEY")

        if api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={"response_mime_type": "application/json"},
            )
            print("Gemini configured successfully")
        except Exception as e:
            print("Error configuring Gemini:", e)
            raise ValueError("Error configuring Gemini")

    def get_model(self) -> genai.GenerativeModel:
        return self.model


class EmbeddingsModel:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name="text-embedding-ada-002",
                generation_config={"response_mime_type": "application/json"},
            )
            print("Embeddings Model configured successfully")
        except Exception as e:
            print("Error configuring Embeddings Model:", e)
            raise ValueError("Error configuring Embeddings Model")

    def get_model(self) -> genai.GenerativeModel:
        return self.model
