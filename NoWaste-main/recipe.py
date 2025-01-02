from openai import OpenAI
import openai
import show
import random


import os

# set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("api_key is not set")


def ask_gpt(prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def get_recipe():
    ingridient = show.ShowValidAsDict()
    ingridient_string = '' #use to stroe name of select ingridient

    if(len(ingridient) <= 5):
        for row in ingridient:
            ingridient_string = ingridient_string + row["Name"] + ','
    else:
        select_ingridient = [] # use to stroe selected ingridient dictionary

        # generate a list consisting of 5 random integer which doesn't duplicate
        random_numbers = random.sample(range(1, len(ingridient)), 5)  # chose 5 int from 100 numbers

        # select ingridient and put it into a new list called slect_ingridient
        for i in random_numbers:
            select_ingridient.append(ingridient[i])

        # select name of every dictionary in selected ingridient. And concatenate them into a whole string.
        for row in select_ingridient:
            ingridient_string = ingridient_string + row["Name"] + ','

    # get rid of redundant comma
    ingridient_string = ingridient_string.rstrip(', ')

    prompt_word = 'I currently have ' + ingridient_string + '.' +\
        'Please randomly select ingredients and provide me with 3 recipes.' +\
        'The recipes must be traditional dishes; you cannot create new recipes.' +\
        'The recipe should include the ingredient quantities and a brief outline of the steps.'

    return ask_gpt(prompt_word)


'''
How to set key of openai as encironment variable?
1. 
export OPENAI_API_KEY="your_openai_api_key"
2. 
echo $OPENAI_API_KEY

'''