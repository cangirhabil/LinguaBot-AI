# Multilingual Chatbot SaaS - AI Service

Bu Python/FastAPI servisi, çok dilli destek botu SaaS platformunun AI katmanıdır. LangChain, OpenAI ve Pinecone kullanarak RAG (Retrieval-Augmented Generation) tabanlı çoklu dil desteği sağlar.

## Kurulum

### 1. Python Ortamını Hazırlayın

```bash
cd backend-python
python -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate     # Windows
```

### 2. Bağımlılıkları Kurun

```bash
pip install -r requirements.txt
```

### 3. Ortam Değişkenlerini Ayarlayın

```bash
cp .env.example .env
# .env dosyasını düzenleyerek API anahtarlarınızı ekleyin
```

### 4. Servisi Çalıştırın

```bash
uvicorn main:app --reload --port 8000
```

## API Endpoints

### POST /v1/ingest

SSS verilerini Pinecone vektör veritabanına işleyip depolar.

### POST /v1/query

Kullanıcı sorularını işleyip çoklu dil desteğiyle yanıt verir.

## Özellikler

- 🌍 **Çoklu Dil Desteği**: Otomatik dil algılama ve çeviri
- 🧠 **RAG Pipeline**: LangChain ile güçlü retrieval-augmented generation
- 🔍 **Vektör Arama**: Pinecone ile hızlı ve doğru bilgi retrieval
- 🔒 **Güvenlik**: API anahtarı tabanlı erişim kontrolü
- ⚡ **Hızlı**: FastAPI ile yüksek performanslı API
