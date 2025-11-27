# 🧠 AI Content Intelligence Engine

A powerful AI-driven content analysis and strategy platform using **OpenAI GPT-4**.

## 🎯 Features

- **Content Audit & Analysis**: Analyze blogs, websites, case studies, and sales assets
- **Persona Mapping**: Automatically classify content by target persona
- **Funnel Stage Classification**: Map content to awareness, consideration, decision stages
- **Gap Analysis**: Identify missing content for each persona/stage combination
- **Content Strategy Recommendations**: AI-generated quarterly content plans
- **Persona Chat Agent**: Interactive AI agent trained on your persona research

## 🚀 Quick Start

### Step 1: Clone/Download the Project

```bash
git clone https://github.com/yourusername/content-intelligence-engine.git
cd content-intelligence-engine
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Key

```bash
# Copy example env file
cp env.example .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/api-keys
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

## 📖 How to Use

| Step | Page | What to Do |
|------|------|------------|
| 1 | 📋 Persona Setup | Upload persona research PDFs or add personas manually |
| 2 | 📥 Content Upload | Upload blogs, case studies, PDFs, or paste URLs |
| 3 | 🔍 Analyze | Click "Run Analysis" to classify all content |
| 4 | 📊 Dashboard | View content inventory, quality scores, charts |
| 5 | 🔲 Gap Matrix | See heatmap of coverage gaps by persona/stage |
| 6 | 📈 Strategy | Get AI-generated quarterly content plan |
| 7 | 💬 Persona Chat | Ask questions about personas for content/sales |

## 📁 Project Structure

```
content-intelligence-engine/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variables template
├── utils/
│   ├── content_analyzer.py     # AI content classification
│   ├── persona_manager.py      # Persona data & chat agent
│   ├── gap_analyzer.py         # Coverage gap detection
│   ├── strategy_generator.py   # AI strategy recommendations
│   ├── pdf_processor.py        # PDF text extraction
│   └── web_scraper.py          # URL content extraction
├── components/
│   ├── upload_section.py       # File/URL upload UI
│   ├── analysis_dashboard.py   # Results visualization
│   ├── gap_matrix.py           # Gap heatmap & charts
│   ├── persona_chat.py         # Chat interface
│   └── strategy_view.py        # Strategy recommendations UI
└── data/                       # Data storage
```

## 🔧 Configuration

Edit `config.py` to customize:

- **MODEL_NAME**: Change to `gpt-4o-mini` for lower costs
- **DEFAULT_PERSONAS**: Pre-configured personas
- **FUNNEL_STAGES**: Customer journey stages
- **SCORING_THRESHOLDS**: Gap analysis thresholds

## 💰 Cost Considerations

- **gpt-4o**: Best quality, higher cost (~$5-15 per 1M tokens)
- **gpt-4o-mini**: Good quality, lower cost (~$0.15-0.60 per 1M tokens)

Change the model in `config.py`:
```python
MODEL_NAME = "gpt-4o-mini"  # For lower costs
```

## 📝 License

MIT License
