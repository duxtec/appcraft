import os
import sys

appcraft_root_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)))
)

base_template_path = os.path.join(
    appcraft_root_path, "appcraft", "templates", "base", "files"
)

sys.path.append(appcraft_root_path)
sys.path.append(base_template_path)
