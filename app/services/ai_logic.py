"""
This module is used to analyze the code for N+1 queries, architectural bottlenecks, and security risks.
Purpose: The "Brain." This is where the Staff Engineer personality lives.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class CentryBrain:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)

    def analyze_infrastructure(self, content: str, context: str):
        system_msg = (
            "You are Centry, a Staff Platform Engineer. Analyze this code for "
            "N+1 queries, architectural bottlenecks, and security risks. "
            "Be concise and technical."
        )

        message = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_msg,
            messages=[{"role": "user", "content": f"Review this {context}:\n\n{content}"}]
        )
        return message.content[0].text