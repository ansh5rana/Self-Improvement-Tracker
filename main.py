import streamlit as st
from datetime import date
import chromadb
from chromadb import Client
from config import get_or_create_collection, get_chroma_client


# Create a collection for responses if it doesn't exist
responses_collection = get_or_create_collection("daily_responses")

def main():
    st.title("Daily Self-Improvement Journal")

    # Daily questions
    questions = [
        "What actions did you take today to improve upon yourself and your goals?",
        "What were your failures today?",
        "What is something that made you smile or laugh today?",
        "How would you rate your happiness today on a scale of 1-5?"
    ]
    questionMD = ["actions", "failures", "happiness", "rating"]

    # Get today's date
    today = str(date.today())

    answers = []
    #for question in questions:
        #response = st.text_input(question)
        #answers.append(response)

    actions_response = st.text_input("What actions did you take today to improve upon yourself and your goals?")
    failures_response = st.text_input("What were your failures today?")
    happiness_response = st.text_input("What is something that made you smile or laugh today?")
    rating_response = str(st.number_input(
        label="How would you rate your happiness today on a scale of 1-5",
        min_value=1,
        max_value=5,
        step=1,
        placeholder="Please select a number between 1-5"))

    answers = [actions_response, failures_response, happiness_response, rating_response]

    print(answers)

    if st.button("Submit Daily Response"):
        existing_response = responses_collection.get(ids=[today])
        if existing_response['ids']:
            st.warning("You have already submitted your responses for today.")
            return
        else:
            responses = answers
            for questionMD in questionMD:
                for response in responses:
                    responses_collection.add(
                        documents=[response],
                        metadatas=[{"question": questionMD}],
                        ids=[today]
                    )
            st.success("Responses submitted successfully!")

if __name__ == "__main__":
    main()
