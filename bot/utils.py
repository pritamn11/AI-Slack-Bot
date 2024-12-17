import google.generativeai as genai

import helpers

GEMINI_API_KEY = helpers.config("GEMINI_API", default=None, cast=str)

genai.configure(api_key=GEMINI_API_KEY)  
model = genai.GenerativeModel("gemini-1.5-flash")  

def gemini_response(message):  
    """  
    Sends a message to the AI model and retrieves the generated response.  

    Parameters:  
    message (str): The input message to send to the AI.  

    Returns:  
    str: The generated response from the AI.  
    """  
    try:  
        response = model.generate_content(message)  
        return response.text  
    except Exception as e:  
        return f"An error occurred: {e}" 