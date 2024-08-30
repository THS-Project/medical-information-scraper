
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Define the prompt template
prompt_template = """You are a medical expert evaluating texts to determine whether
they contain misinformation. Your goal is to explain why the text is factually inaccurate
or misleading, using non-technical language. Use the following context for the response.
Reference details from the provided context if possible, and if the provided information
is insufficient, indicate that more context is needed.

Your response should be concise (2-3 sentences).

Context: {context}
Text: {text}


"""


# Create a LangChain PromptTemplate object
def generate_prompt(context: str, text: str):
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "text"]
    )
    return prompt.format(context=context, text=text)


def evaluate_records(context: list[str], text: str) -> str:
    # Initialize the OpenAI LLM model
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    research_context = ''.join(context)
    formatted_prompt = generate_prompt(research_context, text)

    # Prepare the prompt as a HumanMessage (the correct input for ChatOpenAI)
    human_message = [HumanMessage(content=formatted_prompt)]

    # Call the LLM model with the formatted prompt
    response = llm(human_message)
    output = response.content
    print(output)

    return output
