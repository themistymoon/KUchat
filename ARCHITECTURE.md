# System Architecture Documentation (Version 2.0)

## System Overview

KUchat is an AI-powered chatbot system for Kasetsart University curriculum information, featuring an advanced three-stage retrieval pipeline with dual-catalog support.

**Core Components**:
- **Language Model**: GPT-OSS-20B (4-bit quantized via Unsloth)
- **Deployment Platform**: Google Colab with A100 GPU
- **Interface**: Gradio 4.0+ with public URL sharing
- **RAG System**: Advanced three-stage retrieval pipeline
- **Vector Database**: Qdrant in-memory with cosine similarity
- **Embedding Model**: BGE-M3-Thai (1024 dimensions, Thai-optimized)
- **Reranker**: BGE-Reranker-v2-m3 cross-encoder
- **Dual-Catalog System**: 
  - Primary: 131 curricula, 20 faculties, 863 keywords
  - Secondary: 204 General Education courses, 5 categories

---

## Overall System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                               │
│           (Web Browser via Public Gradio URL)                     │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│          GOOGLE COLAB BACKEND (A100 GPU - 80GB VRAM)             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          GRADIO INTERFACE (Port 7860)                      │ │
│  │                                                            │ │
│  │  User Controls:                                           │ │
│  │  • Chat Input (text box)                                  │ │
│  │  • Temperature Slider (0.1-1.0)                           │ │
│  │  • Max Tokens Slider (128-2048)                           │ │
│  │  • Enable RAG (checkbox)                                  │ │
│  │  • Enable Web Search (checkbox)                           │ │
│  │  • System Log Display                                     │ │
│  │  • Chat History                                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                         │                                         │
│                         ▼                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          CHAT PROCESSING FUNCTION                          │ │
│  │                                                            │ │
│  │  1. Query Analysis                                        │ │
│  │  2. RAG Retrieval (if enabled)                            │ │
│  │  3. Web Search (if enabled)                               │ │
│  │  4. Context Assembly                                      │ │
│  │  5. Prompt Construction                                   │ │
│  │  6. Model Inference                                       │ │
│  │  7. Post-Processing                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                         │                                         │
│         ┌───────────────┼───────────────┐                        │
│         │               │               │                        │
│         ▼               ▼               ▼                        │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐               │
│  │   RAG    │   │   LLM    │   │ Web Search   │               │
│  │  System  │   │  Model   │   │   System     │               │
│  └──────────┘   └──────────┘   └──────────────┘               │
└──────────────────────────────────────────────────────────────────┘
```

---

## RAG System Architecture (Three-Stage Pipeline)

```
┌──────────────────────────────────────────────────────────────────┐
│                    RAG SYSTEM COMPONENTS                          │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  STAGE 0: CATALOG LOADING                                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  curricula_catalog.json (v2.0)                                   │
│  ┌────────────────────────────────────────────┐                 │
│  │  {                                          │                 │
│  │    "version": "2.0",                        │                 │
│  │    "total_programs": 131,                   │                 │
│  │    "total_faculties": 20,                   │                 │
│  │    "total_keywords": 863,                   │                 │
│  │    "curricula": [                           │                 │
│  │      {                                      │                 │
│  │        "id": "SCI-001",                     │                 │
│  │        "faculty": "คณะวิทยาศาสตร์",         │                 │
│  │        "program": "วท.บ. วิทยาการคอมพิวเตอร์", │             │
│  │        "file_path": "Science/...",          │                 │
│  │        "keywords": ["computer", "cs", ...] │                 │
│  │      },                                     │                 │
│  │      ...                                    │                 │
│  │    ]                                        │                 │
│  │  }                                          │                 │
│  └────────────────────────────────────────────┘                 │
│                                                                   │
│  general_education_catalog.json                                  │
│  ┌────────────────────────────────────────────┐                 │
│  │  {                                          │                 │
│  │    "total_courses": 204,                    │                 │
│  │    "total_categories": 5,                   │                 │
│  │    "required_courses": [...],               │                 │
│  │    "categories": [                          │                 │
│  │      {                                      │                 │
│  │        "category_id": "citizenship",        │                 │
│  │        "category_th": "พลเมืองไทยและโลก",    │                 │
│  │        "courses": [...],                    │                 │
│  │        "total_courses": 21                  │                 │
│  │      },                                     │                 │
│  │      ...                                    │                 │
│  │    ]                                        │                 │
│  │  }                                          │                 │
│  └────────────────────────────────────────────┘                 │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  STAGE 1: DOCUMENT PROCESSING                                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  GitHub Repository                                                │
│       ↓ (Sparse Checkout - docs folder only)                    │
│  Download docs/                                                   │
│       ↓                                                           │
│  PDF Files (130+ curricula)                                      │
│       ↓                                                           │
│  PyPDFLoader                                                      │
│       ↓                                                           │
│  Text Extraction                                                  │
│       ↓                                                           │
│  RecursiveCharacterTextSplitter                                  │
│    • Chunk Size: 1500 characters                                 │
│    • Overlap: 300 characters                                     │
│       ↓                                                           │
│  Text Chunks (with metadata)                                     │
│    • file_path, file_name, chunk_index                           │
│    • program, faculty, degree, id, keywords                      │
│       ↓                                                           │
│  BGE-M3-Thai Embedding Model                                     │
│    • Batch Size: 32 chunks                                       │
│    • Normalize: True                                             │
│    • Dimensions: 1024                                            │
│       ↓                                                           │
│  Vector Embeddings (1024d)                                       │
│       ↓                                                           │
│  Qdrant Vector Database                                          │
│    • Collection: "ku_curricula"                                  │
│    • Distance: Cosine                                            │
│    • Storage: In-memory                                          │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  STAGE 2: QUERY PROCESSING (Three-Stage Retrieval)              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User Query                                                       │
│       ↓                                                           │
│  ┌─────────────────────────────────────────┐                    │
│  │  SUBSTAGE 1: KEYWORD EXTRACTION         │                    │
│  │  • Extract year patterns (ปี 1-4)       │                    │
│  │  • Extract semester (ภาค 1-2, ฤดูร้อน)  │                    │
│  │  • Extract program/major synonyms       │                    │
│  │  • Build keyword list for BOOSTING      │                    │
│  └─────────────────────────────────────────┘                    │
│       ↓                                                           │
│  ┌─────────────────────────────────────────┐                    │
│  │  SUBSTAGE 2: BROAD SEMANTIC SEARCH      │                    │
│  │  • Generate query embedding (1024d)     │                    │
│  │  • NO pre-filtering applied             │                    │
│  │  • Search ALL programs in Qdrant        │                    │
│  │  • Retrieve top 50 candidates           │                    │
│  │  • Cosine similarity scoring            │                    │
│  └─────────────────────────────────────────┘                    │
│       ↓                                                           │
│  50 Candidates with semantic scores                              │
│       ↓                                                           │
│  ┌─────────────────────────────────────────┐                    │
│  │  SUBSTAGE 3: CROSS-ENCODER RERANKING    │                    │
│  │  • Model: BGE-Reranker-v2-m3            │                    │
│  │  • Create query-document pairs          │                    │
│  │  • Predict relevance scores             │                    │
│  │  • Sort by reranking scores             │                    │
│  └─────────────────────────────────────────┘                    │
│       ↓                                                           │
│  50 Reranked Candidates                                          │
│       ↓                                                           │
│  ┌─────────────────────────────────────────┐                    │
│  │  SUBSTAGE 4: POST-FILTER + BOOST        │                    │
│  │  • Keyword matching in text (+0.1)      │                    │
│  │  • Program name match (+0.2)            │                    │
│  │  • Faculty name match (+0.1)            │                    │
│  │  • Calculate final scores               │                    │
│  │  • Select top 5 results                 │                    │
│  └─────────────────────────────────────────┘                    │
│       ↓                                                           │
│  Top 5 Results with boosted scores                               │
│       ↓                                                           │
│  ┌─────────────────────────────────────────┐                    │
│  │  SUBSTAGE 5: CONTEXT ASSEMBLY           │                    │
│  │  • Build result texts with metadata     │                    │
│  │  • Track source files                   │                    │
│  │  • Add related program suggestions      │                    │
│  │  • Auto-append Gen Ed (if applicable)   │                    │
│  │  • Join with separator                  │                    │
│  └─────────────────────────────────────────┘                    │
│       ↓                                                           │
│  Final Context String + Source Metadata                          │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  GENERAL EDUCATION AUTO-APPEND LOGIC                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Query Pattern Detection:                                         │
│  • Regex: (ปี\s*\d+|รายวิชา|เรียนอะไร|วิชาเลือก|ศึกษาทั่วไป)      │
│       ↓                                                           │
│  IF pattern matches AND gened_catalog exists:                    │
│       ↓                                                           │
│  Build Gen Ed Context:                                           │
│  ┌────────────────────────────────────────┐                     │
│  │  [วิชาศึกษาทั่วไป - General Education]│                     │
│  │  รวม 30 หน่วยกิต                       │                     │
│  │                                         │                     │
│  │  **วิชาบังคับ:**                        │                     │
│  │  - 01999111 ศาสตร์แห่งแผ่นดิน (2)      │                     │
│  │                                         │                     │
│  │  **วิชาเลือก:**                         │                     │
│  │  • พลเมืองไทยและโลก (ขั้นต่ำ 3)        │                     │
│  │    Sample courses...                    │                     │
│  │  • ภาษากับการสื่อสาร (ขั้นต่ำ 12)      │                     │
│  │    Sample courses...                    │                     │
│  │  • ศาสตร์แห่งผู้ประกอบการ (ขั้นต่ำ 3)  │                     │
│  │  • สุนทรียศาสตร์ (ขั้นต่ำ 3)           │                     │
│  │  • อยู่ดีมีสุข (ขั้นต่ำ 7)             │                     │
│  └────────────────────────────────────────┘                     │
│       ↓                                                           │
│  Append to result_texts                                          │
│  Add to source_files_metadata                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Language Model Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  GPT-OSS-20B MODEL (UNSLOTH 4-BIT QUANTIZATION)                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Model Configuration:                                             │
│  • Name: unsloth/gpt-oss-20b-unsloth-bnb-4bit                    │
│  • Parameters: 20 billion (4-bit quantized)                      │
│  • Framework: Unsloth FastLanguageModel                          │
│  • Quantization: BitsAndBytes 4-bit                              │
│  • Maximum Sequence Length: 2048 tokens                          │
│  • VRAM Usage: ~12GB                                             │
│  • Inference Speed: 40-80 tokens/second                          │
│                                                                   │
│  Loading Process:                                                 │
│  1. Import unsloth and FastLanguageModel                         │
│  2. Load pre-quantized model from HuggingFace                    │
│  3. Optimize for inference (disable training)                    │
│  4. Move to A100 GPU                                             │
│                                                                   │
│  Inference Pipeline:                                              │
│  ┌────────────────────────────────────────┐                     │
│  │  Input: Context + Query                 │                     │
│  │       ↓                                  │                     │
│  │  Prompt Construction:                    │                     │
│  │    • System instruction                  │                     │
│  │    • Few-shot examples                   │                     │
│  │    • Conversation history (last 3)       │                     │
│  │    • User query                          │                     │
│  │    • Retrieved context (from RAG)        │                     │
│  │       ↓                                  │                     │
│  │  Tokenization                            │                     │
│  │       ↓                                  │                     │
│  │  Model.generate():                       │                     │
│  │    • max_new_tokens: user-configurable   │                     │
│  │    • temperature: user-configurable      │                     │
│  │    • do_sample: True                     │                     │
│  │    • top_p: 0.9                          │                     │
│  │    • top_k: 50                           │                     │
│  │    • use_cache: True                     │                     │
│  │       ↓                                  │                     │
│  │  Decoding                                │                     │
│  │       ↓                                  │                     │
│  │  Post-Processing:                        │                     │
│  │    • Remove model control tokens         │                     │
│  │    • Remove English thinking patterns    │                     │
│  │    • Line-by-line filtering              │                     │
│  │    • Remove leading junk                 │                     │
│  │       ↓                                  │                     │
│  │  Output: Thai response text              │                     │
│  └────────────────────────────────────────┘                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Request Flow Diagram

```
User Query
    ↓
[Gradio Chat Input]
    ↓
chat_with_bot(message, history, use_rag, use_web_search, temp, max_tokens)
    ↓
    ┌─────────────────────────────────────┐
    │  Context Building                    │
    │                                      │
    │  IF use_rag:                         │
    │    context += rag_system.query()     │
    │      ↓                               │
    │      • Stage 1: Broad search (50)    │
    │      • Stage 2: Reranking            │
    │      • Stage 3: Filter + boost (5)   │
    │      • Auto-append Gen Ed            │
    │      • Return context + sources      │
    │                                      │
    │  IF use_web_search:                  │
    │    context += web_search.search()    │
    │      ↓                               │
    │      • DuckDuckGo search             │
    │      • Wikipedia search              │
    │                                      │
    └─────────────────────────────────────┘
    ↓
[Prompt Construction]
    • System instruction (rules + examples)
    • Conversation history (last 3)
    • User query
    • Retrieved context
    ↓
[Tokenization]
    ↓
[GPT-OSS-20B Model Inference]
    • Generate with configured parameters
    • Fallback mode on error
    ↓
[Decoding]
    ↓
[Post-Processing]
    • Extract answer
    • Remove English thinking
    • Clean formatting
    ↓
[Response + Log]
    • Answer text
    • System log (timing, sources, etc.)
    ↓
[Update Gradio Interface]
    • Chat history
    • System log display
```

---

## Data Flow

### Document Loading Flow

```
Start System
    ↓
Cell 4: Download docs from GitHub (sparse checkout)
    ↓
docs/ folder created in /content/
    ├── curricula_catalog.json (131 programs)
    ├── general_education_catalog.json (204 courses)
    └── 20 faculty folders with PDF files
    ↓
Cell 6: Initialize RAG System
    • Create RAGSystem object
    • Load Thai keyword patterns
    • Load faculty/major mappings
    ↓
Cell 7: Load Documents
    ↓
    ┌──────────────────────────┐
    │  load_catalog()          │
    │  • Read JSON files       │
    │  • Parse v2.0 format     │
    │  • Build file_path map   │
    └──────────────────────────┘
    ↓
    ┌──────────────────────────┐
    │  load_models()           │
    │  • Load BGE-M3-Thai      │
    │  • Load BGE-Reranker     │
    │  • Init Qdrant client    │
    └──────────────────────────┘
    ↓
    ┌──────────────────────────┐
    │  load_documents()        │
    │  • Find PDF files        │
    │  • Extract text          │
    │  • Split into chunks     │
    │  • Generate embeddings   │
    │  • Upload to Qdrant      │
    └──────────────────────────┘
    ↓
System Ready
```

### Query Processing Flow

```
User submits query
    ↓
Extract keywords
    • Year patterns (ปี 1-4)
    • Semester patterns (ภาค 1-2)
    • Program/major synonyms
    ↓
Generate query embedding (BGE-M3-Thai)
    ↓
Broad semantic search (Qdrant)
    • NO filtering
    • Retrieve 50 candidates
    • Cosine similarity
    ↓
Cross-encoder reranking (BGE-Reranker-v2-m3)
    • Create query-doc pairs
    • Predict relevance scores
    • Sort by scores
    ↓
Post-filter with keyword boosting
    • Text keyword match: +0.1 per keyword
    • Program match: +0.2
    • Faculty match: +0.1
    • Calculate final scores
    • Select top 5
    ↓
Build context
    • Format result texts with metadata
    • Track source files
    • Add related program suggestions
    • Auto-append Gen Ed (if pattern matches)
    ↓
Return context + source metadata
```

---

## Key Features

### Dual-Catalog System

**Primary Catalog (curricula_catalog.json v2.0)**:
- 131 academic programs
- 20 faculties
- 863 keywords (Thai and English)
- Structured with curricula array format
- Metadata: id, faculty, program, degree, file_path, keywords

**Secondary Catalog (general_education_catalog.json)**:
- 204 General Education courses
- 5 categories with descriptions
- Credit requirements (30 total: 2 required + 28 elective minimum)
- Required course: 01999111 ศาสตร์แห่งแผ่นดิน
- Auto-append logic for year/course queries

### Three-Stage Search Pipeline

**Stage 1: Broad Semantic Search**
- Retrieve 50 candidates without pre-filtering
- Cast wide net to avoid missing relevant documents
- Uses Qdrant cosine similarity search
- Query embedding: BGE-M3-Thai (1024d)

**Stage 2: Cross-Encoder Reranking**
- Model: BGE-Reranker-v2-m3
- Creates query-document pairs
- Predicts relevance scores
- Sorts candidates by reranking scores
- More accurate than embedding similarity alone

**Stage 3: Post-Filter with Boosting**
- Keyword matching in chunk text
- Program name matching
- Faculty name matching
- Cumulative score boosting
- Select top 5 final results

### Smart Context Assembly

**Source Tracking**:
- Track unique source files
- Build source metadata list
- Include file name, program, faculty

**Related Programs**:
- Identify programs with shared IDs
- Generate suggestions (top 3)
- Append to context

**General Education Auto-Append**:
- Detect year/course query patterns via regex
- Build comprehensive Gen Ed context
- Include required courses
- Include category breakdown with sample courses
- Add to source metadata

### Post-Processing Pipeline

**Stage 1: Token Removal**
- Remove model control tokens (assistant, user, system)

**Stage 2: Pattern Removal**
- Remove English thinking patterns
- Comprehensive regex for common phrases

**Stage 3: Line-by-Line Filtering**
- Skip mode to remove leading junk
- Detect real Thai content (5+ characters)
- Filter English thinking lines

**Stage 4: Aggressive Cleanup**
- Find first real content with regex
- Remove leading fragments

**Stage 5: Final Cleanup**
- Remove single Thai character lines
- Trim whitespace

---

## Performance Characteristics

### Model Performance

- **Load Time**: 2-3 minutes (GPT-OSS-20B)
- **VRAM Usage**: ~12GB (model) + ~10GB (RAG) = ~22GB total
- **Inference Speed**: 40-80 tokens per second
- **Context Window**: 2048 tokens
- **Optimization**: 2x faster than FP16, 75% memory reduction

### RAG Performance

- **Catalog Loading**: <1 second (JSON format)
- **Document Loading**: 3-5 minutes (130+ PDFs)
- **Embedding Generation**: Batch processing (32 chunks/batch)
- **Search Latency**: 
  - Broad search: Fast (in-memory Qdrant)
  - Reranking: Moderate (50 pairs)
  - Post-filtering: Fast (5 results)
- **Accuracy**: High relevance through three-stage refinement

### System Requirements

**Google Colab**:
- A100 GPU (80GB VRAM recommended, 40GB minimum)
- Google Colab Pro Plus subscription
- Stable internet connection

**Storage**:
- Model cache: ~15GB
- Documents: ~5GB
- Vector database: In-memory (no disk storage)

---

## Technology Stack

**AI/ML**:
- GPT-OSS-20B (Unsloth 4-bit quantization)
- BGE-M3-Thai (embedding model)
- BGE-Reranker-v2-m3 (cross-encoder)
- PyTorch (deep learning framework)
- HuggingFace Transformers (model loading)

**Vector Database**:
- Qdrant (in-memory)
- Cosine similarity
- 1024-dimensional vectors

**Document Processing**:
- LangChain (document loaders)
- PyPDF (PDF parsing)
- RecursiveCharacterTextSplitter (chunking)

**Web Interface**:
- Gradio 4.0+ (UI framework)
- Share=True for public URL
- Real-time streaming

**Web Search**:
- DuckDuckGo Search
- Wikipedia API
- Bilingual support (Thai/English)

**Infrastructure**:
- Google Colab (cloud GPU)
- Git sparse checkout (document download)
- JSON catalogs (metadata storage)

---

## Security and Best Practices

**Token Management**:
- HuggingFace token stored in notebook (replace before use)
- Never commit real tokens to git
- Use placeholder values in repository

**Data Protection**:
- In-memory vector database (no persistence)
- No user data storage
- No authentication required (public demo)

**Error Handling**:
- Fallback generation mode for CUDA errors
- Graceful degradation when RAG unavailable
- Web search fallback on retrieval failure

**Resource Management**:
- CUDA cache clearing before generation
- Batch processing for embeddings
- Efficient memory usage with 4-bit quantization

---

## Limitations and Considerations

**Current Limitations**:
- Colab session timeout (~12 hours idle)
- A100 GPU access requires Colab Pro Plus
- In-memory database lost on restart
- No persistent chat history
- Single user session per notebook instance

**Future Improvements**:
- Persistent vector database
- Multi-user support
- Session management
- Query caching
- Analytics dashboard
- Voice input/output
- Mobile-responsive design

---

## Deployment Checklist

**Pre-Deployment**:
1. Obtain HuggingFace token with read access
2. Verify Google Colab Pro Plus subscription
3. Ensure stable internet connection
4. Clone repository or download notebook

**Deployment Steps**:
1. Upload notebook to Google Colab
2. Select A100 GPU runtime
3. Replace HuggingFace token placeholder
4. Run cells sequentially (1-10)
5. Wait for document loading completion
6. Copy public Gradio URL
7. Share URL with users

**Post-Deployment**:
1. Monitor system log for errors
2. Test RAG retrieval with sample queries
3. Verify General Education auto-append
4. Test web search functionality
5. Monitor VRAM usage (should be ~22GB)
6. Keep notebook running for continuous service

---

## Maintenance

**Regular Tasks**:
- Restart Colab session every 12 hours
- Monitor for model updates
- Update catalog JSON files as needed
- Review and update keywords periodically

**Troubleshooting**:
- CUDA errors: Restart runtime and re-run cells
- Slow inference: Check GPU allocation (should be A100)
- Missing documents: Verify GitHub sparse checkout succeeded
- No Gen Ed context: Check catalog file exists and loaded

---

**Document Version**: 2.0  
**Last Updated**: October 15, 2025  
**System Status**: Production Ready
