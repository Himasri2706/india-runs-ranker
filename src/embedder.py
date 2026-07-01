import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CandidateEmbedder:
    def __init__(self):
        # Load from cache directory
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
        if not os.path.exists(cache_dir):
            raise RuntimeError(f"Model cache not found at {cache_dir}. Run download_model.py first.")
            
        self.model = SentenceTransformer(cache_dir)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dim)
        self.jd_text = None
        self.jd_embedding = None

    def set_jd(self, jd_text):
        """Embeds the Job Description and normalizes it."""
        self.jd_text = jd_text
        emb = self.model.encode([jd_text], convert_to_numpy=True)
        faiss.normalize_L2(emb)
        self.jd_embedding = emb[0]

    def embed_and_score_batch(self, texts):
        """
        Embeds a batch of candidate texts using a Two-Tower Hybrid Approach:
        - 70% Dense Score (Semantic Meaning via SentenceTransformers)
        - 30% Sparse Score (Exact Keyword Matching via TF-IDF)
        """
        if self.jd_embedding is None or self.jd_text is None:
            raise ValueError("JD not set. Call set_jd() first.")
            
        if not texts:
            return []
            
        # --- 1. Dense Scoring (Semantic) ---
        embs = self.model.encode(texts, convert_to_numpy=True)
        faiss.normalize_L2(embs)
        dense_scores = np.dot(embs, self.jd_embedding)
        dense_normalized = (dense_scores + 1.0) / 2.0
        
        # --- 2. Sparse Scoring (Exact Keywords) ---
        vectorizer = TfidfVectorizer(stop_words='english')
        # Fit on JD and current batch to find overlapping vocabulary importance
        tfidf_matrix = vectorizer.fit_transform([self.jd_text] + texts)
        
        # Element 0 is JD, Elements 1..N are candidates
        jd_sparse_vec = tfidf_matrix[0:1]
        cand_sparse_vecs = tfidf_matrix[1:]
        
        sparse_scores = cosine_similarity(cand_sparse_vecs, jd_sparse_vec).flatten()
        
        # --- 3. Hybrid Blending ---
        hybrid_scores = (0.7 * dense_normalized) + (0.3 * sparse_scores)
        
        return hybrid_scores.tolist()
