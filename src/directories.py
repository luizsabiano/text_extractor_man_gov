from os import getcwd, path, makedirs

# Obtém diretório base
base_dir = getcwd()

MANUAL_PATH = base_dir + '/data/manuals_content/'
makedirs(MANUAL_PATH, exist_ok=True)
CHUNKS_PATH = base_dir + '/data/chunks/'
makedirs(CHUNKS_PATH, exist_ok=True)

