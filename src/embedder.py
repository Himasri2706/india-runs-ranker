import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class CandidateEmbedder:
    def __init__(self):
        # Load from cache directory
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
        if not os.path.exists(cache_dir):
            raise RuntimeError(f"Model cache not found at {cache_dir}. Run download_model.py first.")
            
        self.model = SentenceTransformer(cache_dir)
        # Using Inner Product since sentence embeddings are usually normalized
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dim)
        self.jd_embedding = None

    def set_jd(self, jd_text):
        """Embeds the Job Description and normalizes it."""
        emb = self.model.encode([jd_text], convert_to_numpy=True)
        faiss.normalize_L2(emb)
        self.jd_embedding = emb[0]

    def embed_and_score_batch(self, texts):
        """
        Embeds a batch of candidate texts, normalizes them, and computes cosine similarity with JD.
        Returns a list of semantic scores (0-1).
        """
        if self.jd_embedding is None:
            raise ValueError("JD not set. Call set_jd() first.")
            
        if not texts:
            return []
            
        embs = self.model.encode(texts, convert_to_numpy=True)
        faiss.normalize_L2(embs)
        
        # Compute cosine similarity: dot product of normalized vectors
        # embs shape: (batch_size, dim), jd_embedding shape: (dim,)
        scores = np.dot(embs, self.jd_embedding)
        
        # Ensure scores are between 0 and 1
        # Inner product of L2 normalized vectors gives cosine similarity in [-1, 1]
        # We can map [-1, 1] to [0, 1] using (score + 1) / 2
        normalized_scores = (scores + 1.0) / 2.0
        
        return normalized_scores.tolist()
