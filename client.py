# pip install google-generativeai

import google.generativeai as genai

class OpenAI_Style_Gemini:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    class Chat:
        def __init__(self, outer):
            self.outer = outer

        class Completions:
            def __init__(self, outer):
                self.outer = outer

            def create(self, model, messages):
                # Convert messages to single string prompt
                prompt = ""
                for msg in messages:
                    prompt += f"{msg['role']}: {msg['content']}\n"

                response = self.outer.outer.model.generate_content(prompt)

                # Return in OpenAI-like format
                return {
                    "choices": [
                        {
                            "message": {
                                "content": response.text
                            }
                        }
                    ]
                }

        @property
        def completions(self):
            return self.Completions(self)

    @property
    def chat(self):
        return self.Chat(self)


# ----------------- USAGE -----------------
client = OpenAI_Style_Gemini(
    api_key="GEMINI_OR_OPENAI _AOI_KEY"
)
try:
    completion = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
            {"role": "user", "content": "what is coding"}
        ]
    )
    print(completion["choices"][0]["message"]["content"])
except Exception as e:
    print("Error:", e)