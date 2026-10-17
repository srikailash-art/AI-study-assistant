import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


# Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)


# Application heading
st.title("📚 AI Study Assistant")
st.write(
    "Your AI-powered learning companion. "
    "Create notes, understand concepts, generate quizzes "
    "and improve your answers."
)

st.divider()


# Student name
student_name = st.text_input(
    "Student name (optional)",
    placeholder="Enter your name"
)

if student_name.strip():
    st.caption(f"Welcome, {student_name.strip()}!")


# Check API key
if not API_KEY:
    st.error(
        "Gemini API key is missing. "
        "Add GEMINI_API_KEY to your .env file."
    )
    st.info(
        "Save the API key in .env, then restart or refresh "
        "the application."
    )
    st.stop()


# Create Gemini client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as error:
    st.error("Unable to initialize the Gemini API client.")
    st.code(str(error))
    st.stop()


# Common AI response function
def generate_response(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        answer = response.text

        if not answer or not answer.strip():
            raise ValueError("The AI returned an empty response.")

        return answer.strip()

    except Exception as error:
        message = str(error).lower()

        if isinstance(error, ValueError):
            st.error(str(error))

        elif any(word in message for word in [
            "api key", "unauthenticated", "permission_denied",
            "permission denied", "401", "403"
        ]):
            st.error(
                "API authentication failed. Check your Gemini "
                "API key and its permissions."
            )

        elif any(word in message for word in [
            "429", "quota", "resource_exhausted", "rate limit"
        ]):
            st.error(
                "API usage limit reached. Check your Gemini "
                "API quota and try again later."
            )

        elif any(word in message for word in [
            "404", "not_found", "not found"
        ]):
            st.error(
                f"Model '{MODEL}' was not found or is unavailable. "
                "Check the model name supported by your API key."
            )

        elif any(word in message for word in [
            "timeout", "timed out", "deadline exceeded"
        ]):
            st.error(
                "The request timed out. Check your internet "
                "connection and try again."
            )

        elif any(word in message for word in [
            "connection", "network", "connecterror"
        ]):
            st.error(
                "Connection problem. Check your internet "
                "connection and try again."
            )

        else:
            st.error(
                "The AI request failed. Check your API settings "
                "and try again."
            )
            st.caption(f"Technical details: {error}")

        return None


# Run a prompt and display the result
def run_ai(prompt, heading):
    with st.spinner("AI is working... Please wait."):
        result = generate_response(prompt)

    if result:
        st.subheader(heading)
        st.markdown(result)


# Feature tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Study Notes",
    "Text Summarizer",
    "Question Answering",
    "Concept Explainer",
    "Quiz Generator",
    "Answer Improvement"
])


# 1. AI STUDY NOTES GENERATOR
with tab1:
    st.header("📝 AI Study Notes Generator")
    st.write("Generate organized study notes for any subject.")

    notes_topic = st.text_input(
        "Enter subject or topic",
        placeholder="Example: Artificial Intelligence",
        key="notes_topic"
    )

    notes_level = st.selectbox(
        "Choose explanation level",
        ["Beginner", "Intermediate", "Exam preparation"],
        key="notes_level"
    )

    if st.button("Generate Study Notes"):
        if not notes_topic.strip():
            st.warning("Please enter a subject or topic.")
        else:
            prompt = f"""
You are an educational AI study assistant.

Create study notes about: {notes_topic.strip()}
Student level: {notes_level}

Requirements:
1. Start with a clear definition.
2. Explain the main concepts in simple English.
3. Organize important points under headings.
4. Use bullet points where appropriate.
5. Include a relevant example.
6. Include a short conclusion.
7. Keep the notes accurate and relevant.
8. Do not invent facts.

Format the response using Markdown headings and bullet points.
"""
            run_ai(prompt, "Generated Study Notes")


# 2. AI TEXT SUMMARIZER
with tab2:
    st.header("📄 AI Text Summarizer")
    st.write("Convert lengthy content into clear, useful summaries.")

    source_text = st.text_area(
        "Paste the text to summarize",
        height=220,
        key="source_text"
    )

    summary_style = st.selectbox(
        "Summary style",
        ["Bullet points", "Short paragraph", "Exam revision notes"],
        key="summary_style"
    )

    if st.button("Summarize Text"):
        if not source_text.strip():
            st.warning("Please enter some text to summarize.")
        else:
            prompt = f"""
You are an educational text summarizer.

Summarize the following content.
Summary style: {summary_style}

Requirements:
1. Preserve the original meaning.
2. Include the most important information.
3. Use simple, clear English.
4. Do not add facts that are not in the source.
5. Make the output easy to study.

Source text:
{source_text.strip()}
"""
            run_ai(prompt, "Summary")


# 3. AI QUESTION ANSWERING
with tab3:
    st.header("❓ AI Question Answering")
    st.write("Ask a question and receive a clear answer.")

    question = st.text_area(
        "Enter your question",
        height=120,
        key="student_question"
    )

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            prompt = f"""
You are a helpful educational AI assistant.

Answer this student's question accurately:
{question.strip()}

Instructions:
1. Use simple English.
2. Explain the main idea clearly.
3. Use headings or bullet points when useful.
4. Give an example when appropriate.
5. If the answer is uncertain, say so instead of guessing.
"""
            run_ai(prompt, "Answer")


# 4. AI CONCEPT EXPLAINER
with tab4:
    st.header("💡 AI Concept Explainer")
    st.write("Understand difficult concepts step by step.")

    concept = st.text_input(
        "Enter a concept",
        placeholder="Example: Machine Learning",
        key="concept"
    )

    concept_level = st.selectbox(
        "Explanation level",
        ["Very simple", "College student", "Detailed explanation"],
        key="concept_level"
    )

    if st.button("Explain Concept"):
        if not concept.strip():
            st.warning("Please enter a concept.")
        else:
            prompt = f"""
You are a patient teacher explaining concepts to a student.

Explain: {concept.strip()}
Required level: {concept_level}

Include:
1. Definition.
2. How it works.
3. Important points.
4. A simple real-world example.
5. A short recap.

Use clear, structured Markdown and avoid unnecessary jargon.
"""
            run_ai(prompt, "Concept Explanation")


# 5. AI QUIZ GENERATOR
with tab5:
    st.header("🧠 AI Quiz Generator")
    st.write("Generate practice multiple-choice questions.")

    quiz_topic = st.text_input(
        "Enter quiz topic",
        placeholder="Example: Python basics",
        key="quiz_topic"
    )

    quiz_count = st.selectbox(
        "Number of questions",
        [5, 10, 15, 20],
        key="quiz_count"
    )

    quiz_level = st.selectbox(
        "Quiz difficulty",
        ["Easy", "Medium", "Hard"],
        key="quiz_level"
    )

    if st.button("Generate Quiz"):
        if not quiz_topic.strip():
            st.warning("Please enter a quiz topic.")
        else:
            prompt = f"""
Create {quiz_count} multiple-choice practice questions
about: {quiz_topic.strip()}

Difficulty: {quiz_level}

For every question:
1. Give a numbered question.
2. Provide exactly four options: A, B, C and D.
3. Identify the correct answer.
4. Give a short explanation.

Use simple English and accurate answers.
Use clear Markdown formatting.
"""
            run_ai(prompt, "Generated Quiz")


# 6. AI ANSWER IMPROVEMENT
with tab6:
    st.header("✍️ AI Answer Improvement")
    st.write("Improve grammar, clarity and exam-answer structure.")

    student_answer = st.text_area(
        "Enter your original answer",
        height=200,
        key="student_answer"
    )

    answer_subject = st.text_input(
        "Subject or question (optional)",
        placeholder="Example: Define Artificial Intelligence",
        key="answer_subject"
    )

    if st.button("Improve Answer"):
        if not student_answer.strip():
            st.warning("Please enter your answer.")
        else:
            prompt = f"""
You are an educational answer-improvement assistant.

Subject or question:
{answer_subject.strip() if answer_subject.strip() else "Not provided"}

Student's original answer:
{student_answer.strip()}

Tasks:
1. Correct grammar and spelling.
2. Improve clarity and organization.
3. Correct factual mistakes when identifiable.
4. Preserve the student's intended meaning.
5. Do not add unsupported facts.
6. Show the improved answer first.
7. Then list the important corrections briefly.
8. Use simple English suitable for college study.
"""
            run_ai(prompt, "Improved Answer")


# Footer
st.divider()
st.caption(
    "AI Study Assistant | Powered by Gemini | "
    "Use AI-generated content as a study aid and verify important facts."
)