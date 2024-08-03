import streamlit as st
from datetime import date
import chromadb
from chromadb import Client
from langchain_openai import OpenAIEmbeddings
from config import get_or_create_collection

# Create a collection for goals if it doesn't exist
goals_collection = get_or_create_collection("goals")
goals_collection.add(
    documents=[""],
    metadatas=[{"text": ""}],
    ids=["current_goals"]
)

def main():
    st.title("Set Your Goals")
    # Get current goals
    current_goals = goals_collection.get(ids=["current_goals"])
    goals_text = current_goals["documents"][0]

    #current_goals = goals_collection.get()

    new_goals = st.text_area("Describe your goals:", goals_text)

    if st.button("Submit Goals"):
        goals_collection.update(
            ids=["current_goals"],
            documents=[new_goals],
            metadatas=[{"text": new_goals}]
        )
        st.success("Goals submitted successfully!")

if __name__ == "__main__":
    main()
