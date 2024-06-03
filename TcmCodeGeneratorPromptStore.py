import datetime
import json
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import google.generativeai as genai
import streamlit as st
#This code for full width mode
st.set_page_config(layout="wide")

#This code for Logo
col1, col2 = st.columns([1, 2])
with col1:
    st.image("pics\logo.png", width=200)

#This code for Text color change
with col2:
    st.markdown(f"""
<h1 style="color: #039E0F;">TickingMinds AI CodeGenerator</h1> 
""", unsafe_allow_html=True)
os.environ["GOOGLE_API_KEY"] = "AIzaSyANYAfQgXVVTuwgYFJ6w0phR8DjPhcYc48"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Basic chatbot
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0,verbose=True)

radio_options = ["Java+Selenium+Testng", "python+Selenium+Testng", "selenide+Java+Testng"]  # Add more options as 
neededselected_option = st.radio("Choose an option:", radio_options)

java_selenium_testng = "Can you come up with a selenium test script using Java strictly following the below mentioned guidelines? (1) Java Class to identity the objects in a web page (2) Java Class to store any utilities and configuration (3) Import declaration of Selenium libraries (3) (i)Java Class to execute the test (3) (ii) - declaration for web driver  (3)(iii) - setup() method with annotation  @BeforeTest for declaring the driver and associated items (3) (iv) - Actual test annotated as @Test - refer the objects declared in (1) and do not declare or try to identify the objects separately (3) (v) - tearDown() method to close browser or clear out any other variables as required annotated as @AfterTest."
python_selenium_testng ="Can you come up with a selenium test script using python strictly following the below mentioned guidelines? (1) python Class to identity the objects in a web page (2) python Class to store any utilities and configuration (3) Import declaration of Selenium libraries (3) (i)python Class to execute the test (3) (ii) - declaration for web driver (3)(iii) - setup() method with annotation @BeforeTest for declaring the driver and associated items (3) (iv) - Actual test annotated as @Test - refer the objects declared in (1) and do not declare or try to identify the objects separately (3) (v) - tearDown() method to close browser or clear out any other variables as required annotated as @AfterTest."
selenide_java_testng = "Can you come up with a playwright test script using java strictly following the below mentioned guidelines? (1) java Class to identity the objects in a web page (2) java Class to store any utilities and configuration (3) Import declaration of Selenium libraries (3) (i)java Class to execute the test (3) (ii) - declaration for web driver (3)(iii) - setup() method with annotation @BeforeTest for declaring the driver and associated items (3) (iv) - Actual test annotated as @Test - refer the objects declared in (1) and do not declare or try to identify the objects separately (3) (v) - tearDown() method to close browser or clear out any other variables as required annotated as @AfterTest."

with st.form("my_form"):
    prompt1 = st.text_area("Enter the Test Scenario (Sample: Verify that users can search for trains by name and from to station to check their status and timings.)")
    prompt2 = st.text_area("Enter the Preconditions (Sample: Launch URL https://www.irctc.co.in/nget/ and login with username and password)")
    prompt3 = st.text_area("Enter the Expected Result (Sample: Validate train list is displayed with train name, train number, departure time, arrival time, duration, and running days.))")
    submitted = st.form_submit_button("Submit")

    # if submitted:
        # ConsolidatePrompt = prompt1 + prompt2 + prompt3

    if neededselected_option == "Java+Selenium+Testng":
        # Prompt template for Option 1
        dynamicPrompt_template1 = f"Test case steps:{prompt1}. Preconditions: {prompt2}. Expected Result: {prompt3}. {java_selenium_testng}"
    elif neededselected_option == "python+Selenium+Testng":
        # Prompt template for Option 2
        dynamicPrompt_template1 = f"Test case steps:{prompt1}. Preconditions: {prompt2}. Expected Result: {prompt3}. {python_selenium_testng}"
    elif neededselected_option == "selenide+Java+Testng":
        # Prompt template for Option 3
        dynamicPrompt_template1 = f"Test case steps:{prompt1}. Preconditions: {prompt2}. Expected Result: {prompt3}. {selenide_java_testng} "
    # Add more elif blocks for additional options as needed
        # Add more elif blocks for additional options as needed
    else:
        dynamicPrompt_template1 = f" {prompt1} {prompt2} {prompt3}. Here's the prompt for other options."

    dynamicPromptInput1 = PromptTemplate(
            input_variables=["prompt1", "prompt2", "prompt3"], template=dynamicPrompt_template1
        )
    dynamicPromptValues1 = {"prompt1": prompt1, "prompt2": prompt2, "prompt3": prompt3}
    gemini1 = LLMChain(llm=llm, prompt=dynamicPromptInput1)  # Moved this line inside the conditional block
    
    # Generate a unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Format timestamp as YYYYMMDD_HHMMSS
    filename = f"{neededselected_option}_{timestamp}.txt"

if prompt1 != "" and prompt2 != "" and prompt3 != "":
    placeholder = st.empty()
    clock_gif = "pics\Skateboarding.gif"  # Replace with your GIF path
    with placeholder.container():
        st.image(clock_gif)

        # Get prompt start time
        prompt_start_time = datetime.datetime.now()

        result = gemini1.run(**dynamicPromptValues1)

        # Get prompt end time
        prompt_end_time = datetime.datetime.now()

    placeholder.empty()  # Hide the clock GIF

    try:
        with open("prompts_and_responses.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {
            "prompts": [],
            "responses": [],
        }

    # Generate a unique prompt number
    prompt_number = len(data["prompts"]) + 1

    # Store prompt information in a dictionary
    prompt_data = {
        "PromptId": prompt_number,
        "prompt": dynamicPrompt_template1,
        "start_time": prompt_start_time.isoformat(),  # Store as ISO 8601 format
        "end_time": prompt_end_time.isoformat(),
        "promptResponse": result,
    }

    # Append prompt data and response to the lists
    data["prompts"].append(prompt_data)
    # data["responses"].append(result)

    with open("prompts_and_responses.json", "w") as f:
        json.dump(data, f, indent=4)

    st.write(result)
else:
    st.warning("Please fill all three fields.")