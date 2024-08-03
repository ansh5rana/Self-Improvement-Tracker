import streamlit as st
from datetime import date
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_or_create_collection
from chromadb import Client
from langchain_openai import OpenAIEmbeddings

# Initialize Chroma client and embeddings

embeddings = OpenAIEmbeddings()

responses_collection = get_or_create_collection("daily_responses")
goals_collection = get_or_create_collection("goals")
reports_collection = get_or_create_collection("reports")

def generate_report():
    # Fetch all responses and goals
    goals = goals_collection.get(ids=["current_goals"])
    goals_text = goals["documents"][0]

    def getText(questionMD):
        results = responses_collection.get(
            where={"question":questionMD},
            include = ["documents"]
        )
        return ' '.join(results['documents'])

    answers = []
    questionMD = ["actions", "failures", "happiness", "rating"]
    for questionMD in questionMD:
        answers.append(getText(questionMD))
        
    
    #################
    
    # Generate report using LangChain
    template = """You are an assistant in a self improvement tool. 
    Each day, users will answer some basic questions about their actions and feelings throughout the day which is recorded in the context below.
    Here are the questions they will be asked:
    1. What actions did you take today to improve upon yourself and your goals?
    2. What were your failures today?
    3. What is something that made you smile or laugh today?
    4. How would you rate your happiness today on a scale of 1-5?
    Your job is to take this information and summarize their responses and provide insights on how they can improve their actions and encourage them to keep doing the things that are working well for them on their way to reaching their goals:
    Actions: {actions}
    Failures: {failures}
    Happiness: {happiness}
    Rating: {rating}"""

    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106")
    chain = prompt | llm | StrOutputParser()
    report = chain.invoke({"actions": answers[0], "failures": answers[1], "happiness": answers[2], "rating": answers[3],})

    return report


def main():
    st.title("Generate Your Report")

    if st.button("Get Report"):
        report = generate_report()
        report_date = str(date.today())
        reports_collection.add(documents=[report],
                               metadatas=[{"text": report}],
                               ids=[report_date]
                              )
        st.write(report)

    # Display all past reports
    st.title("Past Reports")
    reports = reports_collection.get()
    for (id, report) in zip(reports["ids"], reports["documents"]):
        st.write(id)
        st.write(report)


if __name__ == "__main__":
    main()
