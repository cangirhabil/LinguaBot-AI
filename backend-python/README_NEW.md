# Multilingual Chatbot AI Service 🤖

A FastAPI-based AI service that provides multilingual chatbot capabilities using RAG (Retrieval-Augmented Generation) with OpenAI and Pinecone.

## ✨ Features

- **Multilingual Support**: Automatic language detection and translation
- **RAG Pipeline**: Combines document retrieval with AI generation
- **Vector Search**: Semantic search using Pinecone vector database
- **API Authentication**: Secure API key-based authentication
- **Development Mode**: Graceful fallbacks when API keys are not configured
- **FastAPI**: Modern, fast web framework with automatic API documentation

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│   AI Service     │───▶│   OpenAI GPT    │
│  (Any Language) │    │                  │    │   (Translation  │
└─────────────────┘    │ 1. Detect Lang   │    │   & Generation) │
                       │ 2. Translate     │    └─────────────────┘
┌─────────────────┐    │ 3. Retrieve      │
│   Pinecone      │◀───│ 4. Generate      │    ┌─────────────────┐
│ Vector Database │    │ 5. Translate Back│───▶│    Response     │
│   (FAQ Store)   │    └──────────────────┘    │  (User's Lang)  │
└─────────────────┘                            └─────────────────┘
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone and navigate to the project
cd backend-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and configure your API keys:

```env
# OpenAI API Key (for embeddings and chat)
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration (for vector storage)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=multilang-chatbot-index

# API Authentication (for service security)
API_KEY=your_secure_api_key_here
```

### 3. Start the Service

```bash
# Using the startup script
./start_dev.sh

# Or manually
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The service will be available at:

- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### 🏥 Health Check

```http
GET /health
```

### 📥 Ingest FAQs

```http
POST /v1/ingest
Headers: X-API-KEY: your_api_key
Content-Type: application/json

{
  "user_id": "user123",
  "faqs": [
    {
      "question": "How can I cancel my order?",
      "answer": "You can cancel your order by logging into your account..."
    }
  ]
}
```

### ❓ Query Chatbot

```http
POST /v1/query
Headers: X-API-KEY: your_api_key
Content-Type: application/json

{
  "user_id": "user123",
  "message": "¿Cómo puedo cancelar mi pedido?"
}
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Make sure the server is running first
python test_api.py
```

The test suite validates:

- ✅ Health check endpoint
- ✅ Root endpoint
- ✅ API authentication
- ✅ FAQ ingestion
- ✅ Multilingual query processing

## 🌍 Supported Languages

The service automatically detects and translates between:

- 🇹🇷 Turkish (`tr`)
- 🇺🇸 English (`en`)
- 🇪🇸 Spanish (`es`)
- 🇫🇷 French (`fr`)
- 🇩🇪 German (`de`)
- 🇮🇹 Italian (`it`)
- 🇵🇹 Portuguese (`pt`)
- 🇷🇺 Russian (`ru`)
- 🇸🇦 Arabic (`ar`)
- 🇨🇳 Chinese (`zh`)
- 🇯🇵 Japanese (`ja`)
- 🇰🇷 Korean (`ko`)

## 🔧 Development Mode

When API keys are not configured, the service runs in development mode:

- ⚠️ OpenAI features are mocked
- ⚠️ Pinecone vector storage is simulated
- ✅ All endpoints remain functional for testing
- ✅ API structure and authentication work normally

## 📊 Technology Stack

| Component              | Technology     | Purpose                           |
| ---------------------- | -------------- | --------------------------------- |
| **Web Framework**      | FastAPI        | HTTP API and documentation        |
| **AI/LLM**             | OpenAI GPT-3.5 | Text generation and translation   |
| **Embeddings**         | OpenAI Ada-002 | Text vectorization                |
| **Vector DB**          | Pinecone       | Semantic search and storage       |
| **Language Chain**     | LangChain      | RAG pipeline orchestration        |
| **Language Detection** | langdetect     | Automatic language identification |
| **Validation**         | Pydantic       | Request/response validation       |

## 🏢 Integration

This AI service is designed to integrate with:

- **Node.js Backend**: Orchestration service (planned)
- **Next.js Frontend**: Admin panel and chat widget (planned)
- **External APIs**: Via secure API key authentication

## 📁 Project Structure

```
backend-python/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic data models
├── requirements.txt     # Python dependencies
├── test_api.py         # Comprehensive API tests
├── start_dev.sh        # Development startup script
├── .env.example        # Environment variables template
├── .env                # Your configuration (not in git)
└── services/
    ├── __init__.py
    ├── ai_service.py   # Core AI/RAG logic
    └── auth_service.py # API key authentication
```

## 🔒 Security

- 🔑 API key authentication for all protected endpoints
- 🏠 CORS middleware configured for specific origins
- 🔐 Environment variables for sensitive configuration
- 🚫 No hardcoded secrets in source code

## 🎯 Next Steps

1. **Configure API Keys**: Add your OpenAI and Pinecone keys to `.env`
2. **Test with Real Data**: Ingest your FAQ data and test queries
3. **Node.js Integration**: Build the orchestration service
4. **Frontend Integration**: Create the admin panel and chat widget
5. **Production Deployment**: Set up hosting and monitoring

## 🤝 Contributing

1. Follow the existing code style and patterns
2. Add tests for new features
3. Update documentation for changes
4. Use type hints for all function parameters
5. Follow the project's architectural principles

---

**🎉 The AI service is ready for integration and testing!**

For more details, visit the interactive API documentation at http://localhost:8000/docs when the service is running.
