import argparse
import sys

from appcraft.utils.template_adder import TemplateAdder
from appcraft.utils.template_loader import TemplateLoader


def add_template():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(
        description="Initialize the project with specified templates."
    )

    # O primeiro argumento é o nome do script e será ignorado
    parser.add_argument(
        "templates",
        nargs="*",
        default=TemplateLoader().default_template_names,
        help="Names of the templates to add (default: base).",
    )

    # Analisa os argumentos
    args = parser.parse_args()

    # O primeiro argumento na lista de templates deve ser ignorado
    template_names = args.templates

    # Instanciar a classe TemplateAdder com os
    # nomes dos templates fornecidos pelo usuário
    template_adder = TemplateAdder()

    try:
        # Adicionar os templates com base nos nomes fornecidos
        for template in template_names:
            template_adder.add_template(template)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
