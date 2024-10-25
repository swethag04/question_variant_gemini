import vertexai
import json
import os

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

from vertexai.generative_models import(
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory
)
model = GenerativeModel(
        model_name = "gemini-1.5-flash-001",
        generation_config =  GenerationConfig(
            response_mime_type="application/json"),
    )
prompt =  """You are an expert question writer. 
        Given the following question, please generate two variants 
        of the question that are similar in difficulty and assess 
        the same knowledge. Generate the variants in json format 
        with keys "variant1" and "variant2".

        Original Question: {q}
        """

def question_generator(q_list):
    variant_1 = []
    variant_2 = []
    
    for q in q_list:
        prompt_updated = prompt.format(q=q)
        response = model.generate_content(prompt_updated)
        response_json = json.loads(response.text)
        variant_1.append(response_json.get('variant1'))
        variant_2.append(response_json.get('variant2'))

    return variant_1, variant_2

