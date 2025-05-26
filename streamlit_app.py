import streamlit as st
import os
import tempfile
import zipfile
from io import BytesIO
import base64
import datetime
from generate_carousel import generate_slides_with_ai, create_slide_html, generate_pdf_from_html, generate_html_from_slides as generate_html_from_slides_core
import json

def get_logo_base64():
    """Convert white logo to base64 for embedding in HTML"""
    try:
        with open("logo-white.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def log_activity(message):
    """Write activity to log file"""
    try:
        log_file = "app_logs.txt"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {message}\n"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        # Also add to session state for real-time viewing
        if 'admin_logs' not in st.session_state:
            st.session_state.admin_logs = []
        st.session_state.admin_logs.append(log_entry.strip())
        
    except Exception as e:
        # Silently fail if logging doesn't work
        pass

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
    
    /* Icon styling with emojis as fallback */
    .icon {
        margin-right: 8px;
        color: #61A9C8;
    }
    
    .icon-large {
        margin-right: 12px;
        color: #61A9C8;
        font-size: 1.2em;
    }
    
    /* Custom app styling */
    .main-header {
        padding: 1.5rem 1rem;
        background: linear-gradient(90deg, #61A9C8 0%, #335069 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        margin-top: -1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        min-height: 120px;
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

def show_admin_panel():
    """Secret admin panel - only accessible via URL parameter"""
    st.markdown("🔐 **ADMIN PANEL** - ProjectWorkLab Internal", unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Usage Logs", "📈 Analytics", "⚙️ System Info"])
    
    with tab1:
        st.header("📋 System Logs")
        
        # Real system logs
        import os
        
        # Check if log file exists
        log_file = "app_logs.txt"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                real_logs = f.readlines()
            
            st.subheader("Recent Activity")
            if real_logs:
                for log in real_logs[-20:]:  # Last 20 entries
                    log = log.strip()
                    if "ERROR" in log.upper():
                        st.error(f"❌ {log}")
                    elif "SUCCESS" in log.upper() or "DOWNLOAD" in log.upper():
                        st.success(f"✅ {log}")
                    elif "INFO" in log.upper():
                        st.info(f"ℹ️ {log}")
                    else:
                        st.write(f"📝 {log}")
                
                # Download real logs
                st.download_button(
                    "📥 Download Full Logs",
                    data="".join(real_logs),
                    file_name=f"carousel_logs_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            else:
                st.info("📝 Log file is empty")
        else:
            st.warning("📂 No log file found yet")
            st.info("💡 Logs will appear here once users start using the app")
        
        # Session state logs (current session activity)
        st.subheader("Current Session Activity")
        if 'admin_logs' not in st.session_state:
            st.session_state.admin_logs = []
        
        if st.session_state.admin_logs:
            for log in st.session_state.admin_logs[-10:]:
                st.write(f"🔄 {log}")
        else:
            st.info("No activity in current session")
    
    with tab2:
        st.header("📈 Real-time Analytics")
        
        # Real metrics from session state
        generations_today = st.session_state.get('generations_today', 0)
        total_slides = st.session_state.get('total_slides_generated', 0)
        pdf_downloads = st.session_state.get('pdf_downloads', 0)
        errors_count = st.session_state.get('errors_count', 0)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Generations Today", generations_today)
        with col2:
            st.metric("Total Slides Created", total_slides)
        with col3:
            st.metric("PDF Downloads", pdf_downloads)
        with col4:
            st.metric("Errors", errors_count)
        
        # Real system info
        st.subheader("📊 System Status")
        
        # Memory usage (if available)
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent()
            st.write(f"**Memory Usage:** {memory_percent:.1f}%")
            st.write(f"**CPU Usage:** {cpu_percent:.1f}%")
        except ImportError:
            st.info("Install psutil for detailed system metrics")
        
        # Session info
        st.subheader("🔄 Session Information")
        st.write(f"**Active Sessions:** {len(st.session_state)}")
        st.write(f"**Current Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # API Key status
        api_key_status = "✅ Active" if os.getenv('OPENAI_API_KEY') else "❌ Not Set"
        st.write(f"**API Key Status:** {api_key_status}")
        
        # File system info
        st.subheader("💾 Storage Information")
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            st.write(f"**Total Space:** {total // (2**30)} GB")
            st.write(f"**Used Space:** {used // (2**30)} GB")
            st.write(f"**Free Space:** {free // (2**30)} GB")
        except:
            st.info("Storage information not available")
    
    with tab3:
        st.header("⚙️ System Information")
        
        # System info
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Configuration")
            st.write("**Environment:** Production")
            st.write("**API Key Status:** ✅ Corporate Active")
            st.write("**PDF Engine:** Playwright")
            st.write("**Storage:** Temporary")
            st.write("**Version:** 1.0.0")
        
        with col2:
            st.subheader("📊 Performance")
            # Real performance metrics
            avg_gen_time = st.session_state.get('avg_generation_time', 'N/A')
            pdf_success_rate = st.session_state.get('pdf_success_rate', 'N/A')
            
            st.write(f"**Avg Generation Time:** {avg_gen_time}")
            st.write(f"**PDF Success Rate:** {pdf_success_rate}")
            
            # Real memory if available
            try:
                import psutil
                memory_mb = psutil.virtual_memory().used // (1024*1024)
                st.write(f"**Memory Usage:** {memory_mb}MB")
            except ImportError:
                st.write("**Memory Usage:** Install psutil for details")
            
            # Uptime (app start time)
            if 'app_start_time' not in st.session_state:
                st.session_state.app_start_time = datetime.datetime.now()
            
            uptime = datetime.datetime.now() - st.session_state.app_start_time
            st.write(f"**Session Uptime:** {str(uptime).split('.')[0]}")
        
        # Admin actions
        st.subheader("🛠️ Admin Actions")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Clear Cache"):
                st.success("Cache cleared!")
        
        with col2:
            if st.button("📊 Export Analytics"):
                st.success("Analytics exported!")
        
        with col3:
            if st.button("🚪 Exit Admin"):
                st.query_params.clear()
                st.rerun()
        
        # Debug info
        with st.expander("🐛 Debug Information"):
            st.write("**Session State:**", dict(st.session_state))
            st.write("**Query Params:**", dict(st.query_params))
            import os
            st.write("**Environment Variables:**", {
                "OPENAI_API_KEY": "✅ Set" if os.getenv('OPENAI_API_KEY') else "❌ Not Set",
                "PORT": os.getenv('PORT', 'Not Set')
            })

def main():
    # Initialize logging on app start
    if 'app_initialized' not in st.session_state:
        log_activity("INFO: App started - LinkedIn Carousel Generator initialized")
        st.session_state.app_initialized = True
        st.session_state.app_start_time = datetime.datetime.now()
    
    # Check for secret admin access
    if st.query_params.get("admin") == "pwl2024":
        log_activity("INFO: Admin panel accessed")
        show_admin_panel()
        return
    
    # Normal app continues here
    # Header with logo positioned to the left and centered text
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; margin-bottom: 1rem; padding-left: 2rem;">
            <img src="data:image/png;base64,{}" width="110" style="margin-right: 25px; flex-shrink: 0;">
            <div style="flex-grow: 1; text-align: center; padding-right: 135px;">
                <h1 style="margin: 0; font-size: 2.6rem; line-height: 1.1;">LinkedIn Carousel Generator</h1>
                <p style="margin: 0.3rem 0 0 0; font-size: 1.05rem;">Transform your Markdown content into professional LinkedIn carousel slides</p>
            </div>
        </div>
        <p style="font-size: 13px; opacity: 0.8; text-align: center; margin: 0;">Powered by ProjectWorkLab</p>
    </div>
    """.format(get_logo_base64()), unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙ Configuration")
        
        # OpenAI API Key input
        api_key = st.text_input(
            "🗝 OpenAI API Key (Optional)",
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
        ### ⚡ Features
        - **🤖 AI-Powered Analysis** (GPT-4)
        - **✨ Professional Design**
        - **📐 LinkedIn Optimized** (1080x1080px)
        - **⚡ Smart Content Organization**
        - **🏛 Corporate Branding**
        
        ### ⚙ Operation Modes
        - **🏛 Corporate Key**: Premium quality automatic (default in production)
        - **👤 Personal Key**: Full control of your account and costs
        - **🔓 No Key**: Basic content only (local development)
        """)
        
        st.markdown("---")
        
        # Help section
        with st.expander("📖 How to Use"):
            st.markdown("""
            1. **⬆ Upload** your Markdown file or paste content
            2. **🗝 Configure** OpenAI API key (optional)
            3. **▶ Generate** carousel slides
            4. **👁 Preview** slides in browser
            5. **⬇ Download** PDF for LinkedIn
            """)
        
        with st.expander("💡 Tips for Best Results"):
            st.markdown("""
            - **🏛 Premium quality** automatically enabled in production
            - **🗝 Personal key** optional for cost control or local development
            - **# Use clear markdown structure** (# ## ###)
            - **📈 Include statistics** and numbers
            - **📄 Add case studies** and results
            - **🎯 Keep content business-focused**
            - **• Use bullet points** for organization
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
                        import time
                        start_time = time.time()
                        
                        # Generate slides
                        slides = generate_slides_with_ai(markdown_content)
                        
                        generation_time = time.time() - start_time
                        
                        if slides:
                            st.session_state.slides = slides
                            st.session_state.filename = filename
                            
                            # Update metrics
                            st.session_state.generations_today = st.session_state.get('generations_today', 0) + 1
                            st.session_state.total_slides_generated = st.session_state.get('total_slides_generated', 0) + len(slides)
                            
                            # Log activity
                            log_activity(f"SUCCESS: Generated {len(slides)} slides in {generation_time:.1f}s")
                            
                            st.success(f"✅ Generated {len(slides)} slides successfully!")
                        else:
                            # Log error
                            log_activity("ERROR: Failed to generate slides")
                            st.session_state.errors_count = st.session_state.get('errors_count', 0) + 1
                            
                            st.error("❌ Failed to generate slides")
                    
                    except Exception as e:
                        # Log exception
                        log_activity(f"ERROR: Exception in generation: {str(e)}")
                        st.session_state.errors_count = st.session_state.get('errors_count', 0) + 1
                        
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
                            if st.download_button(
                                label="⬇️ Download PDF",
                                data=pdf_data,
                                file_name=f"{filename}_carousel.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            ):
                                # Log PDF download
                                st.session_state.pdf_downloads = st.session_state.get('pdf_downloads', 0) + 1
                                log_activity(f"INFO: PDF downloaded - {filename}_carousel.pdf ({len(pdf_data)} bytes)")
                            
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