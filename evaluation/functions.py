import requests
import os
import time
from dotenv import load_dotenv
from enum import Enum


load_dotenv()


class EvaluationType(Enum):
    RELEVANCE = "relevance"
    ACCURACY = "accuracy"
    COHERENCE = "coherence"
    FLUENCY = "fluency"
    GROUNDEDNESS = "groundedness"


def get_response(data):
    """
    Sends a POST request to the conversation API to obtain a response.

    Parameters:
    - data (dict): Body of the request with prompt data.

    Environment Variables:
    - BASE_URL (required): The Base URL of the API. If not provided, defaults to "http://127.0.0.1:5000".

    """
    try:
        base_url = os.environ.get("BASE_URL", "http://127.0.0.1:5000")
        url = f"{base_url}/conversation"
        headers = {
            "content-type": "application/json",
        }

        response = requests.post(url, json=data, headers=headers)

        response.raise_for_status()  # Raises HTTPError for bad responses

        response_json = response.json()

        return response_json

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error in making the API request.\n{e}")

    except (KeyError, IndexError) as e:
        raise Exception(f"Error in parsing the API response.\n{e}")


def process_prompt(prompt: str):
    """
    Process a row of data containing a user question and obtain the AI-generated response along with an evaluation response/rating.

    Parameters:
    - prompt (string): A string containig Prmopt data.

    """
    try:
        prompt_data = {"messages": [{"role": "user", "content": prompt}]}
        start_time = time.time()
        response = get_response(prompt_data)
        end_time = time.time()
        answer = response["choices"][0]["messages"][1]["content"]
        response_time = end_time - start_time
        return answer, response_time

    except (KeyError, IndexError) as e:
        raise Exception(f"Error in parsing the API response.\n{e}")


def evaluate_response(prompt: str, answer: str, evaluation_type: EvaluationType):
    """
    Rate the quality of an AI-generated response based on the provided response and original user question.

    Parameters:
    - prompt (str): The original user question.
    - answer (str): The AI-generated response to be evaluated.
    - evaluation_type (EvaluationType): The type of evaluation to be performed.
    """
    eval_prompts = {
        EvaluationType.RELEVANCE: "judge the relevance of the output above to the given question and context and score the output on a scale of 1-5.",
        EvaluationType.ACCURACY: "judge the accuracy of the output above to the given question and context and score the output on a scale of 1-5.",
        EvaluationType.COHERENCE: "judge the coherence of the output above to the given question and context and score the output on a scale of 1-5.",
        EvaluationType.FLUENCY: "judge the fluency of the output above to the given question and context and score the output on a scale of 1-5.",
        EvaluationType.GROUNDEDNESS: "judge the groundedness of the output above to the given question and context and score the output on a scale of 1-5.",
    }

    try:
        prompt_data = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Question: {prompt}?\nResponse: {answer}\n{eval_prompts[evaluation_type]}",
                }
            ]
        }
        response = get_response(prompt_data)
        evaluation = response["choices"][0]["messages"][1]["content"]
        return evaluation

    except (KeyError, IndexError) as e:
        raise Exception(f"Error in parsing the API response.\n{e}")

