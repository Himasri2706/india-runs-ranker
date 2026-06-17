import os
from sentence_transformers import SentenceTransformer

def download_model():
    print("Downloading and caching all-MiniLM-L6-v2 model...")
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Load model and save it to the cache directory
    model_name = "all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)
    model.save(cache_dir)
    print(f"Model saved successfully to {cache_dir}")

if __name__ == "__main__":
    download_model()
