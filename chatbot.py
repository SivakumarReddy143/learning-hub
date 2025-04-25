from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self):
        try:
            self.groq_api_key = os.getenv('GROQ_API_KEY')
            
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            # Correct model name (as per Groq's supported models)
            self.chat_model = ChatGroq(
                api_key=self.groq_api_key,
                model="gemma2-9b-it"  # ✅ use this instead of "gemma2-9b-it"
            )
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise
    
    def get_response(self, user_message, context="You are a helpful learning assistant"):
        messages = [
            SystemMessage(content=context),
            HumanMessage(content=user_message)
        ]
        
        try:
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error while generating response: {str(e)}"

# Example usage
if __name__ == "__main__":
    try:
        chatbot = Chatbot()
        response = chatbot.get_response("Tell me about Python programming.")
        print("Chatbot response:", response)
    except Exception as e:
        print(f"Failed to initialize chatbot: {str(e)}")
