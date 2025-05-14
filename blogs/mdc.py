import markdown

import openai

from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")


# --- Settings ---
openai_client = openai.OpenAI(api_key=api_key)
markdown_file = 'gdp.md'
html_file = 'your_file.html'

# --- Step 1: Convert Markdown to HTML ---
with open(markdown_file, 'r', encoding='utf-8') as f:
    md_text = f.read()

html_content = markdown.markdown(md_text)

# Save the basic HTML file
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Converted '{markdown_file}' to '{html_file}' successfully.")


# --- Step 2: Open HTML content ---
with open(html_file, 'r', encoding='utf-8') as f:
    html_text = f.read()

# --- Step 3: Define your new Table of Contents ---
new_toc_html = """
<ul>
    <li><a href="#china-us-trade-war">China-US Trade War</a>
        <ul>
            <li><a href="#summary">Summary</a></li>
            <li><a href="#key-points-explained">Key Points Explained</a>
                <ol>
                    <li><a href="#what-are-tariffs">What Are Tariffs?</a></li>
                    <li><a href="#impact-on-the-us-economy">Impact on the US Economy</a></li>
                    <li><a href="#chinas-economic-challenges">China's Economic Challenges</a></li>
                    <li><a href="#global-effects">Global Effects</a></li>
                    <li><a href="#call-for-collaboration">Call for Collaboration</a></li>
                </ol>
            </li>
            <li><a href="#why-it-matters">Why It Matters</a></li>
        </ul>
    </li>
</ul>
"""

# --- Step 4: Send prompt to OpenAI to fix TOC ---

prompt = f"""
You are an expert HTML editor. Do NOT delete or alter any <img> tags or div blocks that contain images, including carousels, standalone visual charts, or any other images outside the carousel.

Your tasks:

1. Find and fully replace the current "Table of Contents" section with the following HTML:

{new_toc_html}

2. Add or correct `id` attributes on all headings (`<h1>`, `<h2>`, `<h3>`, etc.) so that each one has:
   - Do NOT delete or alter any <img> tags or div blocks that contain images (this includes images outside of carousels as well).
   - A lowercase ID,
   - Spaces replaced with hyphens,
   - All punctuation removed (except hyphens),
   - For example: <h2 id="china-us-trade-war">China-US Trade War</h2>

3. Convert any `<div class="carousel">...</div>` into a true slider carousel that includes:
   - Only one image visible at a time
   - Left and right arrow buttons (‹ and ›)
   - Smooth horizontal scrolling
   - Scroll snapping for better UX
   - Mobile and desktop compatibility
   - Wrap the entire carousel in a parent `<div class="carousel-wrapper">`
   - Use this updated working template for CSS and JS:

<-- inject the following into the <head> -->
<style>

body {{
            margin: 0;
            overflow-x: hidden;
        }}

        img, .responsive-img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}

        pre {{
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
    /* 3. Fully responsive images */
    .responsive-img,
    #imageGallery img {{
        width: 100%;
        height: auto;
        max-width: 100%;
        object-fit: contain;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        display: block;
    }}

    /* 4. Fix carousel responsiveness */
    .carousel-inner,
    .carousel-item {{
        width: 100%;
    }}

    /* Responsive carousel container */
    .carousel {{
        width: 100%;
        max-width: 600px;
        height: auto;
        margin: 0 auto;
        overflow: hidden;
    }}

    /* Maintain aspect ratio using padding hack */
    .carousel-inner {{
        position: relative;
        padding-top: 66.66%; /* 600 / 400 = 1.5 → 100 / 1.5 = 66.66% */
    }}

    .carousel-item {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }}

    /* Optional: Make control buttons more visible on mobile */
    .carousel-control-prev,
    .carousel-control-next {{
        width: 10%;
    }}

    .carousel-button:hover {{
        background-color: rgba(0,0,0,0.8);
    }}

    @media (max-width: 768px) {{
        .carousel {{
            max-width: 100%;
        }}
    }}
</style>
<-- inject the following <script> just before </body> -->
<script>
let currentIndex = 0;

function scrollCarousel(direction) {{
    const carousel = document.querySelector('.carousel');
    const totalItems = carousel.children.length;
    currentIndex += direction;

    if (currentIndex < 0) currentIndex = 0;
    if (currentIndex >= totalItems) currentIndex = totalItems - 1;

    carousel.scrollTo({{
        left: carousel.offsetWidth * currentIndex,
        behavior: 'smooth'
    }});
}}
</script>

4. Do NOT touch any images inside the carousel or any other images in the HTML (this includes images outside the carousel). Keep `src`, `alt`, and captions exactly the same.

5. Return the full modified HTML.

6. Ensure all modifications are well-formed and valid HTML.

Here is the HTML content to modify:

{html_text}
"""





response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful HTML editor."},
        {"role": "user", "content": prompt},
    ],
    temperature=0
)

fixed_html = response.choices[0].message.content

# --- Step 5: Save the fixed HTML back ---
fixed_html_file = 'your_file_fixed.html'
with open(fixed_html_file, 'w', encoding='utf-8') as f:
    f.write(fixed_html)

print(f"Fixed HTML saved to '{fixed_html_file}' successfully.")