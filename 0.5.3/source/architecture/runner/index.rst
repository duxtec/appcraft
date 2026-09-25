Runner Layer
====================
Runners are the entry points of the application. It initiates the process and calls the **Presentation** layer or **Service** layer.

Aqui está uma seção **"What to Do in Runners"** no mesmo formato das outras:

What to Do in Runners
-------------------------

    - **Bootstrap the Application**:
        The Runner is responsible for initializing the entire application. It should set up dependencies, load configurations, and start necessary services before the application starts handling requests.  
        
    - **Wire Up Dependencies**:
        Ensure that dependencies, such as repositories, services, and infrastructure components, are instantiated and injected properly. This avoids tight coupling and ensures dependency inversion is respected.  

    - **Load Environment Variables and Configurations**:
        The Runner should read and apply configuration settings from environment variables, configuration files, or a settings module to ensure flexibility and separation of concerns.  

    - **Register Application Components**:
        All necessary components, such as repositories, services, and external integrations, should be properly registered and made available to the application.  

    - **Handle Application Lifecycle Management**:
        Ensure proper shutdown procedures are in place, such as closing database connections, stopping background jobs, and releasing resources when the application stops.  

    - **Integrate Logging and Monitoring**:
        Set up logging configurations and monitoring tools to track application performance and diagnose issues effectively.  

What to Avoid in Runners
--------------------------
While creating runners in the AppCraft framework, it's important to follow best practices to ensure the runners remain clean and focused on their intended purpose. Here are some things to avoid:

    - **Avoid Using Print Statements for Debugging**: 
        Runners should not be used for logging or debugging purposes, such as using `print()` statements. Print statements should be used in the Presentation layer when interacting with the user or displaying output. Logging, on the other hand, should be handled in the Service layer for better management and traceability of events.

    - **Avoid Performing Complex Actions in Runners**:
        Runners should only handle the orchestration of tasks, such as calling the appropriate methods from the Presentation or Service layers. Avoid placing complex business logic, lengthy computations, or time-consuming actions directly in the runner methods.
        For example, avoid making database queries, handling large data processing, or interacting with external systems directly inside the runner. This should be delegated to services or other components that can handle the workload asynchronously or in a more appropriate place.


Types of runners
-----------------
In the AppCraft framework, there are two types of runners:

    1. **Main Runners**:
        These are the primary entry points of the application. They are located in the `runners/main` directory. These scripts are typically used for the main execution flow of the application.

    2. **Auxiliary/Secondary Runners**:
        These runners serve secondary tasks and are located in the `runners/tools` directory. These scripts are typically used for secundary tasks that are not the main execution flow of the application.


To define a class as a runner, it must meet the following conditions:

    - The class must be located in either `runners/main` or `runners/tools`.
    
    - The class must inherit from `AppRunner`.
    
    - The methods that are designated as runners should be decorated with the `@AppRunner.runner` decorator.


Example of a Runner
-----------------------
Here is an example of how to define a runner:

.. code-block:: python
    
    from application.services.app_service import AppService
    from infrastructure.framework.appcraft.core.app_runner import AppRunner
    from infrastructure.memory.adapters.app_adapter import AppAdapter
    from presentation.cli.app_cli_presentation import AppCLIPresentation


    class AppRunner(AppRunner):
        @AppRunner.runner
        def start(self):
            app_adapter = AppAdapter()
            app_service = AppService(app_adapter=app_adapter)
            presentation = AppCLIPresentation(app_service=app_service)
            presentation.start()

        def non_runner1(self):
            # This method does not show in the runner.
            pass


Running Applications
-------------------------
To execute the **Main runners** within your project, use:

.. code-block:: bash

    python run

This command will run the **main runner** of your project that are located in the `runners/main` folder.

If there are **multiple main runners**, you will be prompted to select the desired **filename, class, and method** in the `runners/main` directory.

If you want to know how to **execute a specific runner**, refer to the section `Executing a Specific Runner <#id2>`_.

Running Auxiliary Runner
--------------------------------

To execute **Auxiliary Runner** in your project, use:

.. code-block:: bash

    python run_tools

This command will run the **auxiliary runner** of your project that are located in the `runners/tools` folder.

If there are **multiple auxiliary runners**, you will be prompted to select the desired **filename, class, and method** in the `runners/tools` directory.

If you want to know how to **execute a specific runner**, refer to the section `Executing a Specific Runner <#id2>`_.

Executing a Specific Runner
----------------------------------

If you want to execute a specific runner, you can use the following command:

.. code-block:: bash
    
    python run file_name class_name method_name

- `file_name`: The name of the file containing the class runner.
- `class_name`: The name of the class runner.
- `method_name`: The name of the method within the class runner that you want to run.

If the class contains only one method, you can omit the `method_name`:

.. code-block:: bash

    python run file_name class_name

If the file contains only one class, you can omit the `class_name`:

.. code-block:: bash

    python run file_name method_name

Alternatively, if the file has only one class and one method, both can be omitted, and the runner will be selected automatically:

.. code-block:: bash

    python run file_name

Or, if there is only one file in the project, you can omit the `file_name` entirely:

.. code-block:: bash

    python run class_name method_name

If there is only one file and one class, you can also omit the `method_name`:

.. code-block:: bash

    python run class_name

Finally, if there is only one file, one class, and one method, you can simply use:

.. code-block:: bash

    python run method_name

Or, if everything is automatically determined (only one file, one class, and one method), you can just run:

.. code-block:: bash

    python run

This system allows for flexible execution of your runners, making it easier to manage the different entry points in your project. You can target specific files, classes, or methods directly, depending on your needs.

