from collections.abc import Generator

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv
load_dotenv()

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

def get_prompt_template(systemMessage: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"{systemMessage}",
            ),
            MessagesPlaceholder(variable_name="message"),
        ]
    )

def simple_message(query: str) -> str:
    response = model.invoke([HumanMessage(content=query)])
    return response.content

def template_message(query: str, template: ChatPromptTemplate) -> str:    
    prompt_template = template.invoke({"message": [HumanMessage(query)]})
    response = model.invoke(prompt_template)
    return response.content

def template_message_streamed(query: str, template: ChatPromptTemplate) -> Generator[str, None, None]:
    prompt_template = template.invoke({"message": [HumanMessage(query)]})
    for chunk in model.stream(prompt_template):
      if isinstance(chunk, AIMessage):
        yield chunk.content