from src.embeddings import generate_embedding


text = "building machine learning models"

embedding = generate_embedding(text)


print("\nEmbedding generated successfully!")

print("Vector dimensions:", len(embedding))

print("First 10 values:")
print(embedding[:10])