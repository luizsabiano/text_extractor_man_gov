import os
import json
import spacy
import sys

from langchain_text_splitters import TokenTextSplitter
from tqdm import tqdm
from src import directories
from src.embedding_model import get_hf_embedding
from src.get_manual_content import Manual
from langchain_experimental.text_splitter import SemanticChunker


nlp = spacy.load(name='pt_core_news_sm', disable=['ner'])

OVERLAP_PERCENT = 10

min_tokens_per_docs = 1000

base_dir = directories.CHUNKS_PATH


# Conta e retorna quantidade de tokens do texto fornecido.
def compute_total_tokens(text) -> int:
    token_size = 0
    doc = nlp(text)
    token_size += len([token.orth_ for token in doc])
    return token_size


# Retorna chunks da sentença fornecida
def langchain_chunker(sentences, lengthc=2300, overlap=230):
    text_splitter = TokenTextSplitter(
        chunk_size=lengthc,
        chunk_overlap=overlap,
    )
    return text_splitter.split_text(sentences)


# Retorna uma lista de chunks a partir dos documentos fornecidos
# Os chunks são salvos no formato dicionário
def get_chunks(documents, lenghtc):

    chunks = []

    id_ = 1

    overlap = int((lenghtc * OVERLAP_PERCENT) / 100)

    print()
    with tqdm(total=len(documents), file=sys.stdout, colour='blue',
              desc='\t\t\t  Splitting documents in chuncks') as pbar:
        for document in documents:

            chunks.append(
                {
                    'id': id_,
                    'source': document[0].upper(),
                    'chunks': langchain_chunker(document[1], lenghtc, overlap)
                }
            )
            id_ = id_ + 1
            pbar.update(1)
        # total = sum([len(chunk['chunks']) for chunk in chunks])
        # print("")
        # print("Total de chunks: ", total)
        # print("")
    return chunks


# Retorna uma lista de chunks  a partir dos documentos fornecidos
# Os chunks são salvos no formato dicionário
def get_semantic_chunk(documents):

    # HuggingFace embeddings setup
    embeddings = get_hf_embedding()

    # Using HuggingFace embeddings with SemanticChunker
    text_splitter = SemanticChunker(embeddings)

    chunks_list = []

    id_ = 1

    print()

    with tqdm(total=len(documents), file=sys.stdout, colour='blue',
              desc='\t\t\t  Splitting documents in chuncks') as pbar:
        for document in documents:
            texts = text_splitter.create_documents(document)
            chunks = [chunk.page_content for chunk in texts]
            chunks.pop(0)
            chunks_list.append({'id': id_, 'source': document[0].upper(), 'chunks': chunks})
            id_ = id_ + 1
            pbar.update(1)
    return chunks_list


# Recebe uma lista de chunks, converte para JSON e salva em arquivo local
def chunks_to_json(chunks, lenghtc):

    os.makedirs(base_dir, exist_ok=True)

    # Caminho para o arquivo onde salvar
    file_path = base_dir + 'chunk_list_' + lenghtc + '.json'

    # Abre o arquivo em modo escrita ('w') e salva a lista no formato JSON
    with open(file=file_path, mode='w') as json_file:
        json.dump(chunks, json_file, ensure_ascii=False, indent=4)  # indent=4 para formatar o JSON com 4 espaços

    # print("Chunks saved in ", file_path)


# lista de conteúdos disponíveis na pasta Manuals_Content
# só utiliza o conteúdo de documentos que possuam a quantidade de tokens superior a min_tokens.
def get_list_chunkers(list_splitting_parameters):

    manual = Manual()

    documents_list = []

    manuals_content = manual.get_all_content()

    with tqdm(total=len(manuals_content), file=sys.stdout, colour='blue',
              desc='\t\tTriando documentos') as pbar:
        for manual_content in manuals_content:
            tokens = compute_total_tokens(manual_content[1])
            if tokens >= min_tokens_per_docs:
                documents_list.append(manual_content)
            pbar.update(1)

    del manuals_content

    for splitting_parameter in list_splitting_parameters:

        print(f'\n\t\tSplitting Parameter: {splitting_parameter}')

        if splitting_parameter != 'semantic':
            chunks = get_chunks(documents_list, splitting_parameter)
            chunks_to_json(chunks, str(splitting_parameter))
        else:
            chunks = get_semantic_chunk(documents_list)
            chunks_to_json(chunks, str(splitting_parameter))

    os.chdir(base_dir)
