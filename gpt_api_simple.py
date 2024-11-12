from openai import OpenAI

client = OpenAI(api_key='your key here')

def ask_chatgpt(prompt):
    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Process the streamed response
        for chunk in response:
            if 'choices' in chunk:
                print(chunk['choices'][0]['delta'].get('content', ''), end="")
        print("\n")

    except Exception as e:
        print("Error:", str(e))

while True:
    user_prompt = input("Enter your prompt: ")
    ask_chatgpt(user_prompt)

