# 🧠 AI Content Intelligence Engine

A powerful AI-driven content analysis and strategy platform that helps marketing and sales teams understand content performance, identify gaps, and create data-driven content strategies.

## 🎯 Features

- **Content Audit & Analysis**: Analyze blogs, websites, case studies, and sales assets
- **Persona Mapping**: Automatically classify content by target persona
- **Funnel Stage Classification**: Map content to awareness, consideration, decision stages
- **Gap Analysis**: Identify missing content for each persona/stage combination
- **Content Strategy Recommendations**: AI-generated quarterly content plans
- **Persona Chat Agent**: Interactive AI agent trained on your persona research

## 📁 Project Structure

```
content-intelligence-engine/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration settings
├── utils/
│   ├── __init__.py
│   ├── content_analyzer.py     # Content analysis logic
│   ├── persona_manager.py      # Persona data handling
│   ├── gap_analyzer.py         # Gap analysis engine
│   ├── strategy_generator.py   # Content strategy AI
│   ├── pdf_processor.py        # PDF extraction utilities
│   └── web_scraper.py          # URL content extraction
├── components/
│   ├── __init__.py
│   ├── upload_section.py       # File upload UI
│   ├── analysis_dashboard.py   # Analysis results display
│   ├── gap_matrix.py           # Gap visualization
│   ├── persona_chat.py         # Persona chat interface
│   └── strategy_view.py        # Strategy recommendations UI
└── data/
    └── .gitkeep                # Placeholder for data files
```

## 🚀 Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/content-intelligence-engine.git
cd content-intelligence-engine
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key

Create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Or set it as an environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### 1. Upload Persona Research

- Navigate to **"📋 Persona Setup"** in the sidebar
- Upload your persona research PDF(s)
- The system will extract and structure persona data

### 2. Define Funnel Stages

- Go to **"🎯 Funnel Configuration"**
- Customize your funnel stages (default: Awareness, Consideration, Decision)
- Add stage descriptions and content type mappings

### 3. Add Content Assets

- Go to **"📥 Content Upload"**
- Choose input method:
  - **URLs**: Paste blog/website URLs
  - **PDFs**: Upload case studies, whitepapers
  - **Documents**: Upload sales assets, email templates
- Batch upload supported

### 4. Run Analysis

- Click **"🔍 Analyze Content"**
- View results in the **"📊 Analysis Dashboard"**:
  - Content inventory with classifications
  - Persona mapping scores
  - Funnel stage distribution

### 5. View Gap Analysis

- Navigate to **"🔲 Gap Matrix"**
- See visual heatmap of content coverage
- Identify missing persona/stage combinations

### 6. Get Strategy Recommendations

- Go to **"📈 Content Strategy"**
- View AI-generated recommendations:
  - Priority content to create
  - Content improvement suggestions
  - Quarterly content calendar

### 7. Chat with Persona Agent

- Open **"💬 Persona Chat"**
- Ask questions like:
  - "What are CFO Emma's main pain points?"
  - "What content resonates with technical buyers?"
  - "How should I position this feature for SMB owners?"

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Default personas (overridden by uploads)
DEFAULT_PERSONAS = ["CMO", "VP Marketing", "Content Manager"]

# Funnel stages
FUNNEL_STAGES = {
    "awareness": "Top of funnel - problem recognition",
    "consideration": "Middle of funnel - solution evaluation", 
    "decision": "Bottom of funnel - purchase decision"
}

# Content types
CONTENT_TYPES = ["blog", "case_study", "whitepaper", "email", "video", "webinar"]
```

## 📊 Output Examples

### Content Analysis Report

| Asset | Type | Persona | Stage | Intent | Score |
|-------|------|---------|-------|--------|-------|
| Blog: AI in Marketing | Blog | CMO | Awareness | Educational | 85% |
| Case Study: Acme Corp | Case Study | VP Marketing | Decision | Proof | 92% |

### Gap Matrix

|  | Awareness | Consideration | Decision |
|--|-----------|---------------|----------|
| CMO | ✅ Strong | ⚠️ Moderate | ❌ Gap |
| VP Marketing | ⚠️ Moderate | ✅ Strong | ✅ Strong |
| Developer | ❌ Gap | ❌ Gap | ⚠️ Moderate |

## 🛠️ Technical Details

- **Framework**: Streamlit
- **AI Model**: Claude (Anthropic API)
- **PDF Processing**: pdfplumber, pypdf
- **Web Scraping**: BeautifulSoup, requests
- **Visualization**: Plotly, Altair

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Support

For questions or issues, please open a GitHub issue.
