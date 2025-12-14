import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIAgent:
    """
    Handles all AI-related tasks:
    - Text summarization
    - Classification (future)
    - Intelligent suggestions (future)
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("Missing OPENAI_API_KEY in .env")

        self.client = OpenAI(api_key=api_key)

    # ----------------------------
    # Summarization
    # ----------------------------
    def summarize_text(self, text: str) -> str:
        """
        Uses OpenAI API to generate a clean, compact summary
        based on the content of the file.
        """

        # Keep prompts safe by trimming extremely large text
        if len(text) > 8000:
            text = text[:8000]

        prompt = (
            "Summarize the following document in 3–5 bullet points. "
            "Focus on key ideas, topics, and important information. "
            "Avoid unnecessary detail.\n\n"
            f"Document:\n{text}"
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert summarization engine."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )

        return response.choices[0].message.content

