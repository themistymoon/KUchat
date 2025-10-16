# KUchat - Kasetsart University AI Chatbot

An AI chatbot system powered by GPT-OSS-20B with advanced Retrieval-Augmented Generation capabilities. The system features a three-stage search pipeline combining semantic search, cross-encoder reranking, and keyword boosting for accurate responses about Kasetsart University academic programs.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Google%20Colab-orange.svg)](https://colab.research.google.com/)

---

## What's New (Version 2.1)

**Critical Bug Fixes**
- **Path Conversion Fix**: Resolved catalog metadata lookup failure caused by absolute/relative path mismatch
  - Issue: System used absolute Windows paths (`C:\Users\...\Medicine\...`) to lookup catalog entries stored with relative paths (`Medicine/...`)
  - Impact: All documents had `faculty='Unknown'`, preventing proper keyword boosting and retrieval
  - Solution: Convert absolute paths to relative paths before catalog lookup using `os.path.relpath()`
- **Expanded Faculty Mappings**: Increased faculty coverage from 10 to 20+ faculties for comprehensive keyword boosting
  - Added: Medicine (แพทยศาสตร์), Nursing (พยาบาลศาสตร์), Pharmacy (เภสัชศาสตร์), Veterinary Medicine (สัตวแพทยศาสตร์)
  - Added: Forestry (ป่าไม้), Fisheries (ประมง), Environment (สิ่งแวดล้อม), Agro-Industry (อุตสาหกรรมเกษตร)
  - Added: Architecture (สถาปัตยกรรม), Interdisciplinary Studies (บูรณาการศาสตร์), and more
  - Impact: Better keyword extraction and score boosting for previously missing faculties

**Enhanced Search System (Version 2.0)**
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

## Deployment

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
- **Gradio 4.0+**: Modern web-based chat interface with public URL sharing
- **Real-time Streaming**: Fast response generation with streaming output
- **Configurable Parameters**: Temperature (0.1-1.0), max tokens (128-2048), RAG toggle, web search toggle
- **System Log**: Real-time display of query processing stages and performance metrics
- **Chat History**: Persistent conversation history during session

---

## System Architecture

All-in-one system running on Google Colab:

### Single Integrated System (Google Colab)
- **GPT-OSS-20B Model**: Main language model on A100 GPU
- **RAG System**: Qdrant vector database with BGE-M3-Thai embeddings
- **Web Search System**: DuckDuckGo and Wikipedia integration
- **Gradio Interface**: Built-in web UI with public URL (share=True)
- **No separate frontend**: Everything runs in one notebook

```
┌─────────────────────────────────────────────────────────────┐
│              KUCHAT SYSTEM (Google Colab)                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Gradio Web Interface (Public URL)                          │
│         ↓                                                    │
│  Chat Processing Function                                   │
│         ↓                                                    │
│  ┌─────────────┬──────────────┬─────────────┐              │
│  │  RAG System │  GPT-OSS-20B │ Web Search  │              │
│  │  (Qdrant)   │   (A100)     │  (Optional) │              │
│  └─────────────┴──────────────┴─────────────┘              │
│                                                              │
│  All components run in single Colab notebook                │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

- Google Colab Pro Plus subscription (for A100 GPU access)
- HuggingFace account with access token ([Create token](https://huggingface.co/settings/tokens))
- Web browser to access the public Gradio URL

---

## Installation and Setup

### Step 1: Access the Notebook

1. **Open the Notebook**
   - Navigate to [Google Colab](https://colab.research.google.com/)
   - Go to File → Open Notebook → GitHub
   - Enter: `themistymoon/KUchat`
   - Select `colab_production_demo.ipynb`
   
   OR
   
   - Clone the repository and upload the notebook manually

2. **Configure Runtime**
   - Click Runtime → Change runtime type
   - Set Hardware accelerator to GPU
   - Set GPU type to **A100** (requires Colab Pro+)
   - Click Save

### Step 2: Configure and Run

1. **Configure HuggingFace Token**
   - In Cell 3 (Configuration), replace:
     ```python
     HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN_HERE"
     ```
   - Paste your HuggingFace token from https://huggingface.co/settings/tokens

2. **Run All Cells Sequentially**
   - Click Runtime → Run all
   - OR run cells one by one from top to bottom
   
   **Cell Execution Flow:**
   - Cell 1: Install dependencies (~3-5 minutes)
   - Cell 2: Import libraries and verify A100 GPU
   - Cell 3: Configuration (set your HuggingFace token here)
   - Cell 4: Download documentation from GitHub (~1-2 minutes)
   - Cell 5: Load GPT-OSS-20B model (~2-3 minutes, uses ~12GB VRAM)
   - Cell 6: Initialize RAG System
   - Cell 7: Load documents and create embeddings (~3-5 minutes, uses ~10GB VRAM)
   - Cell 8: Initialize web search system
   - Cell 9: Configure chat function
   - Cell 10: Launch Gradio interface with public URL

3. **Access the Chatbot**
   - After Cell 10 completes, a public Gradio URL will be displayed
   - Example: `https://xxxxxxxx.gradio.live`
   - Click the URL or copy and paste it into your browser
   - Share this URL with others to use the chatbot
   - The chatbot is now live and accessible from anywhere

---

## Project Structure

```
KUchat/
├── colab_production_demo.ipynb      # Main notebook (all-in-one system)
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
├── README.md                        # This documentation
├── ARCHITECTURE.md                  # System architecture documentation
│
└── docs/                            # Document repository (auto-downloaded)
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

1. Open the public Gradio URL in your browser
2. Type your question in the text input field
3. Click Send or press Enter
4. View AI response in chat history
5. Monitor system log for query processing details

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

### Configuration Options

Adjust settings in the right sidebar:
- **Temperature**: 0.1 (focused) to 1.0 (creative)
- **Max Tokens**: 128-2048 (response length)
- **Enable RAG**: Toggle document retrieval
- **Enable Web Search**: Toggle web search

---

## Configuration

### Required Token

| Token | Purpose | Obtain From | Configuration Location |
|-------|---------|-------------|----------------------|
| HuggingFace Token | Model downloads | [HuggingFace Settings](https://huggingface.co/settings/tokens) | `colab_production_demo.ipynb` Cell 3 |

### Model Parameters

Adjustable via Gradio interface:
- **Temperature**: Controls response randomness (0.1 - 1.0)
- **Max Tokens**: Maximum response length (128 - 2048)
- **RAG Toggle**: Enable/disable document retrieval
- **Web Search Toggle**: Enable/disable web search

---

## Troubleshooting

### Gradio URL Not Generated

**Symptom**: Cell 10 doesn't show a public URL

**Solutions**:
1. Verify all previous cells completed successfully
2. Check for error messages in cell outputs
3. Restart runtime and run all cells again
4. Ensure A100 GPU is allocated (check Cell 2 output)

### No Documents Found

**Symptom**: RAG system reports no documents loaded

**Solutions**:
1. Verify Cell 4 (GitHub download) completed successfully
2. Check `/content/docs/` folder exists in Colab file browser
3. Re-execute Cell 7 (Load documents)
4. Review Cell 7 output for file loading statistics

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

### Session Timeout

**Symptom**: Chatbot stops responding after some time

**Solutions**:
1. Colab sessions time out after ~12 hours of inactivity
2. Run Cell 10 again to restart Gradio interface
3. For longer sessions, interact with the notebook periodically

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

## System Specifications

| Aspect | Details |
|--------|---------|
| **Purpose** | Production AI Chatbot |
| **Model** | GPT-OSS-20B (Unsloth 4-bit) |
| **Hardware** | A100 GPU (Colab Pro+) |
| **VRAM Required** | ~22GB (12GB model + 10GB RAG) |
| **Setup Time** | 10-15 minutes |
| **Cost** | ~$50/month (Colab Pro+) |
| **RAG System** | Qdrant + BGE-M3-Thai + Reranking |
| **Catalogs** | Dual (Curricula + Gen Ed) |
| **Response Quality** | Excellent with context |
| **Speed** | 40-80 tokens/sec |
| **Search Pipeline** | Three-stage with reranking |
| **Interface** | Gradio with public URL |
| **Deployment** | All-in-one Colab notebook |

**Note**: This is a production-ready system. Simply run the notebook and share the generated Gradio URL.

---

## Technical Statistics

- **Deployment**: Single Colab notebook (all-in-one system)
- **Codebase**: ~1,300 lines of Python
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
- **Interface**: Gradio 4.0+ with public URL sharing (no separate frontend needed)

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
