import openai

def process_conversation(user_input):
    print("Process Conversation")
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']
