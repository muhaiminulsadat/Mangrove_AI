# 🌿 Mangrove AI Protector

**Mangrove AI Protector** is a satellite deforestation intelligence platform built for the Sundarbans ecosystem. It uses an 8-node LangGraph pipeline combining Gemini 2.5 Vision, deterministic NDVI spectral analysis, IPCC Tier 1 carbon accounting, and ecosystem impact modelling to assess mangrove health and deforestation risks in real-time.

Built by **Team Green Flare** for the **Eco-Tech Hackathon 2026 (Environment Watch: BUET)**.

---

## ⚡ Features

- **8-Node LangGraph Pipeline**: A state graph that conditionally routes image data through validation, spectral analysis, AI detection, and scoring.
- **Zero-AI & AI Hybrid**: Combines deterministic logic (NDVI, Carbon accounting) with Gemini Vision for high-accuracy bounding box detection.
- **IPCC Tier 1 Carbon Accounting**: Estimates carbon stock, loss, CO2 equivalent, and economic losses in BDT.
- **Ecosystem Impact**: Calculates species at risk, coastal vulnerability, and natural vs. assisted recovery timelines.
- **Rich Dashboard**: Built with Streamlit, showing damage maps, heatmaps, carbon science tabs, and downloadable JSON/CSV reports.

## 🛠️ Tech Stack
- **Frontend/UI**: Streamlit
- **AI/LLM**: Google Gemini (gemini-2.5-flash)
- **Agentic Workflow**: LangGraph, Langchain
- **Image Processing**: Pillow (PIL), NumPy
- **Data Viz**: Plotly

## 📋 Prerequisites
- Python 3.9+
- A Google Gemini API Key

## 🚀 Installation & Setup

1. **Clone the repository** (or extract the project folder):
   ```bash
   git clone <repo-url>
   cd mangrove_ai
   ```

2. **Set up a virtual environment** (recommended to keep things clean):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Gemini API Key**:
   Create a `.env` file in the root directory (or `.streamlit/secrets.toml`) and add your key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
   *Note: If you don't add it here, the app will prompt you to enter the API key directly in the sidebar on the UI.*

## 💻 How to Run

Launch the Streamlit app by running:
```bash
streamlit run app.py
```

The app will open automatically in your browser (usually at `http://localhost:8501`). 

### Usage Steps:
1. Provide your Gemini API key (if not already set in `.env`).
2. Upload a satellite or aerial image of a mangrove region (PNG, JPG, TIFF).
3. Adjust the **AI Temperature** and **Max Box Area** settings in the sidebar if needed.
4. Hit the **"🚀 Execute Pipeline"** button.
5. Wait for the 8-node LangGraph pipeline to complete processing. Check out the generated maps, heatmaps, and detailed analysis tabs. You can download the full JSON report or CSV data from the main interface.

## 🧩 Pipeline Architecture

Our LangGraph StateGraph contains 8 distinct nodes:
1. **N1: Validator** - Rejects non-satellite images.
2. **N2: Spectral** - Performs NDVI pixel analysis (Zero AI) to find vegetation properties.
3. **N3: Detector** - Gemini Vision bounds potential hotspots.
4. **N4: Cross-Val** - Verifies AI bounding boxes against spectral masks.
5. **N5: Carbon** - Calculates biomass, CO2 equivalent, and economic loss.
6. **N6: Ecosystem** - Maps biodiversity loss and calculates habitat indices.
7. **N7: Reporter** - Synthesizes insights into human-readable scientific text.
8. **N8: Scorer** - Generates the final 5-signal composite confidence and health scores.

## 🤝 Team
**Team Green Flare**
- Eco-Tech Hackathon 2026
- Track: Environment Watch (BUET)

--- 
*Let's protect our coastal guardians. 🌿*
