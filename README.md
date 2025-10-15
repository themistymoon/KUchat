# KUchat - Kasetsart University AI Chatbot

A multi-modal AI chatbot system powered by dual large language models (Qwen3-Omni-30B and GPT-OSS-120B) with enhanced Retrieval-Augmented Generation capabilities. The system features hybrid search technology combining keyword matching with semantic search for fast and accurate responses about Kasetsart University academic programs.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Google%20Colab-orange.svg)](https://colab.research.google.com/)

---

## What's New (Version 2.0)

**Enhanced Search System**
- **Advanced RAG Pipeline**: Three-stage retrieval process with broad search, reranking, and post-filtering with keyword boosting
- **Dual-Catalog System**: Structured curriculum catalog (131 programs, 863 keywords) with integrated General Education catalog (204 courses)
- **Smart Context Assembly**: Automatic inclusion of General Education requirements for year-level and course queries
- **BGE-M3-Thai Embeddings**: Thai-optimized semantic search with 1024-dimensional vectors for superior accuracy
- **Qdrant Vector Database**: High-performance in-memory vector database with cosine similarity search
- **Cross-Encoder Reranking**: BGE-Reranker-v2-m3 for improved relevance scoring

**General Education Integration**
- Complete catalog of 204 General Education courses across 5 categories
- Automatic requirement calculation (30 total credits: 2 required + 28 elective minimum)
- Category-wise breakdown: Citizenship (21), Communication (76), Entrepreneurship (17), Aesthetics (16), Well-being (74)
- Smart query detection automatically appends General Education context to relevant queries

**Performance Improvements**
- Three-stage search strategy: Broad semantic search (50 candidates) followed by reranking and filtering
- Average keywords per program: 6.6 keywords for precise matching
- Enhanced Thai language support with normalized embeddings
- Related program suggestions based on shared keywords and faculty associations

---

## Deployment Options

### Test Version (Google Colab Free/T4)
For testing and development without costs:
- **Notebook**: `colab_backend_test.ipynb`
- **GPU**: T4 (15GB VRAM) - Available on Colab Free
- **Model**: Qwen2-7B-Instruct (7B parameters)
- **Speed**: 5-10 tokens/second
- **Cost**: Free
- **Purpose**: Test functionality before production deployment

### Production Version (Google Colab Pro+ A100)
For production use with best performance:
- **Notebook**: `colab_production_demo.ipynb`
- **GPU**: A100 (80GB VRAM) - Requires Colab Pro+
- **Model**: GPT-OSS-20B (4-bit quantized via Unsloth)
- **RAG System**: Qdrant + BGE-M3-Thai embeddings + BGE-Reranker-v2-m3
- **Catalogs**: Curricula (131 programs) + General Education (204 courses)
- **Search**: Three-stage pipeline with broad search, reranking, and boosting
- **Speed**: 40-80 tokens/second
- **VRAM Usage**: Approximately 22GB (12GB model + 10GB RAG)
- **Cost**: ~$1/hour
- **Purpose**: Production deployment with enterprise-grade RAG

---

## Features

### AI Model Architecture
**Test Version:**
- **Qwen2-7B-Instruct**: 7B parameter model with 4-bit quantization
- Fits on T4 GPU (15GB VRAM)
- Good quality for testing

**Production Version:**
- **GPT-OSS-20B**: High-performance text generation model with 20 billion parameters
- **4-bit Quantization**: Unsloth-optimized BitsAndBytes quantization for efficient memory usage
- **Expected VRAM**: Approximately 12GB for model, 10GB for RAG components, total ~22GB
- **Inference Speed**: 40-80 tokens per second with 2x faster performance vs FP16
- **Context Length**: 2048 tokens maximum sequence length
- **Optimization**: FastLanguageModel with automatic dtype detection

### Retrieval-Augmented Generation (RAG)
- **Dual-Catalog System**:
  - Primary Catalog: 131 curricula from 20 faculties with 863 keywords
  - General Education Catalog: 204 courses across 5 categories with detailed metadata
- **Advanced Search Pipeline**:
  1. Broad Semantic Search: Retrieve 50 initial candidates without pre-filtering
  2. Cross-Encoder Reranking: BGE-Reranker-v2-m3 for relevance scoring
  3. Post-Filter with Boosting: Keyword-based score enhancement and top-K selection
- **Vector Database**: Qdrant in-memory database with cosine similarity search
- **Embedding Model**: BGE-M3-Thai (1024 dimensions) optimized for Thai language
- **Smart Context Assembly**: Automatic General Education inclusion for year/course queries
- **Document Processing**: RecursiveCharacterTextSplitter with 1500-character chunks and 300-character overlap
- **Related Programs**: Automatic suggestions based on program IDs and keyword overlap

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

### For Test Version (Colab Free)
- Google account (free Colab access)
- HuggingFace account ([Create token](https://huggingface.co/settings/tokens))
- Ngrok account ([Get token](https://dashboard.ngrok.com/get-started/your-authtoken))
- Python 3.9+ for frontend

### For Production Version (Colab Pro+)
- Google Colab Pro Plus subscription (for A100 GPU access)
- HuggingFace account with access token
- Ngrok account with authentication token
- Python 3.9+ for frontend

---

## Installation and Setup

### Option 1: Test Version (Free - Recommended First)

**Perfect for testing before committing to Colab Pro+**

#### Step 1: Deploy Test Backend on Colab Free

1. Open **`colab_backend_test.ipynb`** in Google Colab
2. **Select T4 GPU**: Runtime → Change runtime type → **T4 GPU**
3. **Run all cells** in order:
   - Install dependencies
   - Load Qwen2-7B model (7B parameters)
   - Initialize RAG system
   - Start FastAPI server
   - Start Ngrok tunnel
4. **Copy the public URL** (e.g., `https://xxxx-xx-xx.ngrok.io`)

#### Step 2: Run Frontend on Local Computer

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Edit `frontend_app.py` and update the API URL:
   ```python
   API_URL = "https://your-ngrok-url-here"  # Paste the URL from Colab
   ```

3. Run the frontend:
   ```bash
   python frontend_app.py
   ```

4. Open browser to `http://localhost:7860`

**Test the chatbot** If everything works, you can upgrade to production.

---

### Option 2: Production Version (Colab Pro+)

For production deployment with enhanced hybrid search:

### Step 1: Clone Repository

```bash
git clone https://github.com/themistymoon/KUchat.git
cd KUchat
```

### Step 2: Backend Setup (Google Colab)

1. **Upload Notebook**
   - Navigate to [Google Colab](https://colab.research.google.com/)
   - Upload `colab_production_demo.ipynb` from this repository

2. **Configure Runtime**
   - Click Runtime → Change runtime type
   - Set Hardware accelerator to GPU
   - Set GPU type to A100
   - Click Save

3. **Download Documents**
   - Documents are automatically downloaded from GitHub repository via sparse checkout
   - The system downloads only the `docs` folder to minimize bandwidth usage
   - Required files include:
     - `curricula_catalog.json` (v2.0 format with 131 programs and 863 keywords)
     - `general_education_catalog.json` (204 General Education courses)
     - All curriculum PDF files organized by faculty folders (20 faculties)
   - Automatic document loading occurs in Cell 12 after RAG system initialization

4. **Configure Tokens**
   - In Cell 7: Replace `YOUR_HUGGINGFACE_TOKEN` with your HuggingFace token
   - In Cell 21: Replace `YOUR_NGROK_TOKEN` with your Ngrok authentication token

5. **Execute Cells**
   - Run cells sequentially from top to bottom
   - Wait for each cell to complete before proceeding
   - Cell 1: Install dependencies (~3-5 minutes)
   - Cell 2: Import libraries and verify GPU availability
   - Cell 3: Configure model settings and HuggingFace token
   - Cell 4: Download documentation from GitHub repository
   - Cell 5: Load GPT-OSS-20B Language Model (~2-3 minutes, ~12GB VRAM)
   - Cell 6: Initialize RAG System with three-stage search pipeline
   - Cell 7: Load curriculum documents and create vector embeddings (~3-5 minutes)
   - Cell 8: Initialize web search system (DuckDuckGo and Wikipedia)
   - Cell 9: Configure chat function with prompt engineering
   - Cell 10: Launch Gradio demo interface with public URL

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
├── colab_backend_test.ipynb         # Test backend (T4 GPU, Qwen2-7B-Instruct)
├── colab_production_demo.ipynb      # Production backend (A100 GPU, advanced RAG)
├── frontend_app.py                  # Gradio frontend application
├── convert_md_to_json.py            # Catalog enhancement script
├── setup.py                         # Automated setup script
├── requirements.txt                 # Python dependencies
├── start_frontend.ps1               # Windows PowerShell startup script
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
├── README.md                        # This documentation
├── ARCHITECTURE.md                  # System architecture documentation
├── PROGRESS_REPORT.md               # Development progress and improvements
├── IMPROVEMENT_OPPORTUNITIES.md     # Future enhancement roadmap
│
└── docs/                            # Document repository
    ├── curricula_catalog.json       # Primary catalog (v2.0, 131 programs, 863 keywords)
    ├── general_education_catalog.json # General Education catalog (204 courses, 5 categories)
    ├── docs_location.md             # Documentation index
    ├── Agriculture/                 # 10 curriculum PDFs
    ├── Science/                     # 18 curriculum PDFs (including Computer Science)
    ├── Engineering/                 # 18 curriculum PDFs
    ├── Business Administration/     # 7 curriculum PDFs
    ├── Humanities/                  # 25 curriculum PDFs
    ├── Economics/                   # 7 curriculum PDFs
    ├── Education/                   # 9 curriculum PDFs
    ├── Social Sciences/             # 8 curriculum PDFs
    ├── Veterinary Medicine/         # 2 curriculum PDFs
    ├── Medicine/                    # 1 curriculum PDF
    ├── GeneralEducation/            # General Education course data
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
| GPT-OSS-20B | 20 billion | ~12 GB | 2-3 minutes | 40-80 tokens/sec |
| RAG Components | N/A | ~10 GB | 3-5 minutes | N/A |
| Total System | N/A | ~22 GB | 5-8 minutes | 40-80 tokens/sec |

### RAG System Performance

- **Catalog Loading**: Version 2.0 format with curricula array structure, loads in <1 second
- **General Education Catalog**: 204 courses loaded instantly from JSON
- **Document Loading**: 3-5 minutes for 130+ PDFs with automatic sparse checkout from GitHub
- **Embedding Generation**: Batch processing (32 chunks per batch) with BGE-M3-Thai
- **Vector Database**: Qdrant in-memory with 1024-dimensional vectors
- **Search Pipeline**:
  - Stage 1: Broad semantic search retrieves 50 candidates (no pre-filtering)
  - Stage 2: Cross-encoder reranking for relevance scoring
  - Stage 3: Post-filtering with keyword boosting and top-5 selection
- **Query Processing**: Keyword extraction for year, semester, and program/major patterns
- **Context Assembly**: Smart auto-append of General Education for year/course queries
- **Chunk Configuration**: 1500 characters per chunk with 300-character overlap
- **Search Accuracy**: High relevance through three-stage refinement process

### System Requirements

**Production System (Google Colab)**:
- A100 GPU (80GB VRAM recommended, 40GB minimum)
- Google Colab Pro Plus subscription for A100 access
- Stable internet connection for model downloads and GitHub repository access
- Approximately 30GB storage for models and document cache

**Local Frontend**:
- Python 3.9 or higher
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection to communicate with Colab backend

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

**Version 2.0 (Current)**:
- Advanced three-stage RAG pipeline (broad search, reranking, post-filtering)
- Dual-catalog system with General Education integration (204 courses)
- BGE-M3-Thai embeddings with 1024-dimensional vectors
- Qdrant vector database for high-performance similarity search
- BGE-Reranker-v2-m3 cross-encoder for improved relevance
- Smart context assembly with automatic General Education appending
- Catalog v2.0 format with structured curricula array
- Enhanced Thai language support with normalized embeddings
- Related program suggestions based on keyword overlap

**Implemented Advanced Features**:
- Cross-encoder reranking (BGE-Reranker-v2-m3)
- Post-processing to remove English chain-of-thought from responses
- Comprehensive prompt engineering with few-shot examples
- Keyword boosting for better result ranking
- Fallback generation mode for error handling

**Planned Features (v2.1+)**:
- Query expansion with Thai synonyms and related terms
- Caching layer for frequently asked questions
- Analytics dashboard for usage tracking and query patterns
- Enhanced logging with structured output
- Thai language interface localization
- Voice input and output capabilities
- Persistent chat history with session management
- User authentication and personalization
- Mobile-responsive design improvements
- API rate limiting and quota management

---

## Deployment Options Comparison

| Aspect | Local Test Version | Full Production Version |
|--------|-------------------|-------------------------|
| **Purpose** | Testing & Development | Production Use |
| **Model** | Qwen2-7B-Instruct | GPT-OSS-20B (Unsloth 4-bit) |
| **Hardware** | T4 GPU (Colab Free) | A100 GPU (Colab Pro+) |
| **VRAM Required** | ~15GB | ~22GB (12GB model + 10GB RAG) |
| **Setup Time** | 5-10 minutes | 10-15 minutes |
| **Cost** | Free | ~$50/month (Colab Pro+) |
| **RAG System** | Basic ChromaDB | Advanced Qdrant + Reranking |
| **Catalogs** | Single catalog | Dual catalog (Curricula + Gen Ed) |
| **Response Quality** | Good for testing | Excellent with context |
| **Speed** | 5-10 tokens/sec | 40-80 tokens/sec |
| **Search Pipeline** | Two-stage | Three-stage with reranking |
| **Use Case** | Development, testing | Production, real users |

**Recommendation**: Start with local test version to verify everything works, then deploy to Colab for production use.

---

## Technical Statistics

- **Codebase**: ~1,500 lines of Python (production notebook)
- **Primary Catalog**: JSON v2.0 format with 131 curricula, 863 keywords, 20 faculties
- **General Education Catalog**: 204 courses across 5 categories with detailed metadata
- **Documents**: 130+ PDF curriculum files with automatic GitHub download
- **AI Model**: GPT-OSS-20B (20 billion parameters, 4-bit quantized)
- **Embedding Model**: BGE-M3-Thai (1024 dimensions, Thai-optimized)
- **Reranker**: BGE-Reranker-v2-m3 cross-encoder
- **Vector Database**: Qdrant in-memory with cosine similarity
- **Search Pipeline**: Three-stage (broad search, reranking, post-filtering with boosting)
- **Text Chunking**: 1500 characters per chunk, 300-character overlap
- **Batch Processing**: 32 chunks per batch for embedding generation
- **Supported Features**: RAG, web search (DuckDuckGo + Wikipedia), streaming responses
- **Interface**: Gradio 4.0+ with public URL via share=True

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
