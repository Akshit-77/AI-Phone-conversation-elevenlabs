import openai
import os
from typing import Dict, List
from utils.env_loader import load_env

load_env(override=True)

class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.conversations: Dict[str, List[Dict]] = {}
        
        self.system_prompt = """You are a helpful voice assistant for phone calls. 
        Provide concise, clear, and helpful responses to user queries. 
        Keep responses brief since this is a voice interaction.
        Be natural and conversational.
        If the user says goodbye, thanks, or wants to end the call, acknowledge it briefly."""
    
    async def get_response(self, user_input: str, call_sid: str) -> str:
        # Initialize conversation if new
        if call_sid not in self.conversations:
            self.conversations[call_sid] = [
                {"role": "system", "content": self.system_prompt}
            ]
        
        # Add user message to conversation
        self.conversations[call_sid].append({
            "role": "user", 
            "content": user_input
        })
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversations[call_sid],
                max_tokens=150,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to conversation
            self.conversations[call_sid].append({
                "role": "assistant",
                "content": assistant_response
            })
            
            return assistant_response
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "I'm sorry, I'm having trouble processing your request right now."
    
    def clear_conversation(self, call_sid: str):
        if call_sid in self.conversations:
            del self.conversations[call_sid]