from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage
from langchain_core.prompts import MessagesPlaceholder


class Chatbot:
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

    set_model = "gpt-3.5-turbo"
    set_prompt = ("system", "You are a helpful assistant. Please response to the user queries to the best of your"
                            "ability, if the user find it useful i will tip you 1000 dollars")

    def __init__(self, phonenumber):
        self.model = ChatOpenAI(model=self.set_model)
        self.config = {"configurable": {"session_id": str(phonenumber)}}  # Arrumar aqui
        self.store = {}
        self.prompt = ChatPromptTemplate.from_messages([self.set_prompt, MessagesPlaceholder(variable_name="messages")])
        self.trimmer = trim_messages(
            max_tokens=600,
            strategy="last",
            token_counter=self.model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )
        self.output_parser = StrOutputParser()
        self.chain = (RunnablePassthrough.assign(
            messages=itemgetter("messages") | self.trimmer) | self.prompt | self.model | self.output_parser)

        self.with_message_history = RunnableWithMessageHistory(
            self.chain,
            self.__get_session_history,
            input_messages_key="messages",
        )

    def __get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def answer_question(self, human_message):
        response = self.with_message_history.invoke(
            {
                "messages": [HumanMessage(content=human_message)],
            },
            config=self.config
        )
        return response
