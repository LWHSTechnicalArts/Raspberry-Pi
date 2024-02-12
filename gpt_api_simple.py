from openai import OpenAI
client = OpenAI(api_key='your-api-key') 
 
def ask_chatgpt(prompt):
    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                  "role": "user",
                  "content": prompt
                }
            ],
            stream=True,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        
        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")
        print("\n")
        
    except Exception as e:
        return str(e)

while True:
    user_prompt = input("Enter your prompt: ")
    response = ask_chatgpt(user_prompt)
