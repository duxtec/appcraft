# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Appcraft'
copyright = '2025, Dux Tecnologia, Thiago Costa Pereira'
author = 'Dux Tecnologia, Thiago Costa Pereira'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme"
]

html_theme_options = {
    "navigation_depth": 4,  # Profundidade da árvore de navegação
    "collapse_navigation": False,  # Não colapsar a navegação lateral
    "titles_only": False  # Mostrar a hierarquia completa
}

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
