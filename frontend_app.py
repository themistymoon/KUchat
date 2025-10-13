"""
Multi-Modal AI Chatbot Frontend with RAG
Supports Qwen3-Omni (multimodal) and GPT-OSS-120B (text)
"""

import gradio as gr
import requests
import base64
import json
from pathlib import Path
from typing import Optional, List
import tempfile
import os

# Configuration
API_URL = "YOUR_NGROK_URL_HERE"  # Replace with your ngrok URL from Colab

class ChatbotClient:
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip('/')
        self.conversation_history = []
    
    def check_health(self):
        """Check if API is accessible"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def query_qwen(self, text: str, image=None, audio=None, use_rag=False, 
                   use_web_search=False, max_tokens=512, temperature=0.7):
        """Query Qwen3-Omni model (multimodal)"""
        try:
            payload = {
                "prompt": text,
                "use_rag": use_rag,
                "use_web_search": use_web_search,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            # Encode image if provided
            if image is not None:
                if isinstance(image, str):
                    with open(image, "rb") as f:
                        image_bytes = f.read()
                else:
                    image_bytes = image
                payload["image_base64"] = base64.b64encode(image_bytes).decode()
            
            # Encode audio if provided
            if audio is not None:
                if isinstance(audio, str):
                    with open(audio, "rb") as f:
                        audio_bytes = f.read()
                else:
                    audio_bytes = audio
                payload["audio_base64"] = base64.b64encode(audio_bytes).decode()
            
            response = requests.post(f"{self.api_url}/qwen", json=payload, timeout=120)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def query_gpt(self, text: str, use_rag=False, use_web_search=False, 
                  max_tokens=512, temperature=0.7):
        """Query GPT-OSS model (text only)"""
        try:
            payload = {
                "prompt": text,
                "use_rag": use_rag,
                "use_web_search": use_web_search,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(f"{self.api_url}/gpt", json=payload, timeout=120)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def upload_documents(self, file_paths: List[str]):
        """Upload documents for RAG"""
        try:
            files = []
            for file_path in file_paths:
                if os.path.exists(file_path):
                    files.append(
                        ('files', (os.path.basename(file_path), open(file_path, 'rb')))
                    )
            
            if not files:
                return {"error": "No valid files to upload"}
            
            response = requests.post(f"{self.api_url}/upload-docs", files=files, timeout=60)
            
            # Close file handles
            for _, (_, file_handle) in files:
                file_handle.close()
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def clear_rag(self):
        """Clear RAG database"""
        try:
            response = requests.post(f"{self.api_url}/clear-rag", timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# Initialize client
client = ChatbotClient(API_URL)


# Gradio Interface Functions
def check_connection():
    """Check API connection"""
    if client.check_health():
        return "✅ Connected to API successfully!"
    else:
        return "❌ Cannot connect to API. Please check your API URL."


def chat_qwen(message, image, audio, use_rag, use_web_search, temperature, max_tokens, history):
    """Chat with Qwen3-Omni (Multimodal)"""
    if not message and not image and not audio:
        return history, history
    
    # Add user message to history
    user_content = f"**User:** {message}"
    if image:
        user_content += " [Image attached]"
    if audio:
        user_content += " [Audio attached]"
    if use_rag:
        user_content += " [RAG enabled]"
    if use_web_search:
        user_content += " [Web search enabled]"
    
    history.append([user_content, "Thinking..."])
    
    # Query the model
    result = client.query_qwen(
        text=message or "Describe what you see/hear",
        image=image,
        audio=audio,
        use_rag=use_rag,
        use_web_search=use_web_search,
        max_tokens=int(max_tokens),
        temperature=temperature
    )
    
    # Update history with response
    if "error" in result:
        response = f"❌ Error: {result['error']}"
    else:
        response = f"**Qwen3-Omni:** {result.get('response', 'No response')}"
    
    history[-1] = [user_content, response]
    
    return history, history


def chat_gpt(message, use_rag, use_web_search, temperature, max_tokens, history):
    """Chat with GPT-OSS (Text Only)"""
    if not message:
        return history, history
    
    # Add user message to history
    user_content = f"**User:** {message}"
    if use_rag:
        user_content += " [RAG enabled]"
    if use_web_search:
        user_content += " [Web search enabled]"
    
    history.append([user_content, "Thinking..."])
    
    # Query the model
    result = client.query_gpt(
        text=message,
        use_rag=use_rag,
        use_web_search=use_web_search,
        max_tokens=int(max_tokens),
        temperature=temperature
    )
    
    # Update history with response
    if "error" in result:
        response = f"❌ Error: {result['error']}"
    else:
        response = f"**GPT-OSS-120B:** {result.get('response', 'No response')}"
    
    history[-1] = [user_content, response]
    
    return history, history


def upload_docs_handler(files):
    """Handle document uploads for RAG"""
    if not files:
        return "No files selected"
    
    file_paths = [f.name for f in files]
    result = client.upload_documents(file_paths)
    
    if "error" in result:
        return f"❌ Error: {result['error']}"
    else:
        return f"✅ {result.get('message', 'Documents uploaded')}\n📊 Chunks added: {result.get('chunks_added', 0)}"


def clear_rag_handler():
    """Clear RAG database"""
    result = client.clear_rag()
    
    if "error" in result:
        return f"❌ Error: {result['error']}"
    else:
        return f"✅ {result.get('message', 'RAG database cleared')}"


# Create Gradio Interface
with gr.Blocks(title="Multi-Modal AI Chatbot with RAG", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 Multi-Modal AI Chatbot with RAG & Web Search
        ### Powered by Qwen3-Omni-30B & GPT-OSS-120B
        
        - **Qwen3-Omni**: Supports text, images, audio, and video (multimodal)
        - **GPT-OSS-120B**: Text-only conversations
        - **RAG**: Upload documents for context-aware responses
        - **Web Search**: Real-time information from DuckDuckGo & Wikipedia
        """
    )
    
    # Connection Status
    with gr.Row():
        with gr.Column(scale=3):
            api_url_input = gr.Textbox(
                label="API URL",
                value=API_URL,
                placeholder="Enter your ngrok URL from Colab"
            )
        with gr.Column(scale=1):
            check_btn = gr.Button("🔍 Check Connection", variant="secondary")
            status_output = gr.Textbox(label="Status", interactive=False)
    
    def update_api_url(url):
        client.api_url = url.rstrip('/')
        return check_connection()
    
    check_btn.click(fn=check_connection, outputs=status_output)
    api_url_input.change(fn=update_api_url, inputs=api_url_input, outputs=status_output)
    
    # Main Chat Interface
    with gr.Tabs():
        # Qwen3-Omni Tab (Multimodal)
        with gr.Tab("🎨 Qwen3-Omni (Multimodal)"):
            gr.Markdown("### Supports: Text + Images + Audio + Video")
            
            with gr.Row():
                with gr.Column(scale=2):
                    qwen_chatbot = gr.Chatbot(
                        label="Conversation",
                        height=500,
                        show_copy_button=True
                    )
                    
                    with gr.Row():
                        qwen_message = gr.Textbox(
                            label="Message",
                            placeholder="Type your message here...",
                            lines=2,
                            scale=4
                        )
                    
                    with gr.Row():
                        qwen_image = gr.Image(
                            label="Upload Image (Optional)",
                            type="filepath",
                            height=150
                        )
                        qwen_audio = gr.Audio(
                            label="Upload Audio (Optional)",
                            type="filepath"
                        )
                    
                    with gr.Row():
                        qwen_submit = gr.Button("🚀 Send", variant="primary", scale=2)
                        qwen_clear = gr.Button("🗑️ Clear Chat", scale=1)
                
                with gr.Column(scale=1):
                    gr.Markdown("### Settings")
                    qwen_use_rag = gr.Checkbox(
                        label="Enable RAG",
                        value=False,
                        info="Use uploaded documents for context"
                    )
                    qwen_use_web_search = gr.Checkbox(
                        label="Enable Web Search",
                        value=False,
                        info="Search the internet for real-time info"
                    )
                    qwen_temperature = gr.Slider(
                        minimum=0.1,
                        maximum=1.0,
                        value=0.7,
                        step=0.1,
                        label="Temperature",
                        info="Higher = more creative"
                    )
                    qwen_max_tokens = gr.Slider(
                        minimum=128,
                        maximum=2048,
                        value=512,
                        step=128,
                        label="Max Tokens",
                        info="Maximum response length"
                    )
            
            qwen_state = gr.State([])
            
            qwen_submit.click(
                fn=chat_qwen,
                inputs=[qwen_message, qwen_image, qwen_audio, qwen_use_rag, 
                       qwen_use_web_search, qwen_temperature, qwen_max_tokens, qwen_state],
                outputs=[qwen_chatbot, qwen_state]
            ).then(
                fn=lambda: ("", None, None),
                outputs=[qwen_message, qwen_image, qwen_audio]
            )
            
            qwen_clear.click(fn=lambda: ([], []), outputs=[qwen_chatbot, qwen_state])
        
        # GPT-OSS Tab (Text Only)
        with gr.Tab("📝 GPT-OSS-120B (Text)"):
            gr.Markdown("### Supports: Text Only")
            
            with gr.Row():
                with gr.Column(scale=2):
                    gpt_chatbot = gr.Chatbot(
                        label="Conversation",
                        height=500,
                        show_copy_button=True
                    )
                    
                    gpt_message = gr.Textbox(
                        label="Message",
                        placeholder="Type your message here...",
                        lines=3
                    )
                    
                    with gr.Row():
                        gpt_submit = gr.Button("🚀 Send", variant="primary", scale=2)
                        gpt_clear = gr.Button("🗑️ Clear Chat", scale=1)
                
                with gr.Column(scale=1):
                    gr.Markdown("### Settings")
                    gpt_use_rag = gr.Checkbox(
                        label="Enable RAG",
                        value=False,
                        info="Use uploaded documents for context"
                    )
                    gpt_use_web_search = gr.Checkbox(
                        label="Enable Web Search",
                        value=False,
                        info="Search the internet for real-time info"
                    )
                    gpt_temperature = gr.Slider(
                        minimum=0.1,
                        maximum=1.0,
                        value=0.7,
                        step=0.1,
                        label="Temperature",
                        info="Higher = more creative"
                    )
                    gpt_max_tokens = gr.Slider(
                        minimum=128,
                        maximum=2048,
                        value=512,
                        step=128,
                        label="Max Tokens",
                        info="Maximum response length"
                    )
            
            gpt_state = gr.State([])
            
            gpt_submit.click(
                fn=chat_gpt,
                inputs=[gpt_message, gpt_use_rag, gpt_use_web_search, 
                       gpt_temperature, gpt_max_tokens, gpt_state],
                outputs=[gpt_chatbot, gpt_state]
            ).then(
                fn=lambda: "",
                outputs=gpt_message
            )
            
            gpt_clear.click(fn=lambda: ([], []), outputs=[gpt_chatbot, gpt_state])
        
        # RAG Management Tab
        with gr.Tab("📚 RAG Document Management"):
            gr.Markdown(
                """
                ### Upload Documents for Context-Aware Responses
                
                Supported formats: PDF, TXT, MD
                
                Upload documents to enable RAG (Retrieval Augmented Generation) for more accurate,
                context-aware responses from both models.
                """
            )
            
            with gr.Row():
                with gr.Column():
                    doc_files = gr.File(
                        label="Upload Documents",
                        file_count="multiple",
                        file_types=[".pdf", ".txt", ".md"]
                    )
                    
                    with gr.Row():
                        upload_btn = gr.Button("📤 Upload Documents", variant="primary")
                        clear_rag_btn = gr.Button("🗑️ Clear RAG Database", variant="stop")
                    
                    rag_status = gr.Textbox(
                        label="Status",
                        interactive=False,
                        lines=3
                    )
            
            upload_btn.click(fn=upload_docs_handler, inputs=doc_files, outputs=rag_status)
            clear_rag_btn.click(fn=clear_rag_handler, outputs=rag_status)
    
    # Footer
    gr.Markdown(
        """
        ---
        💡 **Tips:**
        - Enable **RAG** after uploading documents for context-aware responses
        - Enable **Web Search** for real-time information from the internet
        - Use both RAG + Web Search together for comprehensive answers
        - Use Qwen3-Omni for multimodal tasks (images, audio)
        - Use GPT-OSS for pure text conversations
        - Adjust temperature for creativity vs. consistency
        
        🌐 **Web Search Features:**
        - DuckDuckGo search results
        - Wikipedia summaries (English & Thai)
        - Combine with RAG for document + web context
        """
    )


if __name__ == "__main__":
    print("="*60)
    print("🚀 Starting Multi-Modal AI Chatbot Frontend")
    print("="*60)
    print(f"\n📡 API URL: {API_URL}")
    print("\n⚠️  Make sure to update API_URL with your ngrok URL!")
    print("\n🌐 Starting Gradio interface...")
    print("="*60)
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
