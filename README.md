# LinkedIn Carousel Generator

Convert any Markdown file into professional LinkedIn carousel slides with corporate branding.

## 🌐 **Web App Available!**

**🚀 [Try it online](https://your-app-name.onrender.com)** - No installation required!

## 🚀 Features

- **🌐 Web Interface**: User-friendly Streamlit app with drag & drop
- **AI-Powered Content Analysis**: Uses OpenAI GPT-4 to intelligently parse and structure markdown content
- **Professional Design**: Corporate-branded slides with custom color palette
- **Perfect LinkedIn Format**: 1080x1080px slides optimized for LinkedIn carousels
- **Smart Content Organization**: Automatically creates title, content, statistics, and CTA slides
- **Unique Icons**: AI selects relevant, non-repeating emojis for each slide
- **Adaptive Logos**: Different logo variants for different background contrasts
- **Multiple Input Methods**: Upload files or paste content directly
- **Instant Download**: Get HTML preview and PDF files immediately

## 📋 Requirements

- Python 3.7+
- OpenAI API key (optional, falls back to basic parsing)
- Required packages (see requirements.txt)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd md-to-carrusel
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**
```bash
playwright install
```

4. **Set up OpenAI API key (HIGHLY RECOMMENDED)**

Create a `.env` file in the project directory:
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Or manually create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

## 📁 Required Files

Make sure you have these logo files in your project directory:
- `logo.png` - Normal logo for light backgrounds
- `logo-white.png` - White logo for dark backgrounds  
- `logo-dark.png` - Dark logo for medium backgrounds

## 🎯 Usage

### 🌐 **Web App (Recommended)**
1. Visit the [online app](https://your-app-name.onrender.com)
2. Upload your Markdown file or paste content directly
3. Optionally add your OpenAI API key for AI-powered features
4. Click "Generate Carousel" and preview slides
5. Download HTML preview or PDF for LinkedIn

### 🚀 **Run Locally (Streamlit)**
```bash
streamlit run streamlit_app.py
```
Then open http://localhost:8501 in your browser.

### **Command Line Method**

**Windows:**
```bash
generate_carousel.bat "Marketing Report.md"
generate_carousel.bat "Sales Analysis.md"
generate_carousel.bat "Product Launch.md"
```

**macOS/Linux:**
```bash
./generate_carousel.sh "Marketing Report.md"
./generate_carousel.sh "Sales Analysis.md"
./generate_carousel.sh "Product Launch.md"
```

### **Direct Python Method**
```bash
python generate_carousel.py "Marketing Report.md"
python generate_carousel.py "Sales Analysis.md"
python generate_carousel.py "Product Launch.md"
```

## 📁 **Output Files**

The tool automatically generates unique output files based on your input:

**Input:** `Marketing Report.md`
- **HTML Preview:** `Marketing Report_carousel.html`
- **LinkedIn PDF:** `Marketing Report_carousel.pdf`

**Input:** `Sales Analysis 2024.md`
- **HTML Preview:** `Sales Analysis 2024_carousel.html`
- **LinkedIn PDF:** `Sales Analysis 2024_carousel.pdf`

## 🚀 **Batch Processing Multiple Files**

Process multiple reports quickly:

**Windows:**
```bash
generate_carousel.bat "Q1 Report.md"
generate_carousel.bat "Q2 Report.md"
generate_carousel.bat "Q3 Report.md"
generate_carousel.bat "Q4 Report.md"
```

**macOS/Linux:**
```bash
for file in *.md; do ./generate_carousel.sh "$file"; done
```

## 🤖 AI vs Basic Parsing

### With OpenAI API Key (ESSENTIAL for Quality)
- **Intelligent content analysis** and structure
- **Professional slide titles** and descriptions
- **Optimal content distribution** across slides
- **Relevant statistics** and case studies extraction
- **Engaging, business-focused** language
- **7-8 detailed, comprehensive slides**

### Without API Key (Very Basic Fallback)
- **Basic parsing** with simple slide structure
- **Generic titles** and content
- **Limited content organization**
- **Only 2 basic slides**
- **⚠️ NOT RECOMMENDED for professional use**

## 🎨 Customization

### Corporate Colors
The design uses a professional color palette:
- **Air Superiority Blue**: #61A9C8
- **Indigo Dye**: #335069  
- **Oxford Blue**: #1D273D
- **White**: #FFFFFF

### Slide Types
- **Title Slide**: Main introduction with gradient background
- **List Slides**: Key points with bullet format
- **Statistics Slides**: Number-focused content with metrics
- **Results Slides**: Case studies and proven outcomes
- **Final Slide**: Call-to-action with contact information

## 📊 Output Specifications

- **Dimensions**: 1080x1080px (1:1 aspect ratio)
- **Format**: PDF with individual slides
- **Quality**: High-resolution, print-ready
- **Compatibility**: Optimized for LinkedIn carousel format
- **File Size**: Optimized for web upload

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Set the OPENAI_API_KEY environment variable
- Or use the fallback basic parsing (still functional)

**"Playwright browser not found"**
```bash
playwright install chromium
```

**"Logo files not found"**
- Ensure logo.png, logo-white.png, and logo-dark.png are in the project directory

**"PDF generation failed"**
- Check that all dependencies are installed
- Verify the markdown file exists and is readable

## 💡 Tips for Best Results

1. **Use clear markdown structure** with proper headings (# ## ###)
2. **Include statistics and numbers** for automatic stat slide generation
3. **Add case studies and results** for results slide creation
4. **Keep content business-focused** for LinkedIn audience
5. **Use bullet points** for better slide organization

## 🚀 Example Workflow

```bash
# 1. Set up your environment
export OPENAI_API_KEY=your_key_here

# 2. Process your markdown file
python generate_carousel.py "Your Report.md"

# 3. Upload the generated PDF to LinkedIn
```

## 📈 Advanced Features

- **Automatic content chunking** for optimal slide length
- **Smart emoji selection** based on content context
- **Responsive logo placement** avoiding text overlap
- **Professional typography** with proper spacing
- **Corporate branding** throughout all slides

## 🤖 AI Model Options

### GPT-4 (Current Default - Recommended)
- **High-quality content** with detailed analysis
- **Professional business language** optimized for LinkedIn
- **Comprehensive slide generation** with rich context
- **Better reasoning** for complex content structuring
- **Cost**: ~$0.03-0.06 per input token, $0.06-0.12 per output token

### GPT-3.5-turbo (Fallback Option)
- **Cost-effective** for basic content generation
- **Faster processing** but less detailed output
- **Good for simple** markdown files
- **Cost**: ~$0.001-0.002 per token

### Future: o3-mini (When Available)
- **Advanced reasoning** capabilities
- **Cost-efficient** for complex analysis
- **Superior content quality** for business content
- **Expected**: Better than GPT-4 at lower cost

To change models, edit the `model` parameter in `generar_carrusel.py`:
```python
model="gpt-4"  # or "gpt-3.5-turbo" for cost savings
```

## 🚀 Deployment

### Deploy to Render (Free)

1. **Fork this repository** to your GitHub account
2. **Sign up** at [render.com](https://render.com)
3. **Create a new Web Service** and connect your GitHub repo
4. **Use these settings**:
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
5. **Set environment variables** (optional):
   - `OPENAI_API_KEY`: Your OpenAI API key for AI features
6. **Deploy** and get your live URL!

📖 **Detailed deployment guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

### Deploy to Other Platforms

- **Streamlit Cloud**: Connect GitHub repo directly
- **Heroku**: Use provided `Procfile` and `runtime.txt`
- **Railway**: One-click deploy from GitHub
- **DigitalOcean App Platform**: Deploy from GitHub

---

**Ready to create professional LinkedIn carousels from any markdown content!** 🎉 