import streamlit as st
import os
import tempfile
import zipfile
from io import BytesIO
import base64
from generate_carousel import generate_slides_with_ai, create_slide_html, generate_pdf_from_html, generate_html_from_slides as generate_html_from_slides_core
import json

def get_logo_base64():
    """Convert white logo to base64 for embedding in HTML"""
    try:
        with open("logo-white.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# Page configuration
st.set_page_config(
    page_title="LinkedIn Carousel Generator - ProjectWorkLab",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and hiding Streamlit elements
st.markdown("""
<style>
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide "Deploy" button */
    .stDeployButton {display: none;}
    
    /* Custom app styling */
    .main-header {
        padding: 2rem 1rem;
        background: linear-gradient(90deg, #61A9C8 0%, #335069 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .main-header h1 {
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #61A9C8;
        margin: 1rem 0;
    }
    .slide-preview {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background: white;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header with logo positioned to the left and centered text
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; margin-bottom: 1.5rem; padding-left: 2rem;">
            <img src="data:image/png;base64,{}" width="120" style="margin-right: 30px; flex-shrink: 0;">
            <div style="flex-grow: 1; text-align: center; padding-right: 150px;">
                <h1 style="margin: 0; font-size: 2.8rem;">LinkedIn Carousel Generator</h1>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Transform your Markdown content into professional LinkedIn carousel slides</p>
            </div>
        </div>
        <p style="font-size: 14px; opacity: 0.8; text-align: center;">Powered by ProjectWorkLab</p>
    </div>
    """.format(get_logo_base64()), unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # OpenAI API Key input
        api_key = st.text_input(
            "🔑 OpenAI API Key (Optional)",
            type="password",
            help="If you have your own OpenAI API key, use it here for full control. If not provided, we'll use ProjectWorkLab's corporate key with premium quality.",
            placeholder="sk-... (optional - we have corporate key)"
        )
        
        # Check for API key (user's or environment)
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            st.success("✅ Using your personal API Key - Full control!")
        else:
            # In production (Render), corporate key will be available
            # In local development, might not be
            if os.getenv('OPENAI_API_KEY'):
                st.success("✅ Using corporate API Key - Premium quality guaranteed!")
            else:
                st.warning("⚠️ No API key available - Output will be very basic")
                st.info("💡 Get your personal key at: https://platform.openai.com/api-keys")
        
        st.markdown("---")
        
        # Features info
        st.markdown("""
        ### 🚀 Features
        - **🤖 AI-Powered Analysis** (GPT-4)
        - **🎨 Professional Design**
        - **📱 LinkedIn Optimized** (1080x1080px)
        - **🧠 Smart Content Organization**
        - **🏢 Corporate Branding**
        
        ### ⚡ Operation Modes
        - **🏢 Corporate Key**: Premium quality automatic (default in production)
        - **👤 Personal Key**: Full control of your account and costs
        - **🔓 No Key**: Basic content only (local development)
        """)
        
        st.markdown("---")
        
        # Help section
        with st.expander("📖 How to Use"):
            st.markdown("""
            1. **Upload** your Markdown file or paste content
            2. **Configure** OpenAI API key (optional)
            3. **Generate** carousel slides
            4. **Preview** slides in browser
            5. **Download** PDF for LinkedIn
            """)
        
        with st.expander("💡 Tips for Best Results"):
            st.markdown("""
            - **🏢 Premium quality** automatically enabled in production
            - **🔑 Personal key** optional for cost control or local development
            - Use clear markdown structure (# ## ###)
            - Include statistics and numbers
            - Add case studies and results
            - Keep content business-focused
            - Use bullet points for organization
            """)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📄 Input Content")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Upload Markdown File", "Paste Content Directly"],
            horizontal=True
        )
        
        markdown_content = ""
        filename = "content"
        
        if input_method == "Upload Markdown File":
            uploaded_file = st.file_uploader(
                "Choose a Markdown file",
                type=['md', 'markdown', 'txt'],
                help="Upload your .md file to convert to carousel"
            )
            
            if uploaded_file is not None:
                # Read the file content
                markdown_content = uploaded_file.read().decode('utf-8')
                filename = os.path.splitext(uploaded_file.name)[0]
                
                st.success(f"✅ Loaded {len(markdown_content)} characters from {uploaded_file.name}")
                
                # Show preview of content
                with st.expander("📖 Preview Content"):
                    st.markdown(markdown_content[:1000] + "..." if len(markdown_content) > 1000 else markdown_content)
        
        else:
            markdown_content = st.text_area(
                "Paste your Markdown content here:",
                height=300,
                placeholder="""# Your Title Here

## Key Points
- Important point 1
- Important point 2
- Important point 3

## Statistics
- 75% improvement in efficiency
- 50% cost reduction
- 90% user satisfaction

## Case Study
Company X achieved remarkable results by implementing...
""",
                help="Paste your markdown content directly"
            )
            
            if markdown_content:
                filename = "pasted_content"
                st.info(f"📝 Content length: {len(markdown_content)} characters")

    with col2:
        st.header("🎨 Preview & Actions")
        
        if markdown_content:
            # Generate button
            if st.button("🚀 Generate Carousel", type="primary", use_container_width=True):
                with st.spinner("🔄 Generating carousel slides..."):
                    try:
                        # Generate slides
                        slides = generate_slides_with_ai(markdown_content)
                        
                        if slides:
                            st.session_state.slides = slides
                            st.session_state.filename = filename
                            st.success(f"✅ Generated {len(slides)} slides successfully!")
                        else:
                            st.error("❌ Failed to generate slides")
                    
                    except Exception as e:
                        st.error(f"❌ Error generating slides: {str(e)}")
        
        else:
            st.info("👆 Upload a file or paste content to get started")

    # Display generated slides
    if 'slides' in st.session_state and st.session_state.slides:
        st.markdown("---")
        st.header("🎯 Generated Slides")
        
        slides = st.session_state.slides
        filename = st.session_state.get('filename', 'carousel')
        
        # Slide navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            slide_index = st.selectbox(
                "Select slide to preview:",
                range(len(slides)),
                format_func=lambda x: f"Slide {x+1}: {slides[x].get('title', 'Untitled')[:30]}..."
            )
        
        # Display selected slide
        if slide_index < len(slides):
            slide = slides[slide_index]
            
            st.markdown(f"""
            <div class="slide-preview">
                <h3>📄 Slide {slide_index + 1}: {slide.get('title', 'Untitled')}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Show slide content based on type
            if slide.get('type') == 'title':
                st.markdown(f"**Title:** {slide.get('title', '')}")
                st.markdown(f"**Subtitle:** {slide.get('subtitle', '')}")
                if slide.get('highlight'):
                    st.markdown(f"**Highlight:** {slide.get('highlight', '')}")
            
            elif slide.get('type') == 'list':
                st.markdown(f"**Title:** {slide.get('title', '')}")
                st.markdown(f"**Subtitle:** {slide.get('subtitle', '')}")
                if slide.get('description'):
                    st.markdown(f"**Description:** {slide.get('description', '')}")
                if slide.get('items'):
                    st.markdown("**Items:**")
                    for item in slide.get('items', []):
                        st.markdown(f"• {item}")
            
            elif slide.get('type') == 'stat':
                st.markdown(f"**Title:** {slide.get('title', '')}")
                st.markdown(f"**Subtitle:** {slide.get('subtitle', '')}")
                if slide.get('stats'):
                    st.markdown("**Statistics:**")
                    for stat in slide.get('stats', []):
                        st.markdown(f"• {stat}")
            
            elif slide.get('type') == 'results':
                st.markdown(f"**Title:** {slide.get('title', '')}")
                st.markdown(f"**Subtitle:** {slide.get('subtitle', '')}")
                if slide.get('description'):
                    st.markdown(f"**Description:** {slide.get('description', '')}")
                if slide.get('cases'):
                    st.markdown("**Case Studies:**")
                    for case in slide.get('cases', []):
                        st.markdown(f"• {case}")
        
        # Download section
        st.markdown("---")
        st.header("📥 Download Files")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate HTML Preview", use_container_width=True):
                with st.spinner("🔄 Generating HTML..."):
                    try:
                        # Generate HTML content using core function
                        # Add final slide first
                        final_slide = {
                            "type": "final",
                            "title": "Ready to Transform Your Business?",
                            "subtitle": "Let's work together on your next project",
                            "description": "Professional consulting and digital solutions",
                            "cta_text": "Contact ProjectWorkLab"
                        }
                        all_slides = slides + [final_slide]
                        html_content = generate_html_from_slides_core(all_slides)
                        
                        # Create download button for HTML
                        st.download_button(
                            label="⬇️ Download HTML",
                            data=html_content,
                            file_name=f"{filename}_carousel.html",
                            mime="text/html",
                            use_container_width=True
                        )
                        
                        st.success("✅ HTML generated successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating HTML: {str(e)}")
        
        with col2:
            if st.button("📊 Generate PDF", use_container_width=True):
                with st.spinner("🔄 Generating PDF... This may take a moment"):
                    try:
                        # Generate HTML first using core function
                        # Add final slide first
                        final_slide = {
                            "type": "final",
                            "title": "Ready to Transform Your Business?",
                            "subtitle": "Let's work together on your next project",
                            "description": "Professional consulting and digital solutions",
                            "cta_text": "Contact ProjectWorkLab"
                        }
                        all_slides = slides + [final_slide]
                        html_content = generate_html_from_slides_core(all_slides)
                        
                        # Create temporary HTML file
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp_html:
                            tmp_html.write(html_content)
                            tmp_html_path = tmp_html.name
                        
                        # Generate PDF
                        pdf_path = tmp_html_path.replace('.html', '.pdf')
                        
                        # Show progress
                        progress_text = st.empty()
                        progress_text.text("🔄 Initializing PDF generation...")
                        
                        success = generate_pdf_from_html(tmp_html_path, pdf_path)
                        
                        progress_text.text("🔄 Checking PDF output...")
                        
                        if success and os.path.exists(pdf_path):
                            # Check file size
                            file_size = os.path.getsize(pdf_path)
                            progress_text.text(f"✅ PDF generated ({file_size} bytes)")
                            
                            # Read PDF file
                            with open(pdf_path, 'rb') as pdf_file:
                                pdf_data = pdf_file.read()
                            
                            # Create download button for PDF
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=pdf_data,
                                file_name=f"{filename}_carousel.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
                            st.success(f"✅ PDF generated successfully! ({len(pdf_data)} bytes)")
                            
                            # Cleanup
                            try:
                                os.unlink(tmp_html_path)
                                os.unlink(pdf_path)
                            except:
                                pass  # Ignore cleanup errors
                        else:
                            progress_text.text("❌ PDF generation failed")
                            st.error("❌ Failed to generate PDF")
                            st.info("💡 Try refreshing the page and generating again")
                            
                            # Show debug info
                            st.write(f"Debug info:")
                            st.write(f"- Success flag: {success}")
                            st.write(f"- PDF path exists: {os.path.exists(pdf_path) if pdf_path else 'No path'}")
                            st.write(f"- HTML path: {tmp_html_path}")
                            st.write(f"- PDF path: {pdf_path}")
                    
                    except Exception as e:
                        st.error(f"❌ Error generating PDF: {str(e)}")

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0; color: #666;">
            <p><strong>LinkedIn Carousel Generator</strong></p>
            <p>Developed by <a href="https://www.projectworklab.com" target="_blank" style="color: #61A9C8; text-decoration: none;">ProjectWorkLab</a></p>
            <p style="font-size: 12px; margin-top: 1rem;">Transform your content into professional LinkedIn carousels</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main() 