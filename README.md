# AI Resume Matcher

AI Resume Matcher is a Django web application that allows users to upload resumes (PDF, DOCX, TXT),
and semantically compare them with job descriptions using sentence-transformers embeddings. Get instant match scores and highlighted keywords, 
all running locally with no external API required.

## Features

- Upload resumes in multiple formats (PDF, DOCX, TXT)
- Semantic similarity matching with modern NLP embeddings
- Keyword extraction and highlighting for better insights
- Clean, responsive UI built with Bootstrap 5
- Open-source and free; no API keys needed

## Technologies

- Python 3 and Django web framework
- Sentence Transformers library for NLP embeddings
- pdfplumber and python-docx for text extraction
- scikit-learn for cosine similarity calculation
- Bootstrap 5 and Bootstrap Icons for UI

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/MukulKumar0852/your-repo-name.git
    ```
2. Navigate into the project directory:
    ```
    cd your-repo-name
    ```
3. Install required packages:
    ```
    pip install -r requirements.txt
    ```
4. Apply migrations:
    ```
    python manage.py migrate
    ```
5. Run the development server:
    ```
    python manage.py runserver
    ```
6. Open your browser and visit [http://localhost:8000](http://localhost:8000)

## Usage

- Upload your resume file.
- Enter or paste the job description.
- Submit to see your semantic match score and matched keywords.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


