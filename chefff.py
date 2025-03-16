# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token

import os
# from dotenv import load_dotenv
# load_dotenv()
import json
import requests
from typing import Optional


BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.environ.get('LANGFLOW_ID')
FLOW_ID = os.environ.get('FLOW_ID')
APPLICATION_TOKEN = os.environ.get('APPLICATION_TOKEN')
# print(APPLICATION_TOKEN)
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "Agent-3aEQ5": {},
  "CalculatorComponent-aS2DJ": {},
  "ChatInput-wPjYy": {},
  "ChatOutput-r3GJy": {}
}
def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json", "Access-Control-Allow-Origin" : "*"}
    
    response = requests.post(api_url, json=payload, headers=headers)
    # print(response.status_code)
    return response.json()

def generateRecipes(cuisine="any", allergies="", numServings="", totalBudget="", dietaryReqs=[], remarks=""):
    message = "Please give me 3 recipes: A very cheap recipe, A very nutritional recipe, and A very tasty recipe. Please make sure that you use the calculator when you calculate the total cost per serving."
    if cuisine != "":
        message += f" I want to eat {cuisine} cuisine."

    if allergies != "":
        message += f" I have the following allergies: {allergies}."
    else:
        message += " I do not have any allergies."
    
    if dietaryReqs != "":
        message += f" I have the following dietary requirements: ."
        for i in dietaryReqs:
            message += f", {i}"
    
    if numServings != "":
        message += f" I want to cook {numServings} servings."

    if totalBudget != "":
        message += f" I want each recipe to cost below ${totalBudget}."

    if remarks != "":
        message += f" My additional remarks are: {remarks}."

    try:
        response = run_flow(
            message=message,
            endpoint=FLOW_ID,
            output_type="chat",
            input_type="chat",
            tweaks=TWEAKS,
            application_token=APPLICATION_TOKEN
        )
        # print("Success")

        res = json.dumps(response['outputs'][0]['outputs'][0]['results']['message']['data']['text'], indent=2)

        import re

        arr = res[1:-1].split(r"\n")

        result = {"start" : []}
        for i in arr:
            if i.startswith("###") and bool(re.search(r"\*\*.*\*\*", i)):
                result["start"].append(("bigAndBold", i.replace("**", "").replace("###", "")))
            elif i.startswith("###"):
                result["start"].append(("big", i.replace("###", "")))
            elif bool(re.search(r'\*\*.*\*\*', i)):
                result["start"].append(("bold", i.replace("**", "")))
            else:
                result["start"].append(("normal", i))

        # for i in result["start"]:
        #     print(i[1], i[0])
        return result

    except:
        pass
        # print("OOPSIES =======================================================================================")

    

# start_time = time.time()
# generateRecipes()
# end_time = time.time()
# print("============================================================================================")
# print(end_time - start_time)
# print()
