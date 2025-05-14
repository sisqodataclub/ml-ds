import markdown
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- Settings ---
openai_client = openai.OpenAI(api_key=api_key)
markdown_file = 'comparative.md'
html_file = 'g7br_file.html'

# --- Step 1: Convert Markdown to HTML ---
with open(markdown_file, 'r', encoding='utf-8') as f:
    md_text = f.read()

html_body = markdown.markdown(md_text)

# --- Step 2: Define your custom CSS ---
custom_css = """
<style>
    body {
        margin: 0;
        overflow-x: hidden;
    }

    img, .responsive-img {
        max-width: 100%;
        height: auto;
        display: block;
    }

    pre {
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    .responsive-img,
    #imageGallery img {
        width: 100%;
        height: auto;
        max-width: 100%;
        object-fit: contain;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        display: block;
    }

    .carousel-inner,
    .carousel-item {
        width: 100%;
    }

    .carousel {
        width: 100%;
        max-width: 600px;
        height: auto;
        margin: 0 auto;
        overflow: hidden;
    }

    .carousel-inner {
        position: relative;
        padding-top: 66.66%;
    }

    .carousel-item {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }

    .carousel-control-prev,
    .carousel-control-next {
        width: 10%;
    }

    .carousel-button:hover {
        background-color: rgba(0,0,0,0.8);
    }

    @media (max-width: 768px) {
        .carousel {
            max-width: 100%;
        }
    }
</style>
"""

# --- Step 3: Combine CSS with HTML ---
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GDP Growth Projections</title>
    {custom_css}
</head>
<body>
    {html_body}
</body>
</html>
"""

# --- Step 4: Write final HTML file ---
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Converted '{markdown_file}' to '{html_file}' with custom CSS.")
