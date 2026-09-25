.. _contributing:

Contributing
============

We appreciate your interest in contributing! You can contribute in three ways:

1. `Creating New Templates <#id2>`_.
2. `Updating Existing Templates <#id3>`_.
3. `Translating Templates <#id5>`_.

Creating New Templates
----------------------

To create a new template, follow these steps:

1️⃣ **Clone the repository**:
    .. code-block:: bash

        git clone https://github.com/duxtec/appcraft.git

2️⃣ **Navigate to the repository folder**:
    .. code-block:: bash

        cd appcraft

3️⃣ **Run the command to create a new template**:
    .. code-block:: bash

        python appcraft/utils/template_creator.py <template_name>
   
   This command will generate a new folder:
   ```
   appcraft/templates/<template_name>/
   ```

4️⃣ **Inside this folder, update the `__init__.py` file**:
    - Add a `description` to describe the template.
    - Activate the template by setting the class constant:
        .. code-block:: bash

            active = True

    - The `files/` folder inside contains the template's core files.

5️⃣ **Develop or Edit the Template Using a Temporary Project**
    It is **not recommended** to edit templates directly inside the `appcraft/templates/<template_name>` folder. This approach has several limitations:

    **Why?**
        - **Dependency Issues**: Templates often depend on a base template or other templates, which are not recognized properly when editing them in isolation.
        - **Linting Problems**: Linters and IDEs may fail to detect dependencies, leading to false errors and a poor development experience.
        - **Risk of Breaking the Template Structure**: Direct modifications may lead to inconsistencies or missing files.
    
    **Solution: Use a Temporary Project**
    To safely develop or edit a template, it is best to use a **Temporary Project**. This allows you to work inside a fully functional AppCraft-generated project, where all dependencies, configurations, and integrations work correctly.

    Instructions for creating a temporary project can be found here: `Working in a temporary project <#id5>`_.


6️⃣ **Submit a pull request with the new template**!


Updating Existing Templates
-----------------------------

Updating an existing template follows the same process as creating a new one.  
Simply **skip steps 3 and 4** and proceed with the rest of the instructions.  

For detailed steps, refer to `Creating New Templates <#id2>`_.


Translating Templates
----------------------

To translate templates into another language:

1️⃣ **Identify the template to translate**.

2️⃣ **Create a new language folder inside the template**:

   .. code-block:: bash

      appcraft/templates/<template_name>/other_files/locale/
      ├── en/  # English
      ├── pt/  # Portuguese
      ├── es/  # Spanish


3️⃣ **Translate relevant files** while maintaining consistency.

4️⃣ **Create a new demo project and test the translation**.

5️⃣ **Submit a pull request with the translated version**.

Why Use a Temporary Project?
----------------------------

When working with templates, you might be tempted to edit them directly inside the `appcraft/templates/` folder. However, this approach has several drawbacks:

- **Dependency Issues:** Templates often depend on a base template or other templates, which are not recognized properly when editing them in isolation.
- **Linting Problems:** Linters and IDEs may fail to recognize dependencies, leading to false errors and a poor development experience.
- **Risk of Breaking the Template Structure:** Direct modifications inside `appcraft/templates/` may lead to inconsistencies or missing files in the final template.

To avoid these issues, **the recommended approach is to use a Temporary Project**, which allows you to develop templates inside a fully functional AppCraft-generated project. This ensures that all dependencies, configurations, and integrations work correctly before saving the template.


Working in a temporary project
-------------------------------

**To work in a temporary project:**
    
1. **Uninstall AppCraft (if installed)**:
    .. code-block:: bash
        
        pip uninstall appcraft

2. **Navigate to the cloned AppCraft repository**:
    .. code-block:: bash
        
        cd appcraft
            
3. **Install the local version**:
    .. code-block:: bash
        
        pip install -e .

4. **Create a new project**:
    .. code-block:: bash
        
        appcraft init <template_name> [dependencies]
        
    Replace `<template_name>` with the template you're working on and specify any additional dependencies.
    
    **The temporary project will be created in**:
    ```
    appcraft/templates/temp/
    ```
    
    This project mirrors an AppCraft-initialized project, allowing safe editing.

5. **After modifying or creating files in the temporary project, save the template**:
    .. code-block:: bash

        python appcraft/utils/template_saver.py <template_name>

    **Modify only one template at a time**.
    
    If you need to modify another template, **save the current template first**, then repeat the process starting from `appcraft init`.


Ready to Contribute?
--------------------

If you have any questions, feel free to open an issue or reach out to the maintainers.

🚀 Happy Coding!