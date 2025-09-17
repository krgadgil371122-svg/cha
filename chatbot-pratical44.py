import streamlit as st
import openai
import os

# Set your OpenAI API key here or export it as environment variable OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY_HERE"

# Hardcoded exam date for demo purposes
EXAM_DATE = "December 10, 2025"

def get_openai_response(user_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant for student queries."},
        {"role": "user", "content": user_input}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
            messages=messages,
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {e}"


def answer_question(user_input):
    # Simple logic for exam-related questions
    q = user_input.lower()
    if "exam" in q or "test" in q:
        if "when" in q or "date" in q:
            return f"The next exam is scheduled on {EXAM_DATE}."
    # Otherwise use OpenAI to answer
    return get_openai_response(user_input)

# Streamlit UI
st.set_page_config(page_title="Student Queries Chatbot", page_icon="🎓")

st.title("🎓 Student Queries Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_question = st.text_input("Ask a question about your course, exams, or anything related:")

if user_question:
    # Get the answer
    bot_answer = answer_question(user_question)

    # Save conversation
    st.session_state.chat_history.append(("You", user_question))
    st.session_state.chat_history.append(("Bot", bot_answer))

# Display chat history
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")
