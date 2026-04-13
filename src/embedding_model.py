from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODELS = {
        'ef': 'LocalHuggingFaceEmbeddingFunction',
        'name': 'multilingual_e5_large',
        'model': 'intfloat/multilingual-e5-large',
        'normalize_embeddings': False
    }



def get_hf_embedding():
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODELS['model'],
        model_kwargs={'device': 'cuda'},
        encode_kwargs={'normalize_embeddings': False},
    )
    return hf_embeddings
