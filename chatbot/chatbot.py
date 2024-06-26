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

from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


class Chatbot:
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

    set_model = "gpt-3.5-turbo"
    set_prompt = ChatPromptTemplate.from_template("""
        Voce e um chatbot feito para a empresa Parkside e deve tirar duvidas relacionadas ao contexto fornecido.
        Responda a pergunta apenas baseado no contexto fornecido.
        Se voce nao souber a resposta diga que nao sabe
        Pense passo a passo antes de fornecer uma resposta.
        Tente nao alterar muito o conteudo no contexto fornecido.
        <context>
        {context}
        </context>
        Question: {input}""")

    # Pega Dados do Site
    loader = WebBaseLoader(web_path=(
        "https://www.parkside.com.br/como-funciona", "https://www.parkside.com.br/diferenciais",
        "https://www.parkside.com.br/duvidas-frequentes"),
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(
            class_=(
                "container-col-18 is-pad-t-72", "container-col-18 less-padding is-pad-tb-72", "faq-question",
                "faq-answer", "faq-answer-p", "faq-question-label no-margin")
        )))
    text_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
    documents = text_splitter.split_documents(text_documents)
    db = Chroma.from_documents(documents, OpenAIEmbeddings())

    def __init__(self, phonenumber):
        self.model = ChatOpenAI(model=self.set_model)
        self.store = {}
        self.prompt = self.set_prompt
        self.output_parser = StrOutputParser()

        document_chain = create_stuff_documents_chain(self.model, self.prompt)
        retriever = self.db.as_retriever()
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)
        self.chain = (create_retrieval_chain| self.output_parser)

    def answer_question(self, human_message):
        response = self.retrieval_chain.invoke({'input': human_message})
        return response['answer']
