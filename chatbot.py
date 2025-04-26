# chatbot.py

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Chatbot:
    def __init__(self):
        try:
            self.groq_api_key = os.getenv('GROQ_API_KEY')
            
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            # Initialize the ChatGroq model (no proxies or extra arguments)
            self.chat_model = ChatGroq(
                api_key=self.groq_api_key,
                model_name="gemma2-9b-it",  # you can change model if needed
                streaming=True
            )
            
            # Initialize conversation memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise
    
    def get_response(self, user_message, context="You are a helpful AI learning assistant."):
        try:
            # Get chat history from memory
            chat_history = self.memory.load_memory_variables({})["chat_history"]
            
            # Create messages list with context, history, and current message
            messages = [
                SystemMessage(content=context)
            ]
            
            # Add chat history
            messages.extend(chat_history)
            
            # Add current user message
            messages.append(HumanMessage(content=user_message))
            
            # Get response from model
            response = self.chat_model.invoke(messages)
            
            # Save the interaction to memory
            self.memory.save_context(
                {"input": user_message},
                {"output": response.content}
            )
            
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
