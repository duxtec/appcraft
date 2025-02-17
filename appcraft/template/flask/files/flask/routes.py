from flask import Blueprint, render_template, abort
from core.managers.import_manager import ImportManager
import os
import inspect
import pkgutil

page_bp = Blueprint('pages', __name__, template_folder='../../app')

def register_views(blueprint, views):
    if 'index' in views:
        blueprint.add_url_rule('/', view_func=views["index"])

    # Itera sobre as views e registra as que são funções no blueprint
    
    for name, view in views.items():

        if inspect.isfunction(view):

            url_rule = f'/{name}'
            blueprint.add_url_rule(url_rule, view_func=view, methods=['GET', 'POST'])

im = ImportManager("app.pages")

for _, module_name, _ in pkgutil.iter_modules(["app/pages"]):
    views = im.get_module_attributes(f'.{module_name}')
    register_views(page_bp, views)



# Rota combinada para páginas dinâmicas e estáticas
@page_bp.route('/<page>')
@page_bp.route('/')
def serve_page(page = "index"):
    if page is None or page == "":
        page = "index"

    # Verifica se a página está entre as views dinâmicas
    if page in views:
        return views[page]()
    else:
        return serve_static_page(page)

def serve_static_page(page = None):
    static_page_path = os.path.join('app', 'pages', 'static', f"{page}.html")
    if os.path.exists(static_page_path):
        return render_template(f"static/{page}.html")
    
    page404_path = os.path.join('app', 'pages', 'static', "404.html")
    if os.path.exists(page404_path):
        return render_template("pages/static/404.html"), 404

    # Se nem dinâmica nem estática existirem, retorna erro 404
    abort(404)