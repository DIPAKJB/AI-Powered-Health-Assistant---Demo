import streamlit as st
import nltk
from transformers import pipeline
import re

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load a pre-trained Hugging Face model
chatbot = pipeline("text-generation", model="distilgpt2")

# Define healthcare and general conversational terms
healthcare_terms = [
    "symptom", "appointment", "medication", "emergency", "urgent", "test result", 
    "report", "vaccine", "vaccination", "allergy", "exercise", "fitness", "diet", 
    "nutrition", "mental health", "stress", "anxiety", "blood pressure", "hypertension",
    "diabetes", "heart disease", "cancer", "sleep", "insomnia", "pain", "ache", 
    "headache", "migraine", "fever", "infection"
]

general_terms = [
    "hi", "hello", "thank you", "goodbye", "name", "joke", "funny", "help", 
    "support", "how are you"
]

# Function to generate healthcare responses
def healthcare_chatbot(user_input):
    user_input_lower = user_input.lower()
    suggestions = []

    # Match healthcare-related terms
    for term in healthcare_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', user_input_lower):
            if term == "symptom":
                suggestions.append("It seems like you're experiencing symptoms. Please consult a doctor for accurate advice.")
            elif term == "appointment":
                suggestions.append("Would you like me to schedule an appointment with a doctor?")
            elif term == "medication":
                suggestions.append("It's important to take your prescribed medications regularly. If you have concerns, consult your doctor.")
            elif term == "emergency" or term == "urgent":
                suggestions.append("If this is a medical emergency, please call emergency services immediately.")
            elif term == "test result" or term == "report":
                suggestions.append("For accurate interpretation of test results, please consult your healthcare provider.")
            elif term == "vaccine" or term == "vaccination":
                suggestions.append("Vaccinations are crucial for preventing diseases. Please consult your doctor for the right schedule.")
            elif term == "allergy" or term == "allergic":
                suggestions.append("If you suspect an allergy, it's important to avoid the allergen and consult an allergist.")
            elif term == "exercise" or term == "fitness":
                suggestions.append("Regular exercise is vital for maintaining good health. Aim for at least 30 minutes a day.")
            elif term == "diet" or term == "nutrition":
                suggestions.append("A balanced diet is key to good health. Remember to include a variety of foods in your meals.")
            elif term == "mental health" or term == "stress" or term == "anxiety":
                suggestions.append("Mental health is just as important as physical health. If you're feeling stressed or anxious, consider reaching out to a mental health professional.")
            elif term == "blood pressure" or term == "hypertension":
                suggestions.append("Monitoring your blood pressure regularly is important. Please follow your doctor's advice for management.")
            elif term == "diabetes" or term == "blood sugar":
                suggestions.append("Managing diabetes involves monitoring blood sugar levels and following a healthy lifestyle. Please consult your doctor for personalized advice.")
            elif term == "heart disease" or term == "cardiac":
                suggestions.append("Heart health is critical. Regular check-ups and a healthy lifestyle are important for prevention and management.")
            elif term == "cancer":
                suggestions.append("Early detection is key in cancer treatment. Regular screenings and consultations with a healthcare provider are crucial.")
            elif term == "sleep" or term == "insomnia":
                suggestions.append("Good sleep hygiene is essential for overall health. If you're having trouble sleeping, consider consulting a doctor.")
            elif term == "pain" or term == "ache":
                suggestions.append("If you're experiencing persistent pain, it's important to consult a healthcare professional for proper diagnosis and treatment.")
            elif term == "headache" or term == "migraine":
                suggestions.append("Headaches can have various causes. If you experience frequent or severe headaches, consult a doctor.")
            elif term == "fever":
                suggestions.append("Fever can be a sign of infection. If you have a high or persistent fever, seek medical attention.")
            elif term == "infection":
                suggestions.append("If you suspect an infection, seek medical advice promptly for proper treatment.")

    # Match general conversational terms
    for term in general_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', user_input_lower):
            if term == "hi" or term == "hello":
                suggestions.append("Hello! How can I assist you today? 😊")
            elif term == "thank you":
                suggestions.append("You're welcome! I'm here to help you with any questions or concerns you might have.")
            elif term == "goodbye":
                suggestions.append("Goodbye! Take care and stay healthy. If you need any assistance, feel free to reach out anytime.")
            elif term == "name":
                suggestions.append("I'm your friendly AI Healthcare Assistant. How can I help you today?")
            elif term == "joke" or term == "funny":
                suggestions.append("Why did the doctor carry a red pen? In case they needed to draw blood! 😄")
            elif term == "help" or term == "support":
                suggestions.append("I'm here to assist you with any healthcare-related questions or concerns. How can I help?")

    # If no healthcare-specific or general responses match, generate a response using the model
    if not suggestions:
        response = chatbot(user_input, max_length=300, num_return_sequences=1)
        suggestions.append(response[0]['generated_text'])

    return suggestions

# Function to generate autocomplete suggestions
def autocomplete_suggestions(user_input, terms):
    user_input_lower = user_input.lower()
    suggestions = [term for term in terms if term.startswith(user_input_lower)]
    return suggestions

# Streamlit web app interface
def main():
    # Set up the web app title and input area
    st.title("AI Healthcare Assistant")
    
    # Add some styles to make the web app look professional
    st.markdown(
        """
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .title {
            color: #00aaff;
            font-family: 'Arial Black', Gadget, sans-serif;
        }
        .text-input {
            background-color: #ffffff;
            border: 1px solid #00aaff;
            border-radius: 10px;
            padding: 10px;
        }
        .button {
            background-color: #00aaff;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #007acc;
        }
        .button:active {
            transform: scale(0.98);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Set up the input area for user queries
    st.markdown('<h2 class="title">How Can I Assist You Today?</h2>', unsafe_allow_html=True)
    user_input = st.text_input("", "", key="user_input", help="Type your query here")

    # Display autocomplete suggestions as the user types
    if user_input:
        healthcare_suggestions = autocomplete_suggestions(user_input, healthcare_terms)
        general_suggestions = autocomplete_suggestions(user_input, general_terms)
        all_suggestions = healthcare_suggestions + general_suggestions
        if all_suggestions:
            st.write("Autocomplete Suggestions:")
            for suggestion in all_suggestions:
                st.markdown(f"- {suggestion}")

    # Display suggestions as the user types
    if user_input:
        with st.spinner("Getting suggestions..."):
            suggestions = healthcare_chatbot(user_input)
        st.write("Suggestions:")
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")

    # Set up the button for submitting the query
    def submit():
        st.session_state['submit_triggered'] = True

    # Handle form submission and trigger responses
    if st.session_state.get('submit_triggered'):
        st.session_state['submit_triggered'] = False
        if user_input:
            st.write("User:", user_input)
            with st.spinner("Processing your query, please wait..."):
                response = healthcare_chatbot(user_input)
            st.write("AI Healthcare Assistant:", response[0])

    # Display the submit button
    st.button("Submit", on_click=submit)

    # JavaScript for Enter key to submit
    st.markdown(
        """
        <script>
        document.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                document.querySelector("button[type='submit']").click();
            }
        });
        </script>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
