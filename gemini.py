import google.generativeai as genai
import os

with open('config.txt', 'r') as file: # get secret key
    secret_key = file.read().strip()

os.environ["API_KEY"] = secret_key

genai.configure(api_key=os.environ["API_KEY"])

## prompt
PROMPT = """
You will be given descriptions of books provided by users. 
Your task is to extract specific pieces of information from each description and organize them into a dictionary. 
The fields to be extracted are: category, title, author, publisher, year, page, language, extension. 

If any information is missing from the user's description, you should return null for that field. 
The output should be structured as a json, with each field represented as a key and the extracted or missing information as the value.

Example:
User Description: "I'm looking for a fantasy book titled 'The Enchanted Forest' by John Smith, published in 2015 by Magic Press, 300 pages, in English."

Output:
{
  "category": "fantasy",\n
  "title": "The Enchanted Forest",\n
  "author": "John Smith",
  "publisher": "Magic Press",
  "year": 2015,
  "page": 300,
  "language": "English",
}

Your goal is to accurately fill out this dictionary based on the information provided in the user's description. 
If a user doesn’t mention the book's language, for example, you should return null the 'language' field.

The following is the user's description:
[USER_DESCRIPTION]
"""


def extract_fields(user_input):
    prompt = PROMPT.replace("[USER_DESCRIPTION]", user_input)
    return prompt

def query_sth(question):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    response = model.generate_content(extract_fields(question))
    # print(response.text)
    return response.text