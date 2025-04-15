
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import shelve

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Macros(BaseModel):
    calories: int
    protein: int
    fat: int
    carbs: int

def get_macros(general_info, goals):
    completion = client.beta.chat.completions.parse(
        model = "gpt-4o",
        messages = [
            {"role":"system", "content":"You are an expert in nutrition who helps your client to achieve success in their fitness journey"},
            {"role":"user",
             "content": f"Base on the following user profile, please calculate the recommended daily intake of calories, protein (in grams), fat (in grams), and carbohydrates (in grams) to achieve their goals. The user profile is {general_info}, their goals are {goals}"}
        ],
        response_format=Macros
    )
    return dict(completion.choices[0].message.parsed)

def ask_ai(profile, notes, user_question):
    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role":"system", "content":f"You are professional fitness trainer with many years of experience. Your role is to advise your client on fitness-related questions. You have access to the client profile and notes which you can use to understand your client and help them to answer their questions. Your client profile is {profile}. Besides, here are the notes from your client: {notes}."},
            {"role":"user",
             "content": user_question}
        ],
    )
    return completion.choices[0].message.content

def chat_with_ai(profile, notes, input_messages):
    system_message = [
            {"role":"system", "content":f"You are professional fitness trainer with many years of experience. Your role is to advise your client on fitness-related questions. You have access to the client profile and notes which you can use to understand your client and help them to answer their questions. Your client profile is {profile}. Besides, here are the notes from your client: {notes}. Answer your questions in less than 150 words."}
        ]
    all_messages = system_message + input_messages
    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages = all_messages,
        stream= True,
    )
    return completion

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])


# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages