import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from litellm import completion
from langchain_google_genai import ChatGoogleGenerativeAI
import os
load_dotenv()
# set ENV variables
os.environ["GEMINI_API_KEY"] = os.getenv("API_KEY")
llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_LC")
)

app = Flask(__name__)

# Route to render the HTML page


@app.route('/')
def index():
    # Your HTML file should be in the templates folder
    return render_template('index.html')

# Route to handle the POST request from the frontend


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get the query data sent in the request body
        data = request.get_json()
        user_query = data.get('query', '')

        if not user_query:
            return jsonify({'response': 'Please enter a valid query.'}), 400

        # Process the query - Here you would handle the logic to process the query
        response = process_query(user_query)

        # Return the response as Markdown
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500


def process_query(query):

    prompt_1 = f"""This is the users query: {query}, you are a researcher,Do a deep analysis of the users query and then
     provide a detailed response to the user's query. Make sure the response is valid to the query, and return the response in html format using tailwindcss for styling
      , remember to use monochromatic colour scheme including shades of zinc that would look professional, and return it inside a section tag because the prompt will be injected as html
       inside the content of the page, the page has a dark colour scheme """
    response = completion(
        model=os.getenv("MODEL"),
        messages=[{"content": prompt_1, "role": "user"}])

    x: str = response['choices'][0]['message']['content'].lstrip(
        "```html").rstrip('````')
    with open("response.txt", "w") as file:
        file.write(x)

    return x


if __name__ == '__main__':
    app.run(debug=True)
