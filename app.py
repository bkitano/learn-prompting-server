from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from utils.parseRawPromptForInput import parseRawPromptForInputVariables

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # allows all origins to make calls


# Home page
@app.route("/api/v1/check", methods=["POST"])
def check():
    print(request.json)
    return jsonify({"status": "OK"})


@app.route("/api/v1/batch", methods=["POST"])
def batch():
    llm = OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    raw_prompt = request.json.get("prompt")

    """
    prompt: string with {{brackets}} for input variables
    inputs: dict of input variables
    """
    input_variables = parseRawPromptForInputVariables(raw_prompt)
    cleaned_prompt = raw_prompt.replace("{{", "{").replace("}}", "}")

    # run the tool with the input
    inputs = request.json.get("inputs")

    prompt = PromptTemplate(template=cleaned_prompt, input_variables=input_variables)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    completions = llm_chain.apply(inputs)

    response = [
        {"input": input, "completion": completion}
        for input, completion in zip(inputs, completions)
    ]

    return jsonify({"completions": response})


@app.route("/api/v1/submit", methods=["POST"])
def submit():
    llm = OpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    raw_prompt = request.json.get("prompt")

    """
    prompt: string with {{brackets}} for input variables
    inputs: dict of input variables
    """
    input_variables = parseRawPromptForInputVariables(raw_prompt)

    if request.json.get("inputs") == {}:
        print("no inputs")
        response = llm(raw_prompt)
        return jsonify({"completion": response})

    # run the tool with the input
    inputs = request.json.get("inputs")
    cleaned_prompt = raw_prompt.replace("{{", "{").replace("}}", "}")

    prompt = PromptTemplate(template=cleaned_prompt, input_variables=input_variables)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    completion = llm_chain.run(**inputs)

    return jsonify({"completion": completion})
