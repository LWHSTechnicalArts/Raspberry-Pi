mport requests
import json

OPENAI_API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key

def chat_with_gpt(prompt):
  url = 'https://api.openai.com/v1/completions'
  headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {OPENAI_API_KEY}',
  }

  data = {
      'model': 'text-davinci-003',  # Specify the GPT-3 model
      'prompt': prompt,
      'temperature': 0.7,
      'max_tokens': 150,
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
      return response.json()['choices'][0]['text']
  else:
      print(f"Error: {response.status_code}")
      print(response.text)
      return None


if __name__ == "__main__":
    user_prompt = input("User: ")
    while user_prompt.lower() not in ['exit', 'quit']:
        response = chat_with_gpt(user_prompt)
        print(f"ChatGPT: {response}")
        user_prompt = input("User: ")
