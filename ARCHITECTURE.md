# System Architecture Diagrams

## Overall System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     USER INTERACTION                                 │
│                  (Web Browser - localhost:7860)                      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Local System)                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Gradio Web Interface                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │   │
│  │  │ Qwen3-Omni   │  │   GPT-OSS    │  │ RAG Manager  │      │   │
│  │  │     Tab      │  │     Tab      │  │     Tab      │      │   │
│  │  │ (Multimodal) │  │   (Text)     │  │   (Docs)     │      │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Frontend Components:                                                │
│  • ChatbotClient (API wrapper)                                      │
│  • File upload handlers                                             │
│  • Parameter controls (temp, tokens)                                │
│  • Connection status monitor                                        │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                     HTTPS Requests
                     (via ngrok URL)
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        NGROK TUNNEL                                  │
│                 (Public URL → Colab Internal)                        │
│         https://xxxx-xxx.ngrok.io → localhost:8000                   │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│              BACKEND (Google Colab - A100 GPU)                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              FastAPI Server (:8000)                          │   │
│  │  Endpoints:                                                  │   │
│  │    • POST /qwen → Multimodal inference                      │   │
│  │    • POST /gpt → Text inference                             │   │
│  │    • POST /upload-docs → Add to RAG                         │   │
│  │    • POST /clear-rag → Reset database                       │   │
│  │    • GET /health → Status check                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              AI MODELS (A100 GPU)                            │   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────────┐            │   │
│  │  │    Qwen3-Omni-30B-A3B-Instruct             │            │   │
│  │  │    • 4-bit quantized (NF4)                 │            │   │
│  │  │    • Multimodal: text, image, audio, video │            │   │
│  │  │    • VRAM: ~20-25GB                        │            │   │
│  │  │    • AutoProcessor + AutoModelForCausalLM  │            │   │
│  │  └────────────────────────────────────────────┘            │   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────────┐            │   │
│  │  │    GPT-OSS-120B-Unsloth-BNB-4bit           │            │   │
│  │  │    • Pre-quantized 4-bit                   │            │   │
│  │  │    • Text-only processing                  │            │   │
│  │  │    • VRAM: ~30-35GB                        │            │   │
│  │  │    • AutoTokenizer + AutoModelForCausalLM  │            │   │
│  │  └────────────────────────────────────────────┘            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              RAG SYSTEM (ChromaDB)                           │   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────┐                │   │
│  │  │   Document Processing Pipeline         │                │   │
│  │  │   1. Upload (PDF/TXT/MD)               │                │   │
│  │  │   2. Text Extraction                   │                │   │
│  │  │   3. Chunking (1000 chars, 200 overlap)│                │   │
│  │  │   4. Embedding Generation              │                │   │
│  │  │   5. Vector Storage                    │                │   │
│  │  └────────────────────────────────────────┘                │   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────┐                │   │
│  │  │   Retrieval Pipeline                   │                │   │
│  │  │   1. Query Embedding                   │                │   │
│  │  │   2. Similarity Search (k=4)           │                │   │
│  │  │   3. Context Assembly                  │                │   │
│  │  │   4. Augmented Prompt                  │                │   │
│  │  └────────────────────────────────────────┘                │   │
│  │                                                              │   │
│  │  Embedding Model: all-MiniLM-L6-v2 (GPU)                    │   │
│  │  Vector DB: ChromaDB (/content/chroma_db)                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Request Flow Diagrams

### Text-Only Request (GPT-OSS)

```
User Input (Frontend)
        ↓
[Gradio Interface]
        ↓
ChatbotClient.query_gpt()
        ↓
HTTPS POST → ngrok URL → /gpt
        ↓
[FastAPI Endpoint: gpt_endpoint()]
        ↓
   ┌─────────────────────┐
   │  RAG Enabled?       │
   └─────┬───────────────┘
         │
    ├─ Yes → [RAG System]
    │         ↓
    │    Retrieve documents
    │         ↓
    │    Build context
    │         ↓
    └─ No ──→ [Original prompt]
         ↓
[gpt_inference()]
         ↓
Tokenize input
         ↓
[GPT-OSS Model]
         ↓
Generate response
         ↓
Decode output
         ↓
Return JSON
         ↓
[Frontend receives response]
         ↓
Update chat interface
         ↓
Display to user
```

### Multimodal Request (Qwen3-Omni)

```
User Input (Frontend)
        ↓
[Text] + [Image?] + [Audio?]
        ↓
[Gradio Interface]
        ↓
ChatbotClient.query_qwen()
        ↓
Base64 encode media files
        ↓
HTTPS POST → ngrok URL → /qwen
        ↓
[FastAPI Endpoint: qwen_endpoint()]
        ↓
Decode base64 media
        ↓
   ┌─────────────────────┐
   │  RAG Enabled?       │
   └─────┬───────────────┘
         │
    ├─ Yes → [RAG System]
    │         ↓
    │    Retrieve documents
    │         ↓
    │    Build context
    │         ↓
    └─ No ──→ [Original prompt]
         ↓
[qwen_inference()]
         ↓
Process multimodal inputs
    ┌──────┬──────┬──────┐
    │ Text │Image │Audio │
    └──────┴──────┴──────┘
         ↓
[Qwen3-Omni Processor]
         ↓
Unified input tensor
         ↓
[Qwen3-Omni Model]
         ↓
Generate response
         ↓
Decode output
         ↓
Return JSON
         ↓
[Frontend receives response]
         ↓
Update chat interface
         ↓
Display to user
```

### RAG Document Upload Flow

```
User selects files (Frontend)
        ↓
[PDF, TXT, MD files]
        ↓
[Gradio File Upload]
        ↓
upload_docs_handler()
        ↓
HTTPS POST → ngrok URL → /upload-docs
        ↓
[FastAPI Endpoint: upload_documents()]
        ↓
Save files to /content/uploaded_docs
        ↓
[RAG System: add_documents()]
        ↓
┌────────────────────────┐
│  For each document:    │
│                        │
│  1. Load file          │
│   ├─ PDF → PyPDFLoader│
│   ├─ TXT → TextLoader │
│   └─ MD → TextLoader  │
│                        │
│  2. Extract text       │
│                        │
│  3. Split into chunks  │
│     (1000 chars, 200   │
│      overlap)          │
│                        │
│  4. Generate embeddings│
│     (all-MiniLM-L6-v2) │
│                        │
│  5. Store in ChromaDB  │
│                        │
└────────────────────────┘
        ↓
Return: {
  "message": "Success",
  "chunks_added": N
}
        ↓
[Frontend displays status]
        ↓
Documents ready for RAG queries
```

## Component Interaction Map

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│        Gradio Interface              │
│  ┌────────────────────────────────┐  │
│  │      UI Components             │  │
│  │      • Textboxes               │  │
│  │      • File uploaders          │  │
│  │      • Sliders                 │  │
│  │      • Buttons                 │  │
│  │      • Chatbot display         │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │      Event Handlers            │  │
│  │      • chat_qwen()             │  │
│  │      • chat_gpt()              │  │
│  │      • upload_docs_handler()   │  │
│  │      • check_connection()      │  │
│  └────────────────────────────────┘  │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│     ChatbotClient Class              │
│  ┌────────────────────────────────┐  │
│  │       Methods                  │  │
│  │       • query_qwen()           │  │
│  │       • query_gpt()            │  │
│  │       • upload_documents()     │  │
│  │       • clear_rag()            │  │
│  │       • check_health()         │  │
│  └────────────────────────────────┘  │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│   Network Layer (HTTPS)              │
│   via Ngrok Tunnel                   │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│      FastAPI Router                  │
│  ┌────────────────────────────────┐  │
│  │       Endpoints                │  │
│  │       • @app.get("/")          │  │
│  │       • @app.post("/qwen")     │  │
│  │       • @app.post("/gpt")      │  │
│  │       • @app.post("/upload-docs")│ │
│  │       • @app.post("/clear-rag")│  │
│  │       • @app.get("/health")    │  │
│  └────────────────────────────────┘  │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│    Inference Functions               │
│  ┌────────────────────────────────┐  │
│  │    • qwen_inference()          │  │
│  │    • gpt_inference()           │  │
│  └────────────────────────────────┘  │
└──────┬────────────┬──────────────────┘
       │            │
       ▼            ▼
  ┌──────────┐  ┌──────────┐
  │  Qwen    │  │   GPT    │
  │  Model   │  │  Model   │
  └──────────┘  └──────────┘
       │            │
       └─────┬──────┘
             │
             ▼
       ┌────────────┐
       │ RAG System │
       └────────────┘
             │
             ▼
       ┌────────────┐
       │  ChromaDB  │
       └────────────┘
```

## Data Flow: RAG-Enhanced Query

```
┌─────────────────────────────────────────────────────────────┐
│                      USER QUERY                              │
│         "What are the main points in my document?"           │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │   RAG Enabled? (Yes)     │
                └──────────┬───────────────┘
                           │
                           ▼
            ┌───────────────────────────────────┐
            │    RAG System: retrieve()         │
            └───────────────┬───────────────────┘
                           │
                           ▼
            ┌───────────────────────────────────┐
            │  1. Embed query with              │
            │     all-MiniLM-L6-v2              │
            │                                   │
            │  Query → [0.234, -0.123, ...]     │
            └───────────────┬───────────────────┘
                           │
                           ▼
            ┌───────────────────────────────────┐
            │  2. Search ChromaDB               │
            │     similarity_search(query, k=4) │
            │                                   │
            │  Find top 4 most similar chunks   │
            └───────────────┬───────────────────┘
                           │
                           ▼
            ┌───────────────────────────────────┐
            │  3. Retrieve document chunks      │
            │                                   │
            │  Chunk 1: "Machine learning is..." │
            │  Chunk 2: "The key benefits are..."│
            │  Chunk 3: "Applications include..." │
            │  Chunk 4: "Future trends show..."  │
            └───────────────┬───────────────────┘
                           │
                           ▼
            ┌───────────────────────────────────┐
            │  4. Build augmented prompt        │
            │                                   │
            │  Context:                         │
            │    [Chunk 1]                      │
            │    [Chunk 2]                      │
            │    [Chunk 3]                      │
            │    [Chunk 4]                      │
            │                                   │
            │  Question: What are the main      │
            │  points in my document?           │
            └───────────────┬───────────────────┘
                           │
                           ▼
            ┌───────────────────────────────────┐
            │  5. Send to Model                 │
            │     (Qwen or GPT)                 │
            └───────────────┬───────────────────┘
                           │
                           ▼
            ┌───────────────────────────────────┐
            │  6. Model generates response      │
            │     using retrieved context       │
            │                                   │
            │  "Based on the document, the main │
            │   points are: 1) ML enables...    │
            │   2) Key benefits include...      │
            │   3) Applications span..."        │
            └───────────────┬───────────────────┘
                           │
                           ▼
                ┌──────────────────────────┐
                │   Return to Frontend     │
                └──────────┬───────────────┘
                           │
                           ▼
                ┌──────────────────────────┐
                │   Display in Chat UI     │
                └──────────────────────────┘
```

## Memory Layout (A100 80GB GPU)

```
┌────────────────────────────────────────────────────┐
│         A100 GPU VRAM (80GB Total)                 │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  Qwen3-Omni-30B (4-bit quantized)        │    │
│  │  Model weights: ~20GB                    │    │
│  │  Activations: ~3-5GB                     │    │
│  │  Total: ~20-25GB                         │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  GPT-OSS-120B (4-bit quantized)          │    │
│  │  Model weights: ~30GB                    │    │
│  │  Activations: ~3-5GB                     │    │
│  │  Total: ~30-35GB                         │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  Embedding Model (all-MiniLM-L6-v2)      │    │
│  │  Model weights: ~100MB                   │    │
│  │  Working memory: ~200MB                  │    │
│  │  Total: ~300MB                           │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  PyTorch / CUDA overhead                 │    │
│  │  ~2-5GB                                  │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  Free / Buffer                           │    │
│  │  ~15-20GB                                │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
└────────────────────────────────────────────────────┘

Total Used: ~55-65GB out of 80GB
Safety Margin: ~15-25GB
```

---

These diagrams provide a comprehensive view of how all components interact!
