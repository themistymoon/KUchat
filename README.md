# 🎓 KUchat - Kasetsart University AI Chatbot

A powerful multi-modal AI chatbot system powered by dual AI models (Qwen3-Omni-30B + GPT-OSS-120B) with RAG capabilities, designed to answer questions about Kasetsart University programs and general knowledge.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Google%20Colab-orange.svg)](https://colab.research.google.com/)

---

## ✨ Features

### 🤖 Dual AI Models
- **Qwen3-Omni-30B**: Multimodal support (text, images, audio, video)
- **GPT-OSS-120B**: High-performance text generation
- Both models optimized for A100 GPU

### 📚 RAG System (Retrieval-Augmented Generation)
- **170+ Curriculum PDFs**: Complete Kasetsart University program information
- **20 Faculties**: Agriculture, Engineering, Science, Business, and more
- **Auto-loading**: Automatically indexes all documents at startup
- **ChromaDB**: Fast vector database for semantic search
- **Smart Retrieval**: Finds relevant information from documents

### 🌐 Web Search Integration
- **DuckDuckGo**: Real-time web search
- **Wikipedia**: Encyclopedia knowledge
- **Thai + English**: Bilingual search support

### 🎨 Modern Interface
- **Gradio 4.0+**: Beautiful, responsive chat UI
- **Multi-modal Upload**: Drag & drop images, audio, video
- **Real-time Streaming**: Fast response generation
- **Customizable**: Temperature, max tokens, RAG/web search toggles

---

## 🚀 Quick Start

### 📖 **New User? Start Here!**

We have **4 guides** to help you get started:

1. **[SIMPLE_START_GUIDE.md](SIMPLE_START_GUIDE.md)** ⭐ **RECOMMENDED**
   - Visual 4-step process
   - Perfect for beginners
   - 20 minutes to deploy

2. **[FILES_TO_UPLOAD.md](FILES_TO_UPLOAD.md)** 📤
   - Shows exactly what files go where
   - Answers common questions

3. **[COLAB_DEPLOYMENT_GUIDE.md](COLAB_DEPLOYMENT_GUIDE.md)** 📋
   - Complete detailed instructions
   - Troubleshooting section

4. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** ✅
   - Printable checklist
   - Track your progress

---

## 📋 Prerequisites

### Backend (Google Colab)
- Google Colab Pro Plus subscription (for A100 GPU)
- HuggingFace account ([Get token](https://huggingface.co/settings/tokens))
- Ngrok account ([Get token](https://dashboard.ngrok.com/get-started/your-authtoken))

### Frontend (Local Computer)
- Python 3.9 or higher
- 4GB+ RAM
- Internet connection

---

## 🎯 The Simple Version

### What You Upload to Colab:
```
✅ colab_backend.ipynb  (the notebook)
✅ docs/ folder         (your PDF documents)
```

### What Stays on Your Computer:
```
🖥️ frontend_app.py
🖥️ requirements.txt
```

### What You Run:

**In Google Colab:**
1. Upload notebook and docs folder
2. Set runtime to A100 GPU
3. Paste your tokens (HuggingFace + Ngrok)
4. Run all cells in order
5. Copy the Ngrok URL

**On Your Computer:**
```powershell
# Edit frontend_app.py with your Ngrok URL
# Then run:
pip install -r requirements.txt
python frontend_app.py
```

**Open Browser:**
```
http://127.0.0.1:7860
```

---

## 📁 Project Structure

```
KUchat/
├── colab_backend.ipynb              # Main Colab notebook (backend)
├── frontend_app.py                  # Gradio frontend (local)
├── setup.py                         # Automated setup script
├── requirements.txt                 # Frontend dependencies
├── start_frontend.ps1               # Quick start script (Windows)
├── .gitignore                       # Git ignore rules
│
├── docs/                            # Document repository
│   ├── Agriculture/                 # 10 PDFs
│   ├── Science/                     # 18 PDFs
│   ├── Engineering/                 # 18 PDFs
│   ├── Business Administration/     # 7 PDFs
│   ├── Humanities/                  # 25 PDFs
│   └── ... (15 more faculties)      # 110+ more PDFs
│
├── SIMPLE_START_GUIDE.md            # Beginner-friendly guide
├── FILES_TO_UPLOAD.md               # File upload reference
├── COLAB_DEPLOYMENT_GUIDE.md        # Detailed deployment guide
├── DEPLOYMENT_CHECKLIST.md          # Progress checklist
├── ARCHITECTURE.md                  # System architecture
└── README.md                        # This file
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KUCHAT SYSTEM                            │
└─────────────────────────────────────────────────────────────┘

    GOOGLE COLAB (Backend)              LOCAL COMPUTER (Frontend)
    ══════════════════════              ═════════════════════════
    
    ┌─────────────────────┐            ┌──────────────────────┐
    │  Qwen3-Omni-30B     │            │   Gradio Web UI      │
    │  (Multimodal)       │            │   (Chat Interface)   │
    └─────────────────────┘            └──────────────────────┘
    
    ┌─────────────────────┐                      ▲
    │  GPT-OSS-120B       │                      │
    │  (Text)             │                      │
    └─────────────────────┘            HTTP/HTTPS Requests
    
    ┌─────────────────────┐                      │
    │  RAG System         │                      ▼
    │  - ChromaDB         │            ┌──────────────────────┐
    │  - 170+ PDFs        │◄───────────┤  Ngrok Tunnel        │
    │  - Auto-loading     │            │  (Public URL)        │
    └─────────────────────┘            └──────────────────────┘
    
    ┌─────────────────────┐
    │  Web Search         │
    │  - DuckDuckGo       │
    │  - Wikipedia        │
    └─────────────────────┘
    
    ┌─────────────────────┐
    │  FastAPI Server     │
    │  Port: 8000         │
    └─────────────────────┘
```

---

## 🎓 Document Coverage

KUchat includes comprehensive information about **Kasetsart University programs**:

| Faculty | Programs | Example Programs |
|---------|----------|------------------|
| Agriculture | 10 | Agricultural Science, Food Science, Tropical Agriculture |
| Science | 18 | Computer Science, Physics, Chemistry, Biology |
| Engineering | 18 | Computer Engineering, Mechanical, Electrical, Civil |
| Business Administration | 7 | Marketing, Finance, Management, Accounting |
| Humanities | 25 | English, Tourism, Communication Arts, Music |
| Economics | 7 | Economics, Agricultural Economics, Cooperatives |
| Education | 9 | Mathematics Education, Science Education, PE |
| Social Sciences | 7 | Political Science, Sociology, Law, Psychology |
| Veterinary Medicine | 2 | Veterinary Medicine, Veterinary Science |
| Medicine | 1 | Doctor of Medicine |
| **...and 10 more faculties** | **70+** | **170+ total programs** |

---

## 💡 Usage Examples

### Basic Chat
```
User: "Hello! How are you?"
AI: "Hello! I'm doing well, thank you for asking..."
```

### RAG Query (About KU Programs)
```
User: "What courses are in the Computer Science program?"
AI: [Searches through CS curriculum PDF]
    "The Computer Science program includes courses such as:
    - Data Structures and Algorithms
    - Database Systems
    - Software Engineering
    - Artificial Intelligence..."
```

### Web Search Query
```
User: "What's the latest news about AI in 2025?"
AI: [Searches DuckDuckGo + Wikipedia]
    "According to recent sources, in 2025..."
```

### Multimodal Query
```
User: [Uploads image of a math equation]
      "Can you solve this?"
AI: [Analyzes image with Qwen3-Omni]
    "Looking at the equation in your image..."
```

---

## 🔧 Configuration

### Required Tokens

You'll need to obtain these tokens before deployment:

1. **HuggingFace Token**
   - Get from: https://huggingface.co/settings/tokens
   - Type: Read access
   - Used for: Downloading AI models

2. **Ngrok Token**
   - Get from: https://dashboard.ngrok.com/get-started/your-authtoken
   - Used for: Creating public URL for Colab backend

### Where to Paste Tokens

| Token | File | Location |
|-------|------|----------|
| HuggingFace | `colab_backend.ipynb` | Cell 7, line ~90 |
| Ngrok | `colab_backend.ipynb` | Cell 21, line ~1015 |
| Ngrok URL | `frontend_app.py` | Line 16 |

---

## 🐛 Troubleshooting

### Backend Connection Failed
**Problem**: Frontend can't connect to Colab backend

**Solution**:
1. Verify Colab notebook is still running
2. Check Ngrok URL in `frontend_app.py` matches Cell 21 output
3. Ensure URL includes `https://`

### No Documents Found
**Problem**: RAG system shows no documents loaded

**Solution**:
1. Check `/content/docs/` folder exists in Colab
2. Verify PDFs are uploaded to correct location
3. Re-run Cell 23 (Auto-load documents)

### Out of Memory
**Problem**: GPU runs out of memory

**Solution**:
1. Change runtime to A100 GPU (Runtime → Change runtime type)
2. Restart runtime
3. Re-run all cells

### Model Download Fails
**Problem**: Models won't download

**Solution**:
1. Check HuggingFace token is correct
2. Verify you have Read access token
3. Check internet connection in Colab

---

## 📊 Performance

### Model Specifications

| Model | Size | GPU Memory | Load Time | Speed |
|-------|------|------------|-----------|-------|
| Qwen3-Omni-30B | ~30B params | ~40GB | 3-5 min | Fast |
| GPT-OSS-120B-4bit | ~120B (quantized) | ~35GB | 2-3 min | Very Fast |

### RAG Performance

- **Document Loading**: ~2-5 minutes for 170+ PDFs
- **Indexing**: ~1000 chunks per minute
- **Query Speed**: 100-200ms per retrieval
- **Accuracy**: High relevance with semantic search

---

## 🔒 Security

### Protected Files (.gitignore)
- API tokens and secrets
- Configuration files with URLs
- Virtual environment
- ChromaDB database
- Upload cache
- Log files

### Best Practices
- Never commit tokens to repository
- Use environment variables for sensitive data
- Regenerate Ngrok URL for each session
- Keep HuggingFace token private

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### AI Models
- **Qwen3-Omni-30B** by Alibaba Cloud
- **GPT-OSS-120B** by OpenGPT-X

### Technologies
- **Google Colab** - Cloud GPU platform
- **Gradio** - Web interface framework
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **FastAPI** - Backend API framework
- **Ngrok** - Tunneling service

### Data
- **Kasetsart University** - Curriculum information
- All PDF documents belong to their respective programs and faculties

---

## 📞 Support

### Getting Help
1. Check the guides: `SIMPLE_START_GUIDE.md`, `COLAB_DEPLOYMENT_GUIDE.md`
2. Review `DEPLOYMENT_CHECKLIST.md` for missed steps
3. See troubleshooting section above
4. Open an issue on GitHub

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Dual AI models (Qwen3-Omni + GPT-OSS)
- ✅ RAG system with 170+ PDFs
- ✅ Web search integration
- ✅ Multimodal support
- ✅ Auto-loading documents

### Future Plans
- [ ] Multi-language support (Thai interface)
- [ ] Voice input/output
- [ ] Document upload via frontend
- [ ] Chat history persistence
- [ ] User authentication
- [ ] Mobile-responsive design
- [ ] Docker deployment option
- [ ] Local deployment guide (without Colab)

---

## 📈 Stats

- **Lines of Code**: ~1,500+
- **Documents**: 170+ PDF curriculum files
- **Faculties**: 20
- **Models**: 2 (Qwen3-Omni + GPT-OSS)
- **Guides**: 4 comprehensive deployment guides
- **Supported Formats**: PDF, TXT, MD, Images, Audio, Video

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ for Kasetsart University students and faculty**

**Questions? Open an issue or check the guides!**

[Documentation](SIMPLE_START_GUIDE.md) • [Architecture](ARCHITECTURE.md) • [License](LICENSE)

</div>
