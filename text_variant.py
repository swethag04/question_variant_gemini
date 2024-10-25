import vertexai
import json

PROJECT_ID = ""
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

from vertexai.generative_models import(
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory
)
generation_config = {
    "temperature": 0,
    "top_p": 0.95
}
model = GenerativeModel(
        model_name = "gemini-1.5-flash-001",
        generation_config =  GenerationConfig(
            response_mime_type="application/json"),
    )

def question_generator(q_list):
    variant_1 = []
    variant_2 = []
    
    for q in q_list:
        prompt =  """You are an expert question writer. 
        Given the following question, please generate two variants 
        of the question that are similar in difficulty and assess 
        the same knowledge. Generate the variants in json format 
        with keys "variant1" and "variant2".

        Original Question: {q}
        """
        response = model.generate_content(prompt)
        response_json = json.loads(response.text)
        variant_1.append(response_json.get('variant1'))
        variant_2.append(response_json.get('variant2'))
    
    print(f"question: {q_list}")
    print(f"variant1: {variant_1}")
    print(f"variant2: {variant_2}")

    return variant_1, variant_2

