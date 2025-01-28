##pip install google-generativeai

import streamlit as st
# import google.generativeai as genai
from datetime import datetime, timedelta

# Configure the API key for Google Generative AI
surya_api_key = "AIzaSyCu2susiqMRwXoSPdgreHNMcemLXMOFY4M"  # Your API key
genai.configure(api_key=surya_api_key)

# Initialize the generative model for Google AI
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get date-related responses for the AI Chat
def get_date_info(user_input):
    """Return date-related information based on user query."""
    today_date = datetime.now()

    if 'today' in user_input.lower():
        return f"Today's date is {today_date.strftime('%Y-%m-%d')}."

    if 'tomorrow' in user_input.lower():
        tomorrow = today_date + timedelta(days=1)
        return f"Tomorrow's date is {tomorrow.strftime('%Y-%m-%d')}."

    if 'yesterday' in user_input.lower():
        yesterday = today_date - timedelta(days=1)
        return f"Yesterday's date was {yesterday.strftime('%Y-%m-%d')}."

    if 'day' in user_input.lower() and 'week' in user_input.lower():
        return f"Today is {today_date.strftime('%A')}."

    if 'next thursday' in user_input.lower():
        current_day = today_date.weekday()
        days_until_thursday = (3 - current_day) if current_day <= 3 else (10 - current_day)
        next_thursday = today_date + timedelta(days=days_until_thursday)
        return f"The next Thursday will be on {next_thursday.strftime('%Y-%m-%d')}."

    return None

# Function to add background image for the main app
def set_background_image(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to set custom font style and size in code
def set_font_style_and_size(font_family, font_size):
    st.markdown(
        f"""
        <style>
        .stApp {{
            font-family: '{font_family}';
            font-size: {font_size}px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to set font size for text_area
def set_text_area_font_size(font_size):
    st.markdown(
        f"""
        <style>
        .stTextArea textarea {{
            font-size: {font_size}px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit app
def main():
    # Set background image for main app
    set_background_image("https://t3.ftcdn.net/jpg/06/27/85/70/360_F_627857071_bREuJgK1MTU5YcTPTfgJPOYZ86F1l421.jpg")
    
    # Dynamic font size slider for code output and text_area
    # font_size = st.slider("Select Font Size for Text Area and Code", min_value=10, max_value=50, value=18)  # Dynamic font size

    # Apply the selected font size to code blocks and text_area
    #set_font_style_and_size("Arial", font_size)
    #set_text_area_font_size(font_size)
    
    # Sidebar for navigation between functionalities
    option = st.sidebar.selectbox("Choose functionality", ("Surya's AI Chatbot",))

    # AI Chat
    if option == "Surya's AI Chatbot":
        st.header("Surya's AI Chatbot")
        st.write("This is a chatbot created by Surya Vishal")

        # Initialize conversation history in session state
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        # Initialize message_id to track unique question inputs
        if "message_id" not in st.session_state:
            st.session_state.message_id = 0

        # Display the conversation history
        for message in st.session_state.conversation_history:
            if message.startswith("You:"):
                st.markdown(f"**{message}**")
            else:
                st.markdown(f"{message}")

        # Input and button for AI Chat
        user_input = st.text_input(
            "**Enter your question:**", 
            key=f"user_input_{st.session_state.message_id}", 
            placeholder="Type your question here..."
        )

        if st.button("Submit") and user_input:
            # Add user input to the conversation history
            st.session_state.conversation_history.append(f"You: {user_input}")

            # Check for date-related responses
            date_response = get_date_info(user_input)
            if date_response:
                st.session_state.conversation_history.append(f"**Surya's AI Response:** {date_response}")
            else:
                # Generate a response using the AI model
                try:
                    context = "\n".join(st.session_state.conversation_history)
                    response = model.generate_content(f"{context}\nAI:")
                    response_text = response.text  # Adjust this if necessary

                    # Highlight "Subplots" if mentioned
                    if "Subplots" in response_text:
                        response_text = response_text.replace("Subplots", "**Subplots**")

                    st.session_state.conversation_history.append(f"**Surya's AI Response:** {response_text}")
                except Exception as e:
                    st.error(f"Error generating response: {e}")
                    return

            # Increment message_id to generate a new input box for next question
            st.session_state.message_id += 1

if __name__ == "__main__":
    main()
