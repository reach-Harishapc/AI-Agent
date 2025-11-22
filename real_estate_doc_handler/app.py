from flask import Flask, render_template, request, jsonify
import markdown

# Import the agent executor from the document handler's main module
from real_estate_doc_handler.main import agent_executor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    try:
        # Invoke the LangChain agent
        response = agent_executor.invoke({"input": user_message})
        output = response['output']
        # Convert Markdown to HTML for display
        output_html = markdown.markdown(output)
        return jsonify({'response': output_html})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use a different port to avoid conflict with the real_estate UI
    app.run(debug=True, port=5002)
