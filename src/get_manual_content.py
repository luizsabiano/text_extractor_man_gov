import os
import re
import docx
import sys
import textract

from os import chdir, listdir
from os.path import isfile
from tqdm import tqdm
from src import directories

# Caso apareça o erro do operador  extract-msg<=0.29.*
# Use o pip versão 24.0 comando: pip install pip==24.0


# Lista todas as pastas em 1 nível a partir do diretório base
def list_dir(path):
    list_dirs = []
    # retorna uma lista contendo os nomes dos arquivos dentro do diretório fornecido
    for c in listdir(path):
        if not isfile(path + c):
            list_dirs.append(path + '/' + c)
    if not list_dirs:
        list_dirs.append(path)
    return list_dirs


# Lista todos os Manuais dentro das pastas do diretório base
def list_files(path):
    list_files_ = []
    list_dirs = list_dir(path)
    for dir_path in list_dirs:
        for c in listdir(dir_path):
            if isfile(dir_path + '/' + c):
                c_split = c.split('.')[0]
                list_files_.append((c_split, dir_path + '/' + c))
    return list_files_


class Manual:

    # Converte todos arquivos docx para doc
    def docx_to_doc(self):
        list_manuals = list_dir(directories.MANUAL_PATH)
        for manual in list_manuals:
            chdir(manual)
            for c in listdir():
                if isfile(c):
                    if c.split(".")[1] == 'docx':
                        print("Criado novo arquivo: ", manual + "/" + c)
                        doc = docx.Document(manual + "/" + c)
                        doc.save(manual + "/" + c.split(".")[0]+".doc")

    # Remove todos os arquivos docx
    def docx_remove(self):
        list_manuals = list_dir(directories.MANUAL_PATH)
        for manual in list_manuals:
            chdir(manual)
            for c in listdir():
                if isfile(c):
                    if c.split(".")[1] == 'docx':
                        os.remove(manual + '/' + c)

    # Acrescenta tabulação tripla caso o texto e expressão fornecida combinem
    def substituir(self, match):
        return "\t\t\t" + match.group(0)

    # Retorna o texto identado ou não.
    def trimmed(self, s: str, indented: bool = True):

        if indented:
            # para textos com formatação alinha as alínas a b c etc com três tabulações
            padrao = r'[a-z]\)'
            s = re.sub(padrao, self.substituir, s, flags=re.MULTILINE)
        else:
            # alinhas todos os quebras de linhas no inicio da linha
            while '  ' in s:
                s = s.replace('  ', ' ')
        return s

    # Extrai conteúdo de texto dos arquivos .doc
    def extract_content(self, manual_list):

        text = ""

        if manual_list[1].split('.')[1] == 'doc':
            text = textract.process(manual_list[1])

        text = text.decode('utf-8')

        # Exclui o texto abaixo inserido automaticamente
        # "convert /home/biano/gitHub/manuals_questions_generator/Manuais_Correios/MANDIS/mandis-modulo-02-capitulo-002_anexo-02.doc as
        # a Writer document -> /tmp/tmps6i3ysim/mandis-modulo-02-capitulo-002_anexo-02.txt using filter : Text"
        if ': Text\n\ufeff' in text:
            text = text.split(': Text\n\ufeff')[1]

        text = text.replace('\n\n', '\n')

        # Remove varios espaços em branco em cadeia ou identa
        text = self.trimmed(text, True)

        return manual_list[0], text

    # Lê lista diretórios e extrai texto de todos os manuais
    def get_all_content(self):

        lista = list_files(directories.MANUAL_PATH)

        content = []
        print()

        with tqdm(total=len(lista), file=sys.stdout, colour='blue', desc='\t\tReading documents') as pbar:

            for item in lista:

                try:
                    text = self.extract_content(item)
                except Exception as e:
                    print(f'\t\t\t{e}')
                    pbar.update(1)
                    continue

                content.append(text)

                pbar.update(1)

            return content


# manual = Manual()
# manual.docx_to_doc()
# manual.docx_remove()
