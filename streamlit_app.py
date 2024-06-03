import os
import json
from datetime import datetime
import streamlit as st
import google.generativeai as genai

# Function to initialize session state
def initialize_session_state():
    return st.session_state.setdefault('api_key', None)

# Function to load or create JSON file
def load_or_create_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []
    return data

# Function to save data to JSON file
def save_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Main Streamlit app
def text_page():
    st.title("TESTING UI")
    st.title("")

    # Initialize session state
    initialize_session_state()

    # Configure API key
    api_key = 'AIzaSyANYAfQgXVVTuwgYFJ6w0phR8DjPhcYc48';

    # Check if the API key is provided
    if not api_key:
        st.sidebar.error("Please enter your API key.")
        st.stop()
    else:
        # Store the API key in session state
        st.session_state.api_key = api_key

    genai.configure(api_key=api_key)

    safety_settings = "{}"
    safety_settings = json.loads(safety_settings)

    col1, col2 = st.columns(2)



    with col1:
        prompt_1 = st.text_area("Persona:", height=100)
        prompt_2 = st.text_area("Task:", height=100)
        prompt_3 = st.text_area("Criteria to achieve the task:", height=100)
        prompt_4 = st.text_area("Assumption:", height=100)


    with col2:
        prompt_5 = st.text_area("Project Overview:", height=100)
        prompt_6 = st.text_area("Business Requirement/User Story:", height=100)
        prompt_7 = st.text_area("Shots: ", height=100)
        prompt_8 = st.text_area("Free Prompts: ",height=100)
    # Concatenate the inputs and generate content when the "Generate" button is clicked
    if st.button("Generate"):
        prompt = ".".join(filter(None, [prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_6, prompt_7, prompt_8]))

        # Check if the query is provided
        if not prompt:
            st.error("Please enter your query.")
        else:
            gemini = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                           safety_settings=safety_settings)
            prompt_parts = [prompt]

            try:
                response = gemini.generate_content(prompt_parts)
                st.subheader("Gemini:")
                if response.text:
                    st.write(response.text)
                    # Save prompt, response, prompt ID, and date/time to JSON
                    data = load_or_create_json("generated_data.json")
                    prompt_id = len(data) + 1  # Generate prompt ID
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data.append({
                        "prompt_id": prompt_id,
                        "prompt": prompt,
                        "response": response.text,
                        "timestamp": timestamp
                    })
                    save_to_json(data, "generated_data.json")
                else:
                    st.write("No output from Gemini.")
            except Exception as e:
                st.write(f"An error occurred: {str(e)}")

# Run the Streamlit app
if __name__ == "__main__":
    text_page()
