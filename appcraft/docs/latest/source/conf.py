from pathlib import Path

import toml

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Appcraft'
copyright = '2025, Dux Tecnologia, Thiago Costa Pereira'
author = 'Dux Tecnologia, Thiago Costa Pereira'

conf_path = Path(__file__).resolve()
release_dir = conf_path.parents[1].name

if release_dir == "latest":
    pyproject_path = conf_path.parents[4] / "pyproject.toml"

    if pyproject_path.exists():
        pyproject_data = toml.load(pyproject_path)
        release = pyproject_data.get("project", {}).get("version", "unknown")
    else:
        release = "unknown"
else:
    release = release_dir


extlinks = {
    'latestversion': (
        '../../latest/index%shtml',
        f'Latest Version ({release})%s',
    )
}


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_rtd_theme", "sphinx.ext.extlinks"]

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "titles_only": False,
}

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

latex_engine = 'lualatex'
latex_theme = 'howto'

latex_elements = {
    "preamble": r"""
    \usepackage{commonunicode}
    \directlua {
        luaotfload.add_fallback("emoji",
        {
            "[NotoColorEmoji-Regular.ttf]:mode=harf;",
            "[TwemojiMozilla.ttf]:mode=harf;",
            "[DejaVuSans.ttf]:mode=harf;",
        })
    }
    \setmainfont{NotoSans}[
        RawFeature={fallback=emoji},
    ]
    \setsansfont{NotoSans}[RawFeature={fallback=emoji}]
    \setmonofont{DejaVuSansMono}[RawFeature={fallback=emoji},Scale=0.8]
    """,
}
