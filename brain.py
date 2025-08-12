from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json

class AIAgent:
    def __init__(self, GROQ_API_KEY, prompt_templete):
        self.groq_api = GROQ_API_KEY
        self.prompt_templete = prompt_templete
        self.llm = self.create_llm()
        self.prompt = self.crate_prompt() 
    
    def crate_prompt(self):
        return ChatPromptTemplate.from_template(self.prompt_templete)
    
    def create_llm(self):
        return ChatGroq(api_key=self.groq_api, model="llama-3.3-70b-versatile")
    
    def create_chain(self):
        chain = self.prompt | self.llm
        return chain
    
    def get_final_response(self, query):
        chain = self.create_chain()
        response = chain.invoke({"input": query})
        return json.loads(response.content)

