from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = Field(default="Bank Mandiri Multimodal RAG", alias="APP_NAME")

    upload_dir: str = Field(default="data/uploads", alias="UPLOAD_DIR")
    chroma_dir: str = Field(default="data/chroma", alias="CHROMA_DIR")
    extracted_image_dir: str = Field(default="data/extracted_images", alias="EXTRACTED_IMAGE_DIR")

    collection_name: str = Field(default="bank_mandiri_2025", alias="COLLECTION_NAME")

    use_local_model: bool = Field(default=True, alias="USE_LOCAL_MODEL")
    ollama_llm_model: str = Field(default="llama3.2", alias="OLLAMA_LLM_MODEL")
    ollama_embedding_model: str = Field(default="nomic-embed-text", alias="OLLAMA_EMBEDDING_MODEL")

    class Config:
        extra = "ignore"


settings = Settings()

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
Path(settings.extracted_image_dir).mkdir(parents=True, exist_ok=True)