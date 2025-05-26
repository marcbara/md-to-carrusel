# 🚀 Deployment Guide: Render

This guide will help you deploy the LinkedIn Carousel Generator to Render.

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **OpenAI API Key** (optional) - For AI-powered content analysis

## 🔧 Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your repository contains these files:
```
md-to-carrusel/
├── streamlit_app.py          # Main Streamlit app
├── generate_carousel.py      # Core logic
├── requirements.txt          # Python dependencies
├── packages.txt              # System packages
├── render.yaml              # Render configuration
├── .streamlit/config.toml   # Streamlit config
├── icons/                   # Icon assets
├── logo*.png               # Logo files
└── README.md               # Documentation
```

### 2. Create Render Service

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
2. **Click "New +"** → **"Web Service"**
3. **Connect GitHub**: Authorize Render to access your repositories
4. **Select Repository**: Choose your `md-to-carrusel` repository
5. **Configure Service**:
   - **Name**: `linkedin-carousel-generator` (or your choice)
   - **Region**: `Oregon` (or closest to you)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

### 3. Set Environment Variables

In the Render dashboard, add these environment variables:

**Required:**
- `STREAMLIT_SERVER_HEADLESS` = `true`
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS` = `false`

**Optional (for AI features):**
- `OPENAI_API_KEY` = `your_openai_api_key_here`

### 4. Deploy

1. **Click "Create Web Service"**
2. **Wait for Build**: First deployment takes 5-10 minutes
3. **Check Logs**: Monitor the build process in the logs tab
4. **Access Your App**: Use the provided `.onrender.com` URL

## 🎯 Post-Deployment

### Custom Domain (Optional)
1. Go to **Settings** → **Custom Domains**
2. Add your domain (e.g., `carousel.yourdomain.com`)
3. Update DNS records as instructed

### Monitoring
- **Logs**: Check application logs in the Render dashboard
- **Metrics**: Monitor CPU, memory, and response times
- **Health Checks**: Render automatically monitors your app

## 💰 Pricing

### Free Tier
- **750 hours/month** free compute time
- **Sleeps after 15 minutes** of inactivity
- **Wakes up** when accessed (30-60 seconds)
- **Perfect for testing** and low-traffic use

### Paid Plans
- **Starter ($7/month)**: Always-on, faster builds
- **Standard ($25/month)**: More resources, better performance

## 🔧 Troubleshooting

### Common Issues

**Build Fails:**
```bash
# Check logs for specific error
# Common fixes:
pip install --upgrade pip
playwright install chromium --with-deps
```

**App Won't Start:**
```bash
# Verify start command:
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

**PDF Generation Fails:**
- Ensure `packages.txt` includes all system dependencies
- Check Playwright installation in build logs
- Verify sufficient memory allocation

**Slow Performance:**
- Consider upgrading to paid plan
- Optimize image sizes
- Reduce OpenAI API calls

### Debug Commands

```bash
# Test locally first:
streamlit run streamlit_app.py

# Check Playwright:
playwright install chromium
python -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"

# Verify dependencies:
pip install -r requirements.txt
```

## 🚀 Going Live

### Share Your App
Once deployed, share your app URL:
```
https://your-app-name.onrender.com
```

### Usage Tips for Colleagues
1. **No Installation Required** - Just visit the URL
2. **Upload or Paste** markdown content
3. **Optional API Key** - Can use their own OpenAI key
4. **Download Results** - PDF ready for LinkedIn

### Analytics (Optional)
Consider adding:
- Google Analytics
- User feedback forms
- Usage tracking
- Error monitoring

## 📈 Scaling

### Performance Optimization
- **Caching**: Add `@st.cache_data` for expensive operations
- **Async Processing**: For large files
- **CDN**: For static assets

### Advanced Features
- **User Authentication**: Add login system
- **Database**: Store user preferences
- **API Endpoints**: For programmatic access
- **Batch Processing**: Handle multiple files

## 🆘 Support

### Resources
- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Playwright Docs**: [playwright.dev](https://playwright.dev)

### Getting Help
1. **Check Logs**: Most issues show up in deployment logs
2. **Render Community**: [community.render.com](https://community.render.com)
3. **GitHub Issues**: Create issues in your repository

---

## 🎉 Success!

Your LinkedIn Carousel Generator is now live and ready to help colleagues create professional carousel slides!

**Next Steps:**
- Test with sample content
- Share with colleagues
- Monitor usage and performance
- Consider adding premium features 