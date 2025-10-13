# KUchat - Kasetsart University AI Chatbot

A multi-modal AI chatbot system powered by dual large language models (Qwen3-Omni-30B and GPT-OSS-120B) with Retrieval-Augmented Generation capabilities. The system is designed to answer questions about Kasetsart University academic programs and provide general knowledge assistance.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Google%20Colab-orange.svg)](https://colab.research.google.com/)

---

## Features

### Dual AI Model Architecture
- **Qwen3-Omni-30B-A3B-Instruct**: Multimodal model supporting text, images, audio, and video inputs
- **GPT-OSS-120B-Unsloth-BNB-4bit**: High-performance text generation model with 4-bit quantization
- Both models optimized for NVIDIA A100 GPU execution

### Retrieval-Augmented Generation (RAG)
- **Document Collection**: 170+ curriculum PDF files covering Kasetsart University programs
- **Faculty Coverage**: 20 faculties including Agriculture, Engineering, Science, Business, and more
- **Vector Database**: ChromaDB for efficient semantic search and retrieval
- **Auto-loading**: Automatic document indexing at system startup
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 for document vectorization

### Web Search Integration
- **DuckDuckGo Search**: Real-time web search capabilities
- **Wikipedia Integration**: Encyclopedia knowledge retrieval
- **Bilingual Support**: Thai and English language search

### User Interface
- **Gradio 4.0+**: Modern web-based chat interface
- **Multimodal Upload**: Support for images, audio, and video files
- **Real-time Streaming**: Fast response generation with streaming output
- **Configurable Parameters**: Temperature, max tokens, RAG toggle, web search toggle

---

## System Architecture

The system consists of two main components:

### Backend (Google Colab)
- Hosts both AI models on A100 GPU
- Runs FastAPI server for API endpoints
- Manages RAG system and document retrieval
- Handles web search integration
- Provides public access via Ngrok tunnel

### Frontend (Local Computer)
- Gradio web interface for user interaction
- Connects to backend via HTTPS
- Handles file uploads and multimodal inputs
- Manages chat history and UI state

```
┌─────────────────────────────────────────────────────────────┐
│                    KUCHAT SYSTEM                            │
└─────────────────────────────────────────────────────────────┘

    GOOGLE COLAB (Backend)              LOCAL COMPUTER (Frontend)
    ══════════════════════              ═════════════════════════
    
    - Qwen3-Omni-30B Model              - Gradio Web Interface
    - GPT-OSS-120B Model                - HTTP Client
    - RAG System (ChromaDB)             - File Upload Handlers
    - Web Search System                 - Chat UI Management
    - FastAPI Server (Port 8000)
    - Ngrok Public Tunnel               
                   │                              │
                   └──── HTTPS Connection ────────┘
```

---

## Prerequisites

### Backend Requirements (Google Colab)
- Google Colab Pro Plus subscription (required for A100 GPU access)
- HuggingFace account with access token ([Create token](https://huggingface.co/settings/tokens))
- Ngrok account with authentication token ([Get token](https://dashboard.ngrok.com/get-started/your-authtoken))

### Frontend Requirements (Local Computer)
- Python 3.9 or higher
- 4GB+ RAM
- Stable internet connection

---

## Installation and Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/themistymoon/KUchat.git
cd KUchat
```

### Step 2: Backend Setup (Google Colab)

1. **Upload Notebook**
   - Navigate to [Google Colab](https://colab.research.google.com/)
   - Upload `colab_backend.ipynb` from this repository

2. **Configure Runtime**
   - Click Runtime → Change runtime type
   - Set Hardware accelerator to GPU
   - Set GPU type to A100
   - Click Save

3. **Upload Documents**
   - In Colab's file browser (left sidebar), create folder `/content/docs/`
   - Upload the entire `docs` folder from this repository
   - Ensure folder structure is preserved with all faculty subfolders

4. **Configure Tokens**
   - In Cell 7: Replace `YOUR_HUGGINGFACE_TOKEN` with your HuggingFace token
   - In Cell 21: Replace `YOUR_NGROK_TOKEN` with your Ngrok authentication token

5. **Execute Cells**
   - Run cells sequentially from top to bottom
   - Wait for each cell to complete before proceeding
   - Cell 3: Install dependencies (~5 minutes)
   - Cell 7: Verify GPU and configure HuggingFace
   - Cell 9: Load Qwen model (~3-5 minutes)
   - Cell 12: Load GPT model (~2-3 minutes)
   - Cell 15: Initialize RAG system
   - Cell 17: Start FastAPI server
   - Cell 21: Create Ngrok tunnel and obtain public URL
   - Cell 23: Auto-load documents (~2-5 minutes)
   - Cell 24: Initialize web search system

6. **Copy Ngrok URL**
   - After Cell 21 completes, copy the PUBLIC URL displayed
   - Example format: `https://xxxx-xx-xx-xx-xx.ngrok-free.app`

### Step 3: Frontend Setup (Local Computer)

1. **Install Dependencies**

```bash
cd KUchat
pip install -r requirements.txt
```

2. **Configure API Endpoint**
   - Open `frontend_app.py` in a text editor
   - Locate line 16: `API_URL = "YOUR_NGROK_URL_HERE"`
   - Replace with your Ngrok URL from Step 2.6
   - Save the file

3. **Run Frontend Application**

```bash
python frontend_app.py
```

4. **Access Web Interface**
   - Open web browser
   - Navigate to `http://127.0.0.1:7860`
   - The chat interface should load successfully

---

## Project Structure

```
KUchat/
├── colab_backend.ipynb              # Google Colab notebook (backend server)
├── frontend_app.py                  # Gradio frontend application
├── setup.py                         # Automated setup script
├── requirements.txt                 # Python dependencies for frontend
├── start_frontend.ps1               # Windows PowerShell startup script
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
├── README.md                        # This documentation
├── ARCHITECTURE.md                  # System architecture documentation
│
└── docs/                            # Document repository (170+ PDFs)
    ├── Agriculture/                 # 10 curriculum PDFs
    ├── Science/                     # 18 curriculum PDFs
    ├── Engineering/                 # 18 curriculum PDFs
    ├── Business Administration/     # 7 curriculum PDFs
    ├── Humanities/                  # 25 curriculum PDFs
    ├── Economics/                   # 7 curriculum PDFs
    ├── Education/                   # 9 curriculum PDFs
    ├── Social Sciences/             # 8 curriculum PDFs
    ├── Veterinary Medicine/         # 2 curriculum PDFs
    ├── Medicine/                    # 1 curriculum PDF
    └── ... (10 additional faculties)
```

---

## Document Coverage

The system includes comprehensive curriculum information for Kasetsart University:

| Faculty | Programs | Example Disciplines |
|---------|----------|---------------------|
| Agriculture | 10 | Agricultural Science, Food Science, Animal Science |
| Science | 18 | Computer Science, Physics, Chemistry, Mathematics |
| Engineering | 18 | Computer, Mechanical, Electrical, Civil Engineering |
| Business Administration | 7 | Marketing, Finance, Management, Accounting |
| Humanities | 25 | English, Tourism, Communication Arts, Languages |
| Economics | 7 | Economics, Agricultural Economics, Cooperatives |
| Education | 9 | Mathematics, Science, Physical Education |
| Social Sciences | 8 | Political Science, Psychology, Sociology, Law |
| Veterinary Medicine | 2 | Veterinary Medicine, Veterinary Science |
| Medicine | 1 | Doctor of Medicine |
| Pharmacy | 1 | Pharmacy |
| Nursing | 1 | Nursing |
| Forestry | 4 | Forestry, Wood Science, Pulp and Paper Technology |
| Fisheries | 1 | Fisheries |
| Veterinary Technology | 2 | Veterinary Technology, Animal Nursing |
| Environment | 3 | Environmental Science and Technology |
| Architecture | 4 | Architecture, Landscape Architecture |
| Agro-Industry | 8 | Food Engineering, Biotechnology, Textiles |
| Interdisciplinary Studies | 2 | Tourism Management, Service Industry |
| College of Interdisciplinary Studies | 1 | Land Science for Sustainable Development |

**Total**: 20 faculties, 170+ academic programs

---

## Usage

### Basic Text Interaction

1. Select model (Qwen3-Omni or GPT-OSS-120B)
2. Type message in the text input field
3. Click Send or press Enter
4. View AI response in chat history

### Document Retrieval (RAG)

1. Enable "Enable RAG" checkbox
2. Ask questions about Kasetsart University programs
3. System retrieves relevant information from curriculum PDFs
4. Response includes context from documents

Example query:
```
User: "What courses are required for the Computer Science program?"
System: [Retrieves CS curriculum PDF] → Provides course list
```

### Web Search

1. Enable "Enable Web Search" checkbox
2. Ask questions requiring current information
3. System searches DuckDuckGo and Wikipedia
4. Response includes web search results

Example query:
```
User: "What are the latest developments in artificial intelligence?"
System: [Searches web] → Provides current information
```

### Multimodal Input

1. Click "Upload Image" or "Upload Audio" button
2. Select file from local system
3. Optionally add text query
4. Click Send
5. Qwen3-Omni model processes multimodal input

Supported formats:
- Images: JPG, PNG, BMP, GIF
- Audio: MP3, WAV, M4A
- Video: MP4, AVI, MOV

---

## Configuration

### API Tokens

| Token | Purpose | Obtain From | Configuration Location |
|-------|---------|-------------|----------------------|
| HuggingFace Token | Model downloads | [HuggingFace Settings](https://huggingface.co/settings/tokens) | `colab_backend.ipynb` Cell 7 |
| Ngrok Token | Public tunnel | [Ngrok Dashboard](https://dashboard.ngrok.com/get-started/your-authtoken) | `colab_backend.ipynb` Cell 21 |
| Ngrok URL | Frontend connection | Generated by Cell 21 | `frontend_app.py` Line 16 |

### Model Parameters

Adjustable via frontend interface:
- **Temperature**: Controls response randomness (0.1 - 2.0)
- **Max Tokens**: Maximum response length (256 - 4096)
- **RAG Toggle**: Enable/disable document retrieval
- **Web Search Toggle**: Enable/disable web search

---

## Troubleshooting

### Backend Connection Failed

**Symptom**: Frontend cannot connect to backend

**Solutions**:
1. Verify Colab notebook is running (check Cell 17 status)
2. Confirm Ngrok URL in `frontend_app.py` matches Cell 21 output
3. Ensure URL includes `https://` protocol
4. Check Colab session has not timed out

### No Documents Found

**Symptom**: RAG system reports no documents loaded

**Solutions**:
1. Verify `/content/docs/` folder exists in Colab file browser
2. Check PDFs are uploaded with correct folder structure
3. Re-execute Cell 23 (Auto-load documents)
4. Review Cell 23 output for file loading statistics

### GPU Memory Error

**Symptom**: Out of memory error during model loading

**Solutions**:
1. Confirm runtime is set to A100 GPU (not T4 or other GPUs)
2. Restart Colab runtime (Runtime → Restart runtime)
3. Re-execute all cells in sequence
4. Close other GPU-intensive processes

### Model Download Failure

**Symptom**: Models fail to download from HuggingFace

**Solutions**:
1. Verify HuggingFace token is correct and active
2. Confirm token has "Read" access permissions
3. Check Colab internet connectivity
4. Retry cell execution after brief wait

### Frontend Installation Issues

**Symptom**: `pip install` fails or packages missing

**Solutions**:
1. Upgrade pip: `python -m pip install --upgrade pip`
2. Install packages individually if batch install fails
3. Verify Python version is 3.9 or higher
4. Use virtual environment to avoid conflicts

---

## Performance Specifications

### Model Performance

| Model | Parameters | GPU Memory | Load Time | Inference Speed |
|-------|-----------|------------|-----------|-----------------|
| Qwen3-Omni-30B | ~30 billion | ~40 GB | 3-5 minutes | Fast |
| GPT-OSS-120B-4bit | ~120 billion (quantized) | ~35 GB | 2-3 minutes | Very Fast |

### RAG System Performance

- **Document Loading**: 2-5 minutes for 170+ PDFs
- **Indexing Rate**: ~1000 text chunks per minute
- **Retrieval Speed**: 100-200 milliseconds per query
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Chunk Size**: 1000 characters with 200 character overlap

### System Requirements

**Minimum**:
- A100 GPU (40GB VRAM minimum)
- 32GB System RAM
- 50GB Storage (for models and documents)
- 10 Mbps internet connection

**Recommended**:
- A100 GPU (80GB VRAM)
- 64GB System RAM
- 100GB Storage
- 50 Mbps internet connection

---

## Security Considerations

### Protected Information

The `.gitignore` file protects:
- API tokens and authentication credentials
- Configuration files containing URLs
- Virtual environment directories
- Vector database files
- Temporary upload cache
- Log files

### Best Practices

1. Never commit tokens or secrets to version control
2. Regenerate Ngrok URL for each session
3. Use environment variables for sensitive configuration
4. Keep HuggingFace token private
5. Regularly rotate authentication tokens
6. Review `.gitignore` before committing changes

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete terms and conditions.

---

## Acknowledgments

### AI Models

- **Qwen3-Omni-30B-A3B-Instruct** developed by Alibaba Cloud
- **GPT-OSS-120B-Unsloth-BNB-4bit** developed by OpenGPT-X consortium

### Technology Stack

- **Google Colab** - Cloud GPU computing platform
- **Gradio** - Web interface framework
- **LangChain** - RAG orchestration framework
- **ChromaDB** - Vector database
- **FastAPI** - Backend API framework
- **Ngrok** - Secure tunneling service
- **HuggingFace Transformers** - Model loading and inference
- **PyTorch** - Deep learning framework

### Data Sources

- **Kasetsart University** - Curriculum documentation and program information
- All PDF documents are property of their respective academic programs and faculties

---

## Support and Contributing

### Getting Help

1. Review this README for setup instructions
2. Check the [ARCHITECTURE.md](ARCHITECTURE.md) file for system details
3. Examine troubleshooting section above
4. Open an issue on GitHub for unresolved problems

### Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

### Development Roadmap

**Current Version (v1.0)**:
- Dual AI model support
- RAG system with 170+ documents
- Web search integration
- Multimodal capabilities
- Auto-loading document system

**Planned Features**:
- Thai language interface localization
- Voice input and output capabilities
- Frontend document upload functionality
- Persistent chat history storage
- User authentication system
- Mobile-responsive design improvements
- Docker containerization
- Self-hosted deployment documentation

---

## Technical Statistics

- **Codebase**: ~1,500 lines of Python
- **Documents**: 170+ PDF curriculum files
- **Faculties Covered**: 20 academic faculties
- **AI Models**: 2 large language models
- **Supported Input Formats**: Text, PDF, Images (JPG/PNG), Audio (MP3/WAV), Video (MP4)
- **API Endpoints**: 8 FastAPI routes
- **Vector Database**: ChromaDB with ~15,000+ text chunks

---

## Citation

If you use this system in academic work, please cite:

```
KUchat: A Multi-Modal AI Chatbot with RAG for Kasetsart University
Repository: https://github.com/themistymoon/KUchat
Year: 2025
```

---

## Contact

For questions, issues, or collaboration inquiries:
- Open an issue on GitHub
- Submit a pull request for contributions
- Review existing documentation before requesting support

---

**Built for Kasetsart University students and faculty**

[Documentation](README.md) • [Architecture](ARCHITECTURE.md) • [License](LICENSE)
