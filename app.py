from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from utils.parseRawPromptForInput import parseRawPromptForInputVariables

app = Flask(__name__)
CORS(app)


# Home page
@app.route("/api/v1/check", methods=["POST"])
def check():
    print(request.json)
    return jsonify({"status": "OK"})


@app.route("/api/v1/submit", methods=["POST"])
def submit():
    llm = OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    # run the tool with the input
    raw_prompt = request.json.get("prompt")
    inputs = request.json.get("inputs")
    input_variables = parseRawPromptForInputVariables(raw_prompt)
    cleaned_prompt = raw_prompt.replace("{{", "{").replace("}}", "}")

    prompt = PromptTemplate(template=cleaned_prompt, input_variables=input_variables)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    output = llm_chain.run(**inputs)

    return jsonify({"output": output})
