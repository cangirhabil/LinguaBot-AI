import os
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from pinecone import Pinecone
from langdetect import detect
from models import FAQ

class AIService:
    """
    AI servisi - RAG pipeline ile çoklu dil desteği sağlar
    """
    
    def __init__(self):
        self.pc = None  # Pinecone client
        self.index = None
        self.embeddings = None
        self.llm = None
        self.vector_store = None
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "multilang-chatbot-index")
        
    async def initialize(self):
        """Servis başlatma - Pinecone, OpenAI bağlantıları"""
        try:
            # OpenAI bağlantısı
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key or openai_api_key == "your_openai_api_key_here":
                print("⚠️ OPENAI_API_KEY not set. AI features will be limited.")
                # Mock objects for development
                self.embeddings = None
                self.llm = None
            else:
                self.embeddings = OpenAIEmbeddings(
                    openai_api_key=openai_api_key,
                    model="text-embedding-ada-002"
                )
                
                self.llm = ChatOpenAI(
                    openai_api_key=openai_api_key,
                    model="gpt-3.5-turbo",
                    temperature=0.3
                )
            
            # Pinecone bağlantısı
            pinecone_api_key = os.getenv("PINECONE_API_KEY")
            if not pinecone_api_key or pinecone_api_key == "your_pinecone_api_key_here":
                print("⚠️ PINECONE_API_KEY not set. Vector store will be mocked.")
                # Mock için index
                self.pc = None
                self.index = None
            else:
                # Pinecone client'ı başlat (new API)
                self.pc = Pinecone(api_key=pinecone_api_key)
                
                # Index'i kontrol et ve gerekirse oluştur
                await self._ensure_index_exists()
            
            print("AI Service initialized successfully")
            
        except Exception as e:
            print(f"Failed to initialize AI Service: {str(e)}")
            print("⚠️ Running in development mode with limited functionality")
            # Don't raise exception in development
            self.pc = None
            self.index = None
            self.embeddings = None
            self.llm = None
    
    async def _ensure_index_exists(self):
        """Pinecone index'ini kontrol et ve gerekirse oluştur"""
        try:
            if not self.pc:
                return
                
            # Mevcut index'leri listele
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                print(f"Creating new Pinecone index: {self.index_name}")
                
                # Yeni index oluştur
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI ada-002 embedding dimension
                    metric="cosine",
                    spec={
                        "serverless": {
                            "cloud": "aws",
                            "region": "us-east-1"
                        }
                    }
                )
                
                print(f"Index {self.index_name} created successfully")
            
            # Index'e bağlan
            self.index = self.pc.Index(self.index_name)
            print(f"Connected to index: {self.index_name}")
            
        except Exception as e:
            print(f"Error ensuring index exists: {str(e)}")
            raise
    
    async def ingest_faqs(self, faqs: List[FAQ], user_id: str) -> bool:
        """
        SSS verilerini işleyip Pinecone'a yükler
        
        Args:
            faqs: SSS listesi
            user_id: Kullanıcı ID'si (namespace için)
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            if not faqs:
                return True
            
            # Development mode check
            if not self.embeddings or not self.index:
                print("⚠️ Running in development mode - FAQ ingestion simulated")
                print(f"Would ingest {len(faqs)} FAQs for user {user_id}")
                return True
            
            # Her SSS için doküman oluştur
            documents = []
            for i, faq in enumerate(faqs):
                # Soru ve cevabı birleştir
                content = f"Soru: {faq.question}\nCevap: {faq.answer}"
                
                doc = Document(
                    page_content=content,
                    metadata={
                        "question": faq.question,
                        "answer": faq.answer,
                        "user_id": user_id,
                        "faq_id": f"{user_id}_{i}"
                    }
                )
                documents.append(doc)
            
            # Vektör store oluştur ve dökümanları ekle
            vector_store = PineconeVectorStore.from_documents(
                documents=documents,
                embedding=self.embeddings,
                index_name=self.index_name,
                namespace=user_id  # Kullanıcı verilerini ayır
            )
            
            print(f"Successfully ingested {len(faqs)} FAQs for user {user_id}")
            return True
            
        except Exception as e:
            print(f"Error ingesting FAQs: {str(e)}")
            return False
    
    async def query(self, user_message: str, user_id: str) -> str:
        """
        Kullanıcı sorusunu işleyip çoklu dil desteğiyle yanıt verir
        
        Args:
            user_message: Kullanıcının sorusu
            user_id: Kullanıcı ID'si (namespace için)
            
        Returns:
            str: AI'dan gelen yanıt
        """
        try:
            # Development mode check
            if not self.llm or not self.embeddings or not self.index:
                print("⚠️ Running in development mode - query simulated")
                return f"Development mode: Received query '{user_message}' for user {user_id}. Please configure OpenAI and Pinecone API keys for full functionality."
            
            # 1. Kullanıcının dilini tespit et
            try:
                original_language = detect(user_message)
            except:
                original_language = "tr"  # Default Turkish
            
            # 2. Soruyu İngilizce'ye çevir (eğer İngilizce değilse)
            if original_language != "en":
                english_question = await self._translate_to_english(user_message)
            else:
                english_question = user_message
            
            # 3. Vektör store'u kullanarak ilgili SSS'leri bul
            vector_store = PineconeVectorStore(
                index=self.index,
                embedding=self.embeddings,
                namespace=user_id
            )
            
            retriever = vector_store.as_retriever(
                search_kwargs={"k": 3}  # En alakalı 3 dokümanı getir
            )
            
            # 4. RAG pipeline oluştur
            rag_prompt = ChatPromptTemplate.from_template("""
Aşağıdaki bağlamı kullanarak kullanıcının sorusuna cevap ver. 
Eğer bağlamda cevabı bulamazsan, "Bu konuda bilgim yok, lütfen daha spesifik bir soru sorun." şeklinde yanıtla.
Cevabını mümkün olduğunca doğal ve yardımcı bir tonda ver.

Bağlam:
{context}

Soru: {question}

Cevap:""")
            
            # RAG chain oluştur
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            rag_chain = (
                RunnableParallel({"context": retriever | format_docs, "question": RunnablePassthrough()})
                | rag_prompt
                | self.llm
                | StrOutputParser()
            )
            
            # 5. İngilizce cevabı al
            english_answer = rag_chain.invoke(english_question)
            
            # 6. Cevabı orijinal dile çevir (eğer gerekiyorsa)
            if original_language != "en":
                final_answer = await self._translate_to_language(english_answer, original_language)
            else:
                final_answer = english_answer
            
            return final_answer
            
        except Exception as e:
            print(f"Error in query: {str(e)}")
            return "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
    
    async def _translate_to_english(self, text: str) -> str:
        """Metni İngilizce'ye çevirir"""
        try:
            if not self.llm:
                return text
                
            translation_prompt = ChatPromptTemplate.from_template(
                "Translate the following text to English. Only return the translation, nothing else:\n\n{text}"
            )
            
            chain = translation_prompt | self.llm | StrOutputParser()
            return chain.invoke({"text": text})
            
        except Exception as e:
            print(f"Translation to English failed: {str(e)}")
            return text  # Çeviri başarısız ise orijinal metni döndür
    
    async def _translate_to_language(self, text: str, target_language: str) -> str:
        """Metni hedef dile çevirir"""
        try:
            if not self.llm:
                return text
                
            # Dil kodlarını tam isimlere çevir
            language_names = {
                "tr": "Turkish",
                "es": "Spanish", 
                "fr": "French",
                "de": "German",
                "it": "Italian",
                "pt": "Portuguese",
                "ru": "Russian",
                "ar": "Arabic",
                "zh": "Chinese",
                "ja": "Japanese",
                "ko": "Korean"
            }
            
            target_lang_name = language_names.get(target_language, target_language)
            
            translation_prompt = ChatPromptTemplate.from_template(
                f"Translate the following text to {target_lang_name}. Only return the translation, nothing else:\n\n{{text}}"
            )
            
            chain = translation_prompt | self.llm | StrOutputParser()
            return chain.invoke({"text": text})
            
        except Exception as e:
            print(f"Translation to {target_language} failed: {str(e)}")
            return text  # Çeviri başarısız ise orijinal metni döndür
