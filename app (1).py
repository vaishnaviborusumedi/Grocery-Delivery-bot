import streamlit as st
from google import genai
import os

# -------------------------------
# Configuration
# -------------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "models/gemini-flash-lite-latest"

SYSTEM_PROMPT = (
    "You are a grocery delivery order process explanation assistant. "
    "Provide general, informational responses only. "
    "Do not track orders, access accounts, or promise delivery times."
)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Grocery Delivery Bot", page_icon="🛒")
st.title("🛒 Grocery Delivery Process Explainer Bot")
st.write(
    "Ask questions about how grocery delivery works, including order stages, "
    "packing, substitutions, and delivery flow."
)

# FAQ buttons
st.subheader("Quick Questions")
faq_questions = [
    "How does grocery order delivery work?",
    "What happens if an item is unavailable?",
    "Explain the order packing process",
    "What are the delivery stages?"
]

for q in faq_questions:
    if st.button(q):
        st.session_state["user_input"] = q

# Text input
user_input = st.text_input(
    "Type your question here:",
    value=st.session_state.get("user_input", "")
)

# -------------------------------
# Generate Response
# -------------------------------
if user_input:
    with st.spinner("Thinking..."):
        try:
            # Combine system instruction + user question
            contents = f"{SYSTEM_PROMPT}\n\nUser Question: {user_input}"

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents
            )

            # Access text using `content` of the first candidate
            output_text = response.candidates[0].content
            st.markdown("### 🤖 Bot Response")
            st.write(output_text)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Footer
st.markdown("---")
st.caption("⚠️ This bot provides general information only. It cannot access or manage orders.")
