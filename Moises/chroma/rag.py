
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import json
import requests

# Define the prompt template
prompt_template = """You are a medical expert evaluating texts to determine whether
they contain misinformation. Your goal is to explain why the text is factually inaccurate
or misleading, using non-technical language. Reference details from the provided medical
information and if the provided information is insufficient, indicate that more context is needed.

Your response should be concise and written as human (2-3 sentences). Take into account that the reader has little
to no medical background. Mention or cite passages from the provided medical information so the user has more context.

medical information: {context}
Text: {text}

"""

prompt_template_2 = """
You are a medical expert evaluating misinformation in social media texts. Your task is to analyze
the provided text to identify its topic and important keywords. Your output should be a single
coherent sentence that summarizes the topic and helps find the best result in a vector database. 

Return only the vector database query as a string, with no additional text.

text: {text}
"""


# Create a LangChain PromptTemplate object
def generate_prompt(text: str, summary: bool, context: str = ''):
    if not summary:
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["text", "context"]
        )
        return prompt.format(context=context, text=text)
    else:
        prompt = PromptTemplate(
            template=prompt_template_2,
            input_variables=["text"]
        )
        return prompt.format(text=text)


# def evaluate_records(text: str, context: list[str] = None, summary=False) -> str:
#     # Initialize the OpenAI LLM model
#     temp = 0.8 if not summary else 0.4
#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temp)
#     research_context = '\n\n'.join(context) if context else ''
#     formatted_prompt = generate_prompt(text, summary, research_context)
#
#     # Prepare the prompt as a HumanMessage (the correct input for ChatOpenAI)
#     human_message = [HumanMessage(content=formatted_prompt)]
#
#     # Call the LLM model with the formatted prompt
#     response = llm(human_message)
#     output = response.content
#     print(output)
#
#     return output


# def evaluate_records_ollama(text: str, context: list[str] = None, summary=False) -> str:
#
