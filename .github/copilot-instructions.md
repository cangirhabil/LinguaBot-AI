<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Multilingual Chatbot SaaS Project Instructions

This is a multilingual chatbot SaaS platform with a hybrid architecture:

## Project Structure

- `backend-python/`: FastAPI AI service for RAG pipeline and multilingual support
- `backend-node/`: Node.js/Express orchestrator service (to be created)
- `frontend/`: Next.js admin panel and chat widget (to be created)

## Current Focus: Python/FastAPI AI Service

### Key Technologies

- **FastAPI**: Modern Python web framework for APIs
- **LangChain**: LLM application framework with LCEL (LangChain Expression Language)
- **OpenAI**: GPT models for translation and answering
- **Pinecone**: Vector database for semantic search
- **Pydantic**: Data validation and serialization

### Architecture Patterns

- **RAG (Retrieval-Augmented Generation)**: Combines retrieval with generation
- **Multi-step Pipeline**: Translation → Retrieval → Generation → Translation back
- **Namespace Isolation**: Each user's data is isolated in Pinecone namespaces
- **API Key Authentication**: Secure communication between services

### Code Style Preferences

- Use async/await for all I/O operations
- Type hints for all function parameters and returns
- Pydantic models for request/response validation
- Comprehensive error handling with informative messages
- Environment variables for all configuration
- Clear docstrings following Google style

### Key Concepts

- **Embedding**: Converting text to vector representations for similarity search
- **Vector Store**: Database optimized for vector similarity search
- **Retriever**: Component that finds relevant documents based on query
- **Chain**: Sequence of operations in LangChain (prompt → LLM → parser)
- **Namespace**: Pinecone feature to isolate different user data
