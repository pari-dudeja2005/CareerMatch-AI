from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text):
    """
    Convert a single text into a semantic vector.
    """

    return model.encode(
        text,
        normalize_embeddings=True
    )


def generate_embeddings(texts):
    """
    Convert multiple texts into semantic vectors.
    """

    return model.encode(
        texts,
        normalize_embeddings=True
    )