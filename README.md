# ManGov_text_extractor
Extrai texto dos manuais normativos governamentais e persiste no banco de dados vetorial


# <p style="text-align:center;"> Ferramenta de extração e fragmentação de texto em manuais normativos governamentais</p> 

---
## Resumo do utilitário

<p style="text-align:justify;">

Utilitário de extração e fragmentação contruído para, a partir do diretório raiz, ler os arquivos armazenados dentro do diretório "data/manuals_content", extrair o conteúdo destes arquivos e fragmentá-los. Após a fragmentação, os fragmentos extraído são persistidos em arquivos Json com o nome chunk_list_comprimento-do-fragmento.json.

Com o objetivo de excluir anexos, fluxogramas, tabelas e figuras, bem como conteúdos de baixa densidade informacional, implementou-se um filtro com
base na quantidade de palavras que compunham o documento. Desta forma, apenas
arquivos contendo uma quantidade de texto igual ou superior a 1000 palavras (tokens)
foram selecionados para compor o corpus final. Este valor pode ser modificado alterando a varíavel "min_tokens_per_docs" em src/get_chunks.py.


Subsequentemente, todos os documentos selecionados foram submetidos ao processo de
fragmentação em blocos de texto (chunking), sendo divididos em segmentos de 3500
caracteres. Para preservar a continuidade semântica entre os blocos e mitigar a perda
de contexto nas extremidades, foi aplicada uma sobreposição (overlap) de 350 caracteres
entre os blocos consecutivos. Esta configuração de sobreposição visa garantir a integridade
da informação e a coesão semântica para a posterior recuperação de informações. Para
garantir a rastreabilidade e evitar a perda de informações decorrentes de falhas no fluxo,
todos os chunks gerados foram persistidos em um único arquivo JSON dentro do diretório "chunks". 
O arquivo JSON foi estruturado conforme a seguir: id (identificação crescente), source (fonte) e chunks (lista contendo os fragmentos).
Essa medida de backup preserva a totalidade do conteúdo fragmentado, mantendo a informação de qual
manual cada chunk foi derivado.

</p>

Autores: Luiz Sabiano F. Medeiros


## Estrutura de diretórios


<pre>├── <font color="#12488B"><b>data</b></font>
│   ├── <font color="#12488B"><b>chunks</b></font> <font color="#7B68EE"> => Armazena os fragmentos salvos em Json</font>
│   ├── <font color="#12488B"><b>manuals_content</b></font> <font color="#7B68EE"> => Armazena os manuais a serem extraídos e fragmentados</font>
├── <font color="#12488B"><b>src</b></font>
│   ├── directories.py <font color="#7B68EE"> => Arquivo de caminhos (PATHs)</font>
│   ├── embedding_model.py <font color="#7B68EE"> => Configura modelo de embeddings</font>
│   ├── get_chunks.py <font color="#7B68EE"> => Recebe o conteúdo extraído e o fragmenta</font>
│   ├── get_manual_content.py <font color="#7B68EE"> => Extrai o conteúdo armazenado em manuals_conten</font>
│   ├── tools.py  <font color="#7B68EE"> => funções de apoio</font>
├── README.md
└── requirements.txt <font color="#7B68EE">O arquivo de requisitos para reproduzir os experimentos</font>
</pre>


### Instalação das dependências: 

$ pip install pip==24.0

$ pip install -r requirements.txt



## Execução 
Antes da execução crie um arquivo .env com a variável HF_TOKEN="sua chave do Hugging Face".

Execute o arquivo main.py.

## Configuração 

1) list_splitting_parameters: Lista de parâmetros que configura o tamanho dos fragmentos
2) is_extract_chunks: Se True, realiza a extração e fragmentação dos documentos
3) convert_docx_to_doc: Se True, recebe documentos docx e converte para doc (necessário pois o extrator só trabalha com doc)
4) remove_docx: Se True, remove os arquivos docx (só use depois da conversão para doc).

 
Necessário GPU Nvidia.
