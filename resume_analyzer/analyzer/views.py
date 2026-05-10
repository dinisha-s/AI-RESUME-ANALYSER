import os
import PyPDF2

from groq import Groq
from django.shortcuts import render
from .models import ResumeAnalysis
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_text_from_pdf(pdf_file):

    reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def analyze_resume(request):

    feedback = None
    score = None

    if request.method == "POST" and request.FILES.get("resume"):

        pdf_file = request.FILES["resume"]

        resume_text = extract_text_from_pdf(pdf_file)

        prompt = f"""
        Analyze this resume and give:

        1. Score out of 100
        2. Strengths
        3. Weaknesses
        4. Missing skills

        Resume:
        {resume_text}
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        feedback = chat_completion.choices[0].message.content

        import re

        match = re.search(r'Score out of 100:\s*(\d+)', feedback)

        if match:
            score = int(match.group(1))
        else:
            score = 0

        ResumeAnalysis.objects.create(
            resume_text=resume_text,
            ai_feedback=feedback,
            score=score
        )

    return render(request, "analyzer/result.html", {
        "feedback": feedback,
        "score": score
    })