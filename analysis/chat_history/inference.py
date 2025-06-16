import os
import json
from typing import Any
import openai
from pandas import Series, isna
from eval_prompt import EvaluationCateogry, generate_evaluation_system_prompt


AZURE_OPENAI_TEMPERATURE = os.getenv("AZURE_OPENAI_TEMPERATURE")
AZURE_OPENAI_TOP_P = os.getenv("AZURE_OPENAI_TOP_P")
AZURE_OPENAI_MAX_TOKENS = os.getenv("AZURE_OPENAI_MAX_TOKENS")
AZURE_OPENAI_STOP_SEQUENCE = os.getenv("AZURE_OPENAI_STOP_SEQUENCE")
AZURE_OPENAI_RESOURCE = os.getenv("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
openai.api_version = "2023-08-01-preview"
openai.api_key = AZURE_OPENAI_KEY

def evaluate_chat_response(row: Series, categories: list[EvaluationCateogry]) -> tuple[str, dict[str, Any]]:
    print(f"Evaluating chat response for {row['id']} ...")

    user_input = row['user_input']
    context = row['context']
    answer = row['answer']

    if not user_input or not context or not answer or isna(user_input) or isna(context) or isna(answer):
        raise ValueError("The user_input, context, and answer fields must be provided.")
    
    system_message = generate_evaluation_system_prompt(categories)
    messages = [
        { "role": "system", "content": system_message },
        { "role": "user", "content": user_input },
        { "role": "assistant", "content": answer },
        { "role": "user", "content": "# Context\n\nThe previous AI response was based on this context:\n\n{context}\n\nEvaluation:\n" }
    ]

    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_MODEL,
        messages=messages,
        temperature=float(AZURE_OPENAI_TEMPERATURE),
        max_tokens=int(AZURE_OPENAI_MAX_TOKENS),
        top_p=float(AZURE_OPENAI_TOP_P),
        stop=None,
        stream=False
    )

    return process_response(response)

def process_response(response):
    print(f"Processing evaulation response ...")

    result = json.loads(response["choices"][0]["message"]["content"])
    evaluation = result['evaluation']
    scores = result['scores']
    
    return evaluation, scores