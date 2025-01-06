import requests

# Set your Hugging Face API key
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": "Bearer YOUR TOKEN IN PLACE OF CAPITALIZED TEXT"}  # Replace with your key

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

if __name__ == "__main__":
    print("Chatbot: Hello! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # Query the Hugging Face API
        data = query({"inputs": user_input})
        #print(f"Raw Response: {data}")  # Debugging output

        # Extract and print the chatbot's response
        if isinstance(data, list) and "generated_text" in data[0]:
            print(f"Chatbot: {data[0]['generated_text']}")
        elif "error" in data:
            print(f"Chatbot: Error - {data['error']}")
        else:
            print("Chatbot: Sorry, I am unable to respond.")

