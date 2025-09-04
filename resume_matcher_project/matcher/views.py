import os
#import openai  # Commented out since not using OpenAI now
import numpy as np
import re
from django.conf import settings
from django.shortcuts import render
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import docx

from sentence_transformers import SentenceTransformer

# Comment out OpenAI API key setting
# openai.api_key = settings.OPENAI_API_KEY

# Load Sentence Transformer model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print(f"Warning: No text extracted from page {page_num+1}")
    print("DEBUG: PDF text length:", len(text))
    print("DEBUG: First 500 chars:", repr(text[:500]))
    return text


def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


# Commented out OpenAI embedding function
# def get_embedding(text):
#     client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
#     response = client.embeddings.create(
#         model="text-embedding-ada-002",
#         input=[text],
#     )
#     return response.data[0].embedding


def get_embedding(text):
    return model.encode([text])[0]


def semantic_match(resume_text, job_text):
    emb1 = np.array(get_embedding(resume_text)).reshape(1, -1)
    emb2 = np.array(get_embedding(job_text)).reshape(1, -1)
    score = cosine_similarity(emb1, emb2)[0][0]
    return score


def home(request):
    return render(request, 'home.html')


def match_resume(request):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description', '')

        resume_text = ''
        file_ext = ''
        if resume_file:
            file_ext = resume_file.name.split('.')[-1].lower()
            if file_ext == 'pdf':
                resume_text = extract_text_from_pdf(resume_file)
            elif file_ext == 'docx':
                resume_text = extract_text_from_docx(resume_file)
            else:
                try:
                    resume_text = resume_file.read().decode('utf-8')
                except UnicodeDecodeError:
                    resume_text = ''

        print("Resume file extension:", file_ext)
        print("Extracted resume text preview:", repr(resume_text[:500]))
        print("Job description preview:", repr(job_description[:500]))

        match_score = 0
        matched_words = set()
        try:
            if resume_text.strip() and job_description.strip():
                score = semantic_match(resume_text, job_description)
                match_score = round(score * 100, 2)

                resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
                job_words = set(re.findall(r'\b\w+\b', job_description.lower()))
                matched_words = resume_words.intersection(job_words)

                print("Matched keywords:", matched_words)
                print("Match score:", match_score)
            else:
                print("No resume text or job description to match.")
        except Exception as e:
            match_score = 0
            print("Error calculating similarity:", e)

        context = {
            'match_score': match_score,
            'matched_words': matched_words,
            'resume_text': resume_text,
            'job_description': job_description,
        }
        return render(request, 'result.html', context)
    return render(request, 'home.html')
