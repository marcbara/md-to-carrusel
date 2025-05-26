import re
import os
import sys
import requests
import markdown
from bs4 import BeautifulSoup
# from weasyprint import HTML
from playwright.sync_api import sync_playwright
import openai
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURACIÓN ---
def main():
    # Get input file from command line argument - REQUIRED
    if len(sys.argv) > 1:
        INPUT_MD = sys.argv[1]
        print(f"📄 Processing: {INPUT_MD}")
    else:
        print("❌ Error: No markdown file specified!")
        print("💡 Usage: python generate_carousel.py [markdown_file.md]")
        print("📝 Example: python generate_carousel.py 'Marketing Report.md'")
        print("📋 Available batch scripts:")
        print("   Windows: generate_carousel.bat 'Your File.md'")
        print("   macOS/Linux: ./generate_carousel.sh 'Your File.md'")
        sys.exit(1)

    # Generate output filenames based on input
    base_name = os.path.splitext(os.path.basename(INPUT_MD))[0]
    OUTPUT_HTML = f"{base_name}_carousel.html"
    OUTPUT_PDF = f"{base_name}_carousel.pdf"

    print(f"📁 Output files: {OUTPUT_HTML}, {OUTPUT_PDF}")

    return INPUT_MD, OUTPUT_HTML, OUTPUT_PDF

# Only run main when script is executed directly
if __name__ == "__main__":
    INPUT_MD, OUTPUT_HTML, OUTPUT_PDF = main()

ICON_DIR = "icons"
ICON_FALLBACK = "file-text"
ICON_SOURCE_URL = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/"

# OpenAI API configuration
# Create a .env file with: OPENAI_API_KEY=your_key_here
# Or get your API key from: https://platform.openai.com/api-keys
openai.api_key = os.getenv('OPENAI_API_KEY')

os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs("temp", exist_ok=True)

# --- Descargar icono si no existe ---
def get_icon_svg(keyword):
    icon_name = keyword.lower().strip().replace(" ", "-")
    icon_path = os.path.join(ICON_DIR, f"{icon_name}.svg")
    if os.path.exists(icon_path):
        return icon_path
    url = f"{ICON_SOURCE_URL}{icon_name}.svg"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(icon_path, "w", encoding="utf-8") as f:
                f.write(r.text)
            return icon_path
    except:
        pass
    # fallback
    fallback_path = os.path.join(ICON_DIR, f"{ICON_FALLBACK}.svg")
    if not os.path.exists(fallback_path):
        fallback_url = f"{ICON_SOURCE_URL}{ICON_FALLBACK}.svg"
        r = requests.get(fallback_url)
        if r.status_code == 200:
            with open(fallback_path, "w", encoding="utf-8") as f:
                f.write(r.text)
    return fallback_path

def read_markdown_file(input_md):
    """Read markdown file and return content"""
    if not os.path.exists(input_md):
        print(f"❌ Error: File '{input_md}' not found!")
        print(f"💡 Usage: python generar_carrusel.py [markdown_file.md]")
        print(f"📝 Example: python generar_carrusel.py 'Marketing Report.md'")
        sys.exit(1)

    try:
        with open(input_md, "r", encoding="utf-8") as f:
            md_text = f.read()
        print(f"✅ Successfully loaded {len(md_text)} characters from {input_md}")
        return md_text
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

# --- AI-powered content analysis and slide generation ---
def generate_slides_with_ai(md_text):
    """Use OpenAI to intelligently parse markdown and create structured slides"""
    
    if not openai.api_key:
        print("⚠️  OpenAI API key not found. Please set OPENAI_API_KEY in .env file.")
        print("   Falling back to basic parsing...")
        return create_fallback_slides(md_text)
    
    try:
        # Truncate content if too long to fit within token limits
        max_content_length = 3000  # Leave room for prompt and response
        if len(md_text) > max_content_length:
            md_text = md_text[:max_content_length] + "\n\n[Content truncated for processing...]"
        
        prompt = f"""Create exactly 7-8 comprehensive LinkedIn carousel slides from this markdown content. Each slide should be detailed, informative, and engaging for business professionals. 

IMPORTANT: Return ONLY valid JSON with proper string formatting (no nested arrays). DO NOT include a final/CTA slide - we'll add that separately.

YOU MUST GENERATE EXACTLY 7-8 CONTENT SLIDES. Here's the structure to follow:

[
  {{"type": "title", "title": "Main Title", "subtitle": "Comprehensive subtitle", "highlight": "📊 Single key insight with context"}},
  {{"type": "stat", "title": "Key Statistics & Market Data", "subtitle": "Numbers that matter", "stats": ["💰 Specific statistic with full context, implications, and business impact (40-60 words)", "📈 Detailed metric with background information and trend analysis (40-60 words)", "🎯 Important number with business impact explanation and context (40-60 words)", "🚀 Additional statistic with supporting details and relevance (40-60 words)"]}},
  {{"type": "list", "title": "Core Concepts & Fundamentals", "subtitle": "Essential knowledge", "description": "Foundational understanding and key principles", "items": ["🚀 Comprehensive point with details and context (30-50 words)", "💡 In-depth insight with explanation and implications (30-50 words)", "📊 Detailed finding with context and business impact (30-50 words)", "🎯 Actionable takeaway with specific implementation steps (30-50 words)", "⚡ Additional insight with supporting details (30-50 words)"]}},
  {{"type": "list", "title": "Platforms & Tools Analysis", "subtitle": "Technology landscape", "description": "Comprehensive overview of available solutions", "items": ["🔧 Platform analysis with features and capabilities (35-55 words)", "💼 Tool comparison with pros and cons (35-55 words)", "📱 Technology assessment with use cases (35-55 words)", "⚙️ Solution evaluation with implementation considerations (35-55 words)"]}},
  {{"type": "results", "title": "Case Studies & Success Stories", "subtitle": "Proven outcomes and real results", "description": "Real-world examples and their significance", "cases": ["🏢 Detailed company case study with specific results, metrics, and implementation details (50-70 words)", "🚀 Comprehensive success story with metrics, timeline, and business impact (50-70 words)", "📊 In-depth example with measurable outcomes and lessons learned (50-70 words)"]}},
  {{"type": "list", "title": "Implementation Strategies", "subtitle": "Practical approaches and methodologies", "description": "Step-by-step guidance for success", "items": ["🎯 Strategic approach with step-by-step implementation guidance (35-55 words)", "💡 Best practice with detailed explanation and expected outcomes (35-55 words)", "🔧 Practical methodology with tools and resources needed (35-55 words)", "📈 Success factor with measurement criteria and benchmarks (35-55 words)"]}},
  {{"type": "list", "title": "Future Trends & Strategic Recommendations", "subtitle": "What's next and expert guidance", "description": "Forward-looking insights and strategic direction", "items": ["🚀 Emerging trend with impact analysis and preparation strategies (35-55 words)", "💡 Strategic recommendation with implementation timeline and resources (35-55 words)", "🎯 Future opportunity with market analysis and positioning advice (35-55 words)", "⚡ Innovation area with competitive advantage potential (35-55 words)", "🔮 Long-term prediction with strategic implications (35-55 words)"]}},
  {{"type": "list", "title": "Advanced Insights & Expert Tips", "subtitle": "Professional guidance and best practices", "description": "Advanced strategies for maximum impact", "items": ["🎓 Expert insight with professional context and application (35-55 words)", "🏆 Advanced strategy with competitive advantages (35-55 words)", "💎 Premium tip with exclusive knowledge and benefits (35-55 words)", "🔥 Power technique with measurable results (35-55 words)"]}}
]

CRITICAL REQUIREMENTS:
- MUST generate exactly 7-8 content slides (excluding the final CTA slide we add separately)
- Each slide must be substantial with detailed, professional content
- "highlight" must be a SINGLE STRING, not an array
- "items", "stats", "cases" must be arrays of strings
- Each bullet point should be 30-70 words with comprehensive context and explanations
- Include specific numbers, percentages, and concrete examples where available
- Use professional LinkedIn business language with actionable insights
- Extract and elaborate on key statistics, case studies, and strategic recommendations
- Use diverse, relevant emojis (no repetition within the same slide)
- Focus on actionable business insights, practical takeaways, and strategic guidance
- Make each slide substantial and informative for business decision-makers
- DO NOT include a final/CTA slide in your response

Content to analyze:
{md_text}"""

        response = openai.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for better content quality and reasoning
            messages=[
                {"role": "system", "content": "You are a LinkedIn content expert who creates comprehensive, detailed carousel slides. Always generate exactly 7-8 content slides with substantial, professional content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000  # Increased significantly for more detailed content
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content.strip()
        
        # Clean up the response to ensure it's valid JSON
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        
        # Remove any leading/trailing whitespace and newlines
        content = content.strip()
        
        # Try to find JSON array if response contains extra text
        import re
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        
        slides = json.loads(content)
        
        # Validate that slides is a list
        if not isinstance(slides, list):
            raise ValueError("OpenAI response is not a valid list of slides")
        
        # Validate each slide has required fields
        for i, slide in enumerate(slides):
            if not isinstance(slide, dict) or 'type' not in slide:
                raise ValueError(f"Slide {i} is not a valid slide object")
            
            # Fix any array fields that should be strings
            if 'highlight' in slide and isinstance(slide['highlight'], list):
                slide['highlight'] = slide['highlight'][0] if slide['highlight'] else "📊 Key insight"
            
            # Ensure items/stats/cases are properly formatted
            for field in ['items', 'stats', 'cases']:
                if field in slide and isinstance(slide[field], list):
                    # Flatten any nested arrays
                    flattened = []
                    for item in slide[field]:
                        if isinstance(item, list):
                            flattened.extend(item)
                        else:
                            flattened.append(str(item))
                    slide[field] = flattened[:6]  # Limit to 6 items max
        
        print(f"✅ Generated {len(slides)} slides using OpenAI gpt-4")
        return slides
        
    except Exception as e:
        print(f"⚠️  OpenAI API error: {e}")
        print("   Falling back to basic parsing...")
        return create_fallback_slides(md_text)

def create_fallback_slides(md_text):
    """Fallback method if OpenAI API is not available"""
    title_match = re.search(r'^# (.+)', md_text, re.MULTILINE)
    main_title = title_match.group(1).strip() if title_match else INPUT_MD.replace('.md', '').replace('_', ' ').replace('-', ' ').title()
    
    return [
        {
            "type": "title",
            "title": main_title,
            "subtitle": "Professional Guide & Analysis",
            "highlight": "📊 Comprehensive Overview"
        },
        {
            "type": "list",
            "title": "Key Insights",
            "subtitle": "Main takeaways",
            "description": "Essential information from the content",
            "items": [
                "🚀 Important point one",
                "💡 Key insight two", 
                "📊 Critical finding three"
            ]
        }
    ]

def process_markdown_to_carousel(input_md, output_html, output_pdf):
    """Main processing function to convert markdown to carousel"""
    # Read the markdown file
    md_text = read_markdown_file(input_md)
    
    # Generate slides using AI
    slides_content = generate_slides_with_ai(md_text)

    # Remove any final slides that might have been generated by AI or fallback
    slides_content = [slide for slide in slides_content if slide.get("type") != "final"]
    
    return slides_content, md_text

def add_final_slide(slides_content):
    """Add the final CTA slide to the carousel"""
    final_slide = {
        "type": "final",
        "title": "Ready to Transform Your Business?",
        "subtitle": "Let's work together on your next project",
        "description": "Professional consulting and digital solutions",
        "cta_text": "Contact ProjectWorkLab"
    }
    
    # Append the final slide (don't replace)
    slides_content.append(final_slide)
    return slides_content

# --- Generate professional HTML ---
def create_slide_html(slide):
    if slide["type"] == "title":
        return f"""
        <section class="slide title-slide">
            <div class="logo logo-white"></div>
            <div class="slide-content">
                <h1>{slide["title"]}</h1>
                <h2>{slide["subtitle"]}</h2>
                <div class="highlight">{slide["highlight"]}</div>
            </div>
        </section>
        """
    
    elif slide["type"] == "stat":
        stats_html = "".join([f"<div class='stat-item'>{stat}</div>" for stat in slide["stats"]])
        return f"""
        <section class="slide stat-slide">
            <div class="logo logo-normal"></div>
            <div class="slide-content">
                <h2>{slide["title"]}</h2>
                <div class="stats-grid">{stats_html}</div>
                <p class="subtitle">{slide["subtitle"]}</p>
            </div>
        </section>
        """
    
    elif slide["type"] in ["platforms", "comparison", "tools", "trends", "capabilities", "list"]:
        items_html = "".join([f"<div class='item'>{item}</div>" for item in slide["items"]])
        subtitle_html = f"<p class='subtitle'>{slide['subtitle']}</p>" if "subtitle" in slide else ""
        description_html = f"<p class='description'>{slide['description']}</p>" if "description" in slide else ""
        return f"""
        <section class="slide list-slide">
            <div class="logo logo-normal"></div>
            <div class="slide-content">
                <h2>{slide["title"]}</h2>
                {subtitle_html}
                {description_html}
                <div class="items-list">{items_html}</div>
            </div>
        </section>
        """
    
    elif slide["type"] == "results":
        cases_html = "".join([f"<div class='case'>{case}</div>" for case in slide["cases"]])
        subtitle_html = f"<p class='subtitle'>{slide['subtitle']}</p>" if "subtitle" in slide else ""
        description_html = f"<p class='description'>{slide['description']}</p>" if "description" in slide else ""
        return f"""
        <section class="slide results-slide">
            <div class="logo logo-dark"></div>
            <div class="slide-content">
                <h2>{slide["title"]}</h2>
                {subtitle_html}
                {description_html}
                <div class="cases-grid">{cases_html}</div>
            </div>
        </section>
        """
    
    elif slide["type"] == "recommendations":
        sections_html = "".join([f"<div class='rec'>{section}</div>" for section in slide["sections"]])
        subtitle_html = f"<p class='subtitle'>{slide['subtitle']}</p>" if "subtitle" in slide else ""
        description_html = f"<p class='description'>{slide['description']}</p>" if "description" in slide else ""
        return f"""
        <section class="slide recommendations-slide">
            <div class="logo logo-white"></div>
            <div class="slide-content">
                <h2>{slide["title"]}</h2>
                {subtitle_html}
                {description_html}
                <div class="recommendations-grid">{sections_html}</div>
            </div>
        </section>
        """
    
    elif slide["type"] == "cta":
        steps_html = "".join([f"<div class='step'>{step}</div>" for step in slide["steps"]])
        description_html = f"<p class='description'>{slide['description']}</p>" if "description" in slide else ""
        return f"""
        <section class="slide cta-slide">
            <div class="logo logo-white"></div>
            <div class="slide-content">
                <h2>{slide["title"]}</h2>
                <h3>{slide["subtitle"]}</h3>
                {description_html}
                <div class="steps">{steps_html}</div>
                <div class="highlight">{slide["highlight"]}</div>
            </div>
        </section>
        """
    
    elif slide["type"] == "final":
        return f"""
        <section class="slide final-slide">
            <div class="logo-center"></div>
            <h2>{slide["title"]}</h2>
            <h3>{slide["subtitle"]}</h3>
            <p class="description">{slide["description"]}</p>
            <a href="https://www.projectworklab.com" target="_blank" class="cta-button">{slide["cta_text"]}</a>
            <p style="font-size: 16px; margin-top: 30px; opacity: 0.7;">ProjectWorkLab.com</p>
        </section>
        """

def generate_html_from_slides(slides_content):
    """Generate complete HTML from slides"""
    # Generar todas las slides
    slides_html = "".join([create_slide_html(slide) for slide in slides_content])

    # --- HTML final con diseño profesional ---
    final_html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    @page {
      size: 1080px 1080px;
      margin: 0;
      padding: 0;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    html, body {
      width: 1080px;
      height: auto;
      margin: 0;
      padding: 0;
    }
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: white;
      width: 1080px;
    }
    
    .slide {
      width: 1080px !important;
      height: 1080px !important;
      min-width: 1080px !important;
      max-width: 1080px !important;
      min-height: 1080px !important;
      max-height: 1080px !important;
      display: flex;
      align-items: center;
      justify-content: center;
      page-break-after: always;
      page-break-inside: avoid;
      position: relative;
      overflow: hidden;
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    .slide-content {
      width: 100%;
      max-width: 900px;
      padding: 40px 50px 60px 50px;
      text-align: center;
    }
    
    /* Title Slide */
    .title-slide {
      background: linear-gradient(135deg, #61A9C8 0%, #335069 100%);
      color: white;
    }
    
    .title-slide h1 {
      font-size: 56px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 25px;
      letter-spacing: -0.02em;
    }
    
    .title-slide h2 {
      font-size: 28px;
      font-weight: 400;
      opacity: 0.9;
      margin-bottom: 35px;
    }
    
    .title-slide .highlight {
      font-size: 24px;
      font-weight: 600;
      background: rgba(255,255,255,0.2);
      padding: 18px 35px;
      border-radius: 50px;
      display: inline-block;
    }
    
    /* Stat Slide */
    .stat-slide {
      background: linear-gradient(135deg, #dfeef4 0%, #c0dce9 100%);
      color: #1D273D;
    }
    
    .stat-slide h2 {
      font-size: 36px;
      font-weight: 700;
      margin-bottom: 40px;
      color: #335069;
      line-height: 1.1;
    }
    
    .stats-grid {
      display: grid;
      gap: 20px;
      margin-bottom: 35px;
    }
    
    .stat-item {
      font-size: 26px;
      font-weight: 600;
      padding: 18px;
      background: rgba(97,169,200,0.2);
      border-radius: 18px;
      border-left: 6px solid #61A9C8;
      line-height: 1.2;
    }
    
    .stat-slide .subtitle {
      font-size: 20px;
      font-style: italic;
      opacity: 0.8;
    }
    
    /* List Slides */
    .list-slide {
      background: linear-gradient(135deg, #FFFFFF 0%, #dfeef4 100%);
      color: #1D273D;
    }
    
    .list-slide h2 {
      font-size: 36px;
      font-weight: 700;
      margin-bottom: 12px;
      color: #335069;
      line-height: 1.1;
    }
    
    .list-slide .subtitle {
      font-size: 20px;
      margin-bottom: 6px;
      opacity: 0.8;
      font-weight: 500;
      color: #61A9C8;
    }
    
    .list-slide .description {
      font-size: 16px;
      margin-bottom: 25px;
      opacity: 0.7;
      font-style: italic;
      line-height: 1.3;
    }
    
    .items-list {
      display: grid;
      gap: 20px;
      text-align: left;
    }
    
    .item {
      font-size: 22px;
      font-weight: 500;
      padding: 16px 22px;
      background: rgba(97,169,200,0.1);
      border-radius: 12px;
      border-left: 5px solid #61A9C8;
      line-height: 1.2;
    }
    
    /* Results Slide */
    .results-slide {
      background: linear-gradient(135deg, #c0dce9 0%, #a0cbde 100%);
      color: #1D273D;
    }
    
    .results-slide h2 {
      font-size: 36px;
      font-weight: 700;
      margin-bottom: 12px;
      color: #335069;
      line-height: 1.1;
    }
    
    .results-slide .subtitle {
      font-size: 20px;
      margin-bottom: 6px;
      opacity: 0.8;
      font-weight: 500;
      color: #1D273D;
    }
    
    .results-slide .description {
      font-size: 16px;
      margin-bottom: 25px;
      opacity: 0.7;
      font-style: italic;
      line-height: 1.3;
    }
    
    .cases-grid {
      display: grid;
      gap: 20px;
      text-align: left;
    }
    
    .case {
      font-size: 22px;
      font-weight: 600;
      padding: 18px 22px;
      background: rgba(255,255,255,0.6);
      border-radius: 12px;
      border-left: 5px solid #335069;
      line-height: 1.2;
    }
    
    /* Recommendations Slide */
    .recommendations-slide {
      background: linear-gradient(135deg, #80bad2 0%, #61A9C8 100%);
      color: white;
    }
    
    .recommendations-slide h2 {
      font-size: 42px;
      font-weight: 700;
      margin-bottom: 15px;
      color: white;
    }
    
    .recommendations-slide .subtitle {
      font-size: 22px;
      margin-bottom: 8px;
      opacity: 0.9;
      font-weight: 500;
    }
    
    .recommendations-slide .description {
      font-size: 18px;
      margin-bottom: 30px;
      opacity: 0.8;
      font-style: italic;
      line-height: 1.4;
    }
    
    .recommendations-grid {
      display: grid;
      gap: 25px;
      text-align: left;
    }
    
    .rec {
      font-size: 26px;
      font-weight: 600;
      padding: 25px;
      background: rgba(255,255,255,0.2);
      border-radius: 15px;
      border-left: 6px solid white;
      line-height: 1.3;
    }
    
    /* CTA Slide */
    .cta-slide {
      background: linear-gradient(135deg, #335069 0%, #1D273D 100%);
      color: white;
    }
    
    .cta-slide h2 {
      font-size: 46px;
      font-weight: 800;
      margin-bottom: 15px;
      color: #61A9C8;
    }
    
    .cta-slide h3 {
      font-size: 24px;
      font-weight: 500;
      margin-bottom: 8px;
      opacity: 0.9;
    }
    
    .cta-slide .description {
      font-size: 18px;
      margin-bottom: 30px;
      opacity: 0.8;
      font-style: italic;
      line-height: 1.4;
    }
    
    .steps {
      display: grid;
      gap: 18px;
      margin-bottom: 35px;
      text-align: left;
    }
    
    .step {
      font-size: 20px;
      font-weight: 600;
      padding: 18px 22px;
      background: rgba(97,169,200,0.2);
      border-radius: 12px;
      line-height: 1.3;
    }
    
    .cta-slide .highlight {
      font-size: 22px;
      font-weight: 700;
      background: #61A9C8;
      padding: 18px 25px;
      border-radius: 20px;
      display: inline-block;
      color: white;
    }
    
    /* Logo base styles */
    .logo {
      position: absolute;
      top: -20px;
      right: 50px;
      width: 180px;
      height: 180px;
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center;
      opacity: 0.95;
      z-index: 10;
    }
    
    /* Logo for light backgrounds (normal logo) */
    .logo-normal {
      background-image: url('logo.png');
    }
    
    /* Logo for dark backgrounds (white logo) */
    .logo-white {
      background-image: url('logo-white.png');
    }
    
    /* Logo for medium backgrounds (dark logo) */
    .logo-dark {
      background-image: url('logo-dark.png');
    }
    
    /* Final slide - centered logo */
    .final-slide {
      background: linear-gradient(135deg, #1D273D 0%, #335069 100%);
      color: white;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }
    
    .final-slide .logo-center {
      width: 250px;
      height: 250px;
      background-image: url('logo-white.png');
      background-size: contain;
      background-repeat: no-repeat;
      background-position: center;
      margin-bottom: 40px;
      opacity: 1;
    }
    
    .final-slide h2 {
      font-size: 48px;
      font-weight: 800;
      margin-bottom: 20px;
      color: #61A9C8;
    }
    
    .final-slide h3 {
      font-size: 28px;
      font-weight: 500;
      margin-bottom: 15px;
      opacity: 0.9;
    }
    
    .final-slide .description {
      font-size: 20px;
      margin-bottom: 40px;
      opacity: 0.8;
      font-style: italic;
      line-height: 1.4;
    }
    
    .final-slide .cta-button {
      font-size: 24px;
      font-weight: 700;
      background: #61A9C8;
      color: white;
      padding: 20px 40px;
      border-radius: 30px;
      display: inline-block;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 8px 20px rgba(97,169,200,0.3);
      text-decoration: none;
      transition: all 0.3s ease;
    }
    
    .final-slide .cta-button:hover {
      background: #335069;
      transform: translateY(-2px);
      box-shadow: 0 12px 25px rgba(97,169,200,0.4);
    }
    
    /* Print optimizations */
    @media print {
      .slide {
        -webkit-print-color-adjust: exact;
        color-adjust: exact;
        print-color-adjust: exact;
      }
    }
  </style>
</head>
<body>
""" + slides_html + """
</body>
</html>
"""
    return final_html

def save_and_generate_files(slides_content, output_html, output_pdf):
    """Save HTML and generate PDF files"""
    # Generate HTML
    final_html = generate_html_from_slides(slides_content)
    
    # --- Save and export PDF ---
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    # Generate PDF
    success = generate_pdf_from_html(output_html, output_pdf)
    return success

def generate_pdf_from_html(html_path, pdf_path):
    """Generate PDF from HTML file using Playwright"""
    try:
        import asyncio
        import sys
        import threading
        
        # Try different approaches for Windows compatibility
        if sys.platform == "win32":
            # Method 1: Use thread with new event loop
            result = [False]
            exception = [None]
            
            def run_in_thread():
                try:
                    # Create completely isolated event loop
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        result[0] = loop.run_until_complete(_generate_pdf_async(html_path, pdf_path))
                    finally:
                        loop.close()
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=run_in_thread)
            thread.start()
            thread.join(timeout=60)  # 60 second timeout
            
            if exception[0]:
                raise exception[0]
            
            return result[0]
        else:
            # Linux/Mac - use direct async approach
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(_generate_pdf_async(html_path, pdf_path))
            finally:
                loop.close()
            
    except Exception as e:
        print(f"Error generating PDF: {e}")
        # Fallback: try sync playwright as last resort
        try:
            return _generate_pdf_sync_fallback(html_path, pdf_path)
        except Exception as e2:
            print(f"Fallback PDF generation also failed: {e2}")
            return False

def _generate_pdf_sync_fallback(html_path, pdf_path):
    """Fallback sync PDF generation"""
    try:
        from playwright.sync_api import sync_playwright
        import subprocess
        import os
        
        # Try to run playwright in a subprocess to avoid event loop conflicts
        script_content = f'''
import sys
from playwright.sync_api import sync_playwright

def generate_pdf():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({{"width": 1080, "height": 1080}})
        page.goto("file:///{os.path.abspath(html_path)}")
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)
        
        page.pdf(
            path="{pdf_path}",
            width="1080px",
            height="1080px",
            margin={{"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"}},
            print_background=True
        )
        browser.close()
        return True

if __name__ == "__main__":
    try:
        result = generate_pdf()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"Error: {{e}}")
        sys.exit(1)
'''
        
        # Write script to temp file
        script_path = "temp_pdf_generator.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Run in subprocess
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=60)
        
        # Cleanup
        if os.path.exists(script_path):
            os.remove(script_path)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Sync fallback failed: {e}")
        return False

async def _generate_pdf_async(html_path, pdf_path):
    """Async PDF generation function"""
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(
            viewport={'width': 1080, 'height': 1080},
            device_scale_factor=2  # Higher DPI for better quality
        )
        page = await context.new_page()
        
        # Load the HTML file
        await page.goto(f"file:///{os.path.abspath(html_path)}")
        
        # Wait for everything to load
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)  # Longer wait for better rendering
        
        # Force exact LinkedIn carousel dimensions with better styling
        await page.evaluate("""
            // Remove all default margins and padding
            document.body.style.width = '1080px';
            document.body.style.height = 'auto';
            document.body.style.overflow = 'hidden';
            document.body.style.margin = '0';
            document.body.style.padding = '0';
            document.documentElement.style.margin = '0';
            document.documentElement.style.padding = '0';
            
            // Ensure each slide is exactly 1080x1080
            const slides = document.querySelectorAll('.slide');
            slides.forEach((slide, index) => {
                slide.style.width = '1080px';
                slide.style.height = '1080px';
                slide.style.minHeight = '1080px';
                slide.style.maxHeight = '1080px';
                slide.style.boxSizing = 'border-box';
                slide.style.margin = '0';
                slide.style.padding = '0';
                slide.style.position = 'relative';
                slide.style.pageBreakAfter = 'always';
                slide.style.pageBreakInside = 'avoid';
                
                // Ensure fonts are loaded
                slide.style.fontFamily = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
                
                // Force background colors to print
                slide.style.webkitPrintColorAdjust = 'exact';
                slide.style.colorAdjust = 'exact';
                slide.style.printColorAdjust = 'exact';
            });
            
            // Add print styles
            const style = document.createElement('style');
            style.textContent = `
                @media print {
                    * {
                        -webkit-print-color-adjust: exact !important;
                        color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }
                    .slide {
                        page-break-after: always !important;
                        page-break-inside: avoid !important;
                    }
                }
            `;
            document.head.appendChild(style);
        """)
        
        # Generate PDF with exact LinkedIn carousel dimensions
        await page.pdf(
            path=pdf_path,
            format=None,  # Use custom dimensions
            width='1080px',
            height='1080px', 
            margin={'top': '0px', 'right': '0px', 'bottom': '0px', 'left': '0px'},
            print_background=True,
            prefer_css_page_size=True,  # Use CSS page size
            display_header_footer=False,
            scale=1.0,
            outline=False,
            tagged=False
        )
        
        await browser.close()
        return True

if __name__ == "__main__":
    # Process the markdown file
    slides_content, md_text = process_markdown_to_carousel(INPUT_MD, OUTPUT_HTML, OUTPUT_PDF)
    
    # Add final slide
    slides_content = add_final_slide(slides_content)
    
    # Save and generate files
    success = save_and_generate_files(slides_content, OUTPUT_HTML, OUTPUT_PDF)
    
    if success:
        print(f"✅ PDF generated: {OUTPUT_PDF}")
        print(f"📐 Dimensions: 1080x1080px (aspect ratio 1:1 - LinkedIn carousel standard)")
        print(f"📁 File ready to upload to LinkedIn")
        print(f"🎉 Carousel generated from: {INPUT_MD}")
        print(f"📄 HTML preview: {OUTPUT_HTML}")
        print(f"📱 LinkedIn PDF: {OUTPUT_PDF}")
    else:
        print(f"❌ Failed to generate PDF: {OUTPUT_PDF}")
