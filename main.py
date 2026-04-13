
from src import get_chunks, get_manual_content
from huggingface_hub import login
from dotenv import load_dotenv
import os
load_dotenv()
HF_TOKEN_KEY = os.getenv('HF_TOKEN')
login(token=HF_TOKEN_KEY)

manual = get_manual_content.Manual()

def prepare_the_environment(list_splitting_parameters_: list,
                            is_extract_chunks: bool = True,
                            convert_docx_to_doc=False,
                            remove_docx=False):

    if convert_docx_to_doc:
        manual.docx_to_doc()
    if is_extract_chunks:
        # List all directories in manuals_content, read all documents .doc and get chunck
        get_chunks.get_list_chunkers(list_splitting_parameters_)
    if remove_docx:
        manual.docx_remove()


if __name__ == '__main__':

    list_splitting_parameters = [
        500,
        1000,
        2000,
        4000,
        8000,
        'semantic'
    ]


    print(f'\n{"=" * 50} Running Experiments {"=" * 50}')

    prepare_the_environment(
        list_splitting_parameters_=list_splitting_parameters,
        is_extract_chunks=True,
        convert_docx_to_doc=False,
        remove_docx=False
    )
