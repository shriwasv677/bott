import streamlit as st
import json
from fuzzywuzzy import fuzz

st.title("NIIIVIIII")
st.write("SEARCH")

# Load the responses from the JSON file
with open('responses.json', 'r') as file:
    responses = json.load(file)

# Function to find the best response
def get_response(user_input):
    user_input = user_input.lower()
    best_match = None
    best_score = 0
    for item in responses:
        for pattern in item["patterns"]:
            score = fuzz.ratio(pattern.lower(), user_input)
            if score > best_score:
                best_score = score
                best_match = item
    if best_score > 70:  
        return best_match["responses"][0]  # Return the first response directly
    return "I'm not sure how to respond to that."

# Initialize the session state for storing messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Input field for user messages
user_input = st.text_input("Your message:", key="user_input")

# Handle the send button
if st.button("Send"):
    if user_input:
        response = get_response(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": response})

# Display the conversation
for message in st.session_state['messages']:
    if message['role'] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")
