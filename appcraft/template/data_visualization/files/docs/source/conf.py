# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Adiciona o caminho da pasta lib ao sys.path
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Appcraft'
copyright = '2024, Dux Tecnologia'
author = 'Dux Tecnologia'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


# Função para garantir que os diretórios existam
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Função para gerar a lista de módulos recursivamente a partir de um diretório
def generate_module_list(directory):
    modules = []
    for root, dirs, files in os.walk(f"../../{directory}"):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':  # Ignora __init__.py
                # Converte o caminho do arquivo em formato de módulo Python
                module_name = os.path.join(root, file)
                module_name = module_name.replace('../../', '')  # Remove o prefixo '../../'
                module_name = module_name.replace('/', '.').replace('\\', '.')[:-3]
                modules.append(module_name)
    return modules


# Diretórios a serem documentados
directories_to_document = ['services', 'app', 'core']

# Gera e adiciona a documentação para todos os módulos nas pastas
output_dir = 'docs'
ensure_directory_exists(output_dir)

for directory in directories_to_document:
    # Gera a lista de módulos dentro de cada diretório
    modules_to_document = generate_module_list(directory)

    # Cria o conteúdo para o arquivo .rst dessa pasta
    autodoc_docstring = f"{directory.capitalize()} Module\n{'=' * (len(directory) + 7)}\n\n"
    autodoc_docstring += ".. toctree::\n   :maxdepth: 2\n\n"

    # Adiciona cada módulo dentro do arquivo .rst da pasta
    for module in modules_to_document:
        module_rst_filename = module.replace('.', '/')
        autodoc_docstring += f"   {module_rst_filename}\n"
        title = module.split('.')[-1].replace('_', ' ').capitalize()
        module_docstring = f"""
{title}
{'=' * len(title)}

.. automodule:: {module}
   :members:
   :undoc-members:
   :show-inheritance:
"""
        # Gera o arquivo .rst para cada módulo
        module_rst_path = os.path.join(output_dir, f"{module_rst_filename}.rst")
        ensure_directory_exists(os.path.dirname(module_rst_path))
        with open(module_rst_path, "w") as f:
            f.write(module_docstring)

    # Gera o arquivo principal .rst para a pasta
    directory_rst_path = os.path.join(output_dir, f"{directory}.rst")
    with open(directory_rst_path, "w") as f:
        f.write(autodoc_docstring)

print("Arquivos de documentação gerados com sucesso e adicionados ao toctree!")
