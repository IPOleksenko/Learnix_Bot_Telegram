from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

# Initialize the model once at module level
_model = None

def get_model():
    """Get or initialize the SentenceTransformer model"""
    global _model
    if _model is None:
        _model = SentenceTransformer("BAAI/bge-m3")
    return _model

async def merge_plans(plans: List[Dict]) -> Dict:
    if not plans:
        return {}
    
    if len(plans) == 1:
        return plans[0].get("plan", {})
    
    model = get_model()
    
    # Extract all topics from all plans
    all_topics = []
    plan_sources = []  # Track which plan each topic comes from
    
    for plan_dict in plans:
        plan = plan_dict.get("plan", {})
        for name, desc in plan.items():
            all_topics.append(desc)
            plan_sources.append(name)
    
    if not all_topics:
        return {}
    
    # Encode all topics
    embeddings = model.encode(all_topics)
    
    # Cluster similar topics
    clusters = []
    SEMANTIC_THRESHOLD = 0.65
    
    for topic, emb in zip(all_topics, embeddings):
        added = False
        for cluster in clusters:
            # Check against the first topic's embedding
            saved_emb = cluster[0][1]
            sim = cosine_similarity([emb], [saved_emb])[0][0]
            if sim > SEMANTIC_THRESHOLD:
                cluster.append((topic, emb))
                added = True
                break
        if not added:
            clusters.append([(topic, emb)])
    
    # Get the best topic from each cluster (longest one as most descriptive)
    final_topics = [max(cluster, key=lambda x: len(x[0]))[0] for cluster in clusters]
    
    # Create merged plan dictionary
    merged_plan = {
        f"lesson_{i+1}": topic
        for i, topic in enumerate(final_topics)
    }
    
    return merged_plan
