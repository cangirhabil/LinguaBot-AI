# 🤖 Multilingual Chatbot SaaS Platform

A comprehensive SaaS platform for creating multilingual chatbots with advanced RAG (Retrieval-Augmented Generation) capabilities.

## 🏗️ Architecture

This is a hybrid architecture project with three main components:

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│                     │    │                     │    │                     │
│   Frontend          │    │   Node.js Backend   │    │   Python AI Service │
│   (Next.js)         │◀──▶│   (Express)         │◀──▶│   (FastAPI)         │
│                     │    │                     │    │                     │
│ • Admin Panel       │    │ • API Orchestrator  │    │ • RAG Pipeline      │
│ • Chat Widget       │    │ • User Management   │    │ • OpenAI Integration│
│ • Dashboard         │    │ • Authentication    │    │ • Pinecone Vector DB│
│                     │    │ • Business Logic    │    │ • Language Detection│
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

## 📁 Project Structure

```
multilingual-chatbot-saas/
├── 📄 README.md                    # This file
├── 📄 .gitignore                   # Git ignore rules
├── 📁 .github/                     # GitHub configuration
│   └── copilot-instructions.md     # AI development guidelines
├── 📁 backend-python/              # ✅ AI Service (FastAPI)
│   ├── main.py                     # FastAPI application
│   ├── models.py                   # Pydantic models
│   ├── requirements.txt            # Python dependencies
│   ├── test_api.py                 # API tests
│   ├── start_dev.sh                # Development startup script
│   ├── .env.example                # Environment template
│   ├── README_NEW.md               # Detailed AI service docs
│   └── services/
│       ├── ai_service.py           # RAG pipeline logic
│       └── auth_service.py         # API authentication
├── 📁 backend-node/                # 🔄 Orchestrator Service (To be created)
│   ├── package.json
│   ├── src/
│   │   ├── app.js
│   │   ├── routes/
│   │   ├── middleware/
│   │   └── controllers/
│   └── .env.example
└── 📁 frontend/                    # 🔄 Next.js Frontend (To be created)
    ├── package.json
    ├── src/
    │   ├── app/
    │   ├── components/
    │   ├── lib/
    │   └── styles/
    └── .env.example
```

## ✅ Current Status

### 🎉 Completed: AI Service (Python/FastAPI)
- ✅ **RAG Pipeline**: LangChain + OpenAI + Pinecone integration
- ✅ **Multilingual Support**: 12+ languages with automatic detection
- ✅ **API Endpoints**: Health, FAQ ingestion, query processing
- ✅ **Authentication**: Secure API key-based auth
- ✅ **Development Mode**: Graceful fallbacks without API keys
- ✅ **Testing**: Comprehensive test suite (5/5 tests passing)
- ✅ **Documentation**: Interactive API docs at `/docs`
- ✅ **Git Repository**: Initialized with proper `.gitignore`

### 🔄 Next: Node.js Backend (Orchestrator)
- 🔄 **API Gateway**: Route requests between frontend and AI service
- 🔄 **User Management**: Registration, authentication, profiles
- 🔄 **Business Logic**: Subscription plans, usage tracking
- 🔄 **Database**: PostgreSQL with Prisma ORM
- 🔄 **Middleware**: Rate limiting, logging, validation

### 🔄 Future: Next.js Frontend
- 🔄 **Admin Panel**: User dashboard, FAQ management
- 🔄 **Chat Widget**: Embeddable chatbot component
- 🔄 **Authentication**: User login/registration
- 🔄 **Analytics**: Usage statistics and insights

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+ (for future components)
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd multilingual-chatbot-saas
```

### 2. Start AI Service
```bash
cd backend-python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
./start_dev.sh
```

The AI service will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### 3. Test the Service
```bash
cd backend-python
python test_api.py
```

## 🌟 Key Features

### 🤖 AI Capabilities
- **RAG Pipeline**: Combines document retrieval with AI generation
- **Multilingual**: Automatic language detection and translation
- **Semantic Search**: Vector-based similarity search with Pinecone
- **Context Aware**: Maintains conversation context and user isolation

### 🔒 Security
- **API Authentication**: Secure key-based access control
- **Data Isolation**: User data separated via namespaces
- **Environment Variables**: Secure configuration management
- **CORS Protection**: Controlled cross-origin access

### ⚡ Performance
- **Async/Await**: Non-blocking I/O operations
- **FastAPI**: High-performance Python web framework
- **Vector Search**: Sub-second semantic search
- **Caching**: Efficient data retrieval and storage

### 🔧 Developer Experience
- **Type Safety**: Full TypeScript and Python type hints
- **Auto Documentation**: Interactive API docs
- **Development Mode**: Test without external dependencies
- **Comprehensive Testing**: Automated test suite
- **Clear Structure**: Well-organized, maintainable code

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **AI Service** | FastAPI + LangChain | RAG pipeline and AI logic |
| **LLM** | OpenAI GPT-3.5/4 | Text generation and translation |
| **Vector DB** | Pinecone | Semantic search and embeddings |
| **Backend** | Node.js + Express | API orchestration and business logic |
| **Database** | PostgreSQL + Prisma | User data and configuration |
| **Frontend** | Next.js + React | User interface and admin panel |
| **Auth** | JWT + bcrypt | Authentication and authorization |
| **Deployment** | Docker + AWS/Vercel | Containerization and hosting |

## 📊 API Examples

### FAQ Ingestion
```bash
curl -X POST "http://localhost:8000/v1/ingest" \
  -H "X-API-KEY: dev-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "faqs": [
      {
        "question": "How can I cancel my order?",
        "answer": "You can cancel your order by logging into your account..."
      }
    ]
  }'
```

### Multilingual Query
```bash
curl -X POST "http://localhost:8000/v1/query" \
  -H "X-API-KEY: dev-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "¿Cómo puedo cancelar mi pedido?"
  }'
```

## 🎯 Roadmap

### Phase 1: Foundation ✅
- [x] AI Service with RAG pipeline
- [x] Multilingual support
- [x] API authentication
- [x] Comprehensive testing
- [x] Documentation and Git setup

### Phase 2: Backend Orchestration 🔄
- [ ] Node.js Express server
- [ ] User management system
- [ ] PostgreSQL database setup
- [ ] API gateway implementation
- [ ] Rate limiting and monitoring

### Phase 3: Frontend Development 🔄
- [ ] Next.js application setup
- [ ] Admin dashboard
- [ ] Chat widget component
- [ ] User authentication flow
- [ ] Analytics and reporting

### Phase 4: Production Deployment 🔄
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS/Vercel)
- [ ] Monitoring and logging
- [ ] Performance optimization

## 🤝 Contributing

1. **Follow Project Structure**: Maintain the hybrid architecture
2. **Code Quality**: Use type hints, async/await, and proper error handling
3. **Testing**: Add tests for new features
4. **Documentation**: Update docs for changes
5. **Git Workflow**: Use meaningful commit messages

## 📞 Support

For questions and support:
- 📚 Check the component-specific README files
- 🔍 Review the interactive API documentation
- 🧪 Run the test suites to validate setup
- 📝 Follow the architecture guidelines in `.github/copilot-instructions.md`

---

**🎉 Ready to build the future of multilingual chatbots!**

Current status: **AI Service Complete** ✅ | Next: **Node.js Backend** 🔄
