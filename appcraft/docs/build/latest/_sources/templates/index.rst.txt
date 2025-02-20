Templates
=================
In AppCraft, templates define the foundation of a **layered architecture**, ensuring modularity and independence. Each template provides a specific set of features that seamlessly integrate into a project.

All templates are **modular and independent**, allowing them to be combined as needed, making project construction **flexible and scalable**. Whether you require **logging, localization, web interfaces, or API handling**, you can mix and match templates without compromising the core structure of your application.

By leveraging AppCraft's template-based system, developers can streamline development while maintaining a **clean and maintainable architecture**.

.. toctree::
   :maxdepth: 2
   :caption: Templates
   :titlesonly:
   
   base/index
   logs/index
   locales/index
   flask_ui/index
   flask_api/index
   web_scraping/index

.. rubric:: Base Template

The **Base Template** is the foundational template of the framework, providing the backbone for the project's architecture in layers. It serves as the starting point for any application using the framework, offering a solid foundation and essential functionalities for efficient project management.

The Base Template includes the following features:

- **Simplified Management and Execution of EntryPoints**: The Base Template facilitates the setup and execution of various entry points in your project, allowing you to define and organize the core functions of your application.

- **Automatic Management and Installation of Missing Dependencies**: The template automatically handles the installation of dependencies, ensuring that your project has everything it needs to run correctly without requiring manual setup.

- **Error Handler**: It includes a robust error handling mechanism, allowing you to capture and manage exceptions appropriately, ensuring the stability and integrity of the system.

- **CLI UI Theme**: The Base Template includes a user interface theme for the CLI, providing a visually organized and consistent way to interact with the system, improving the user experience.

- **Customizable Message Printer**: The template offers a system for printing custom messages, allowing you to display different types of messages (such as success, warning, error, critical, title, and info) in a clear and formatted way, making communication with users easier during execution.

With these features, the Base Template establishes a solid and easy-to-use foundation for building and expanding projects, keeping them organized while offering great control over dependencies and user interaction.

For more information about this template, you can check the dedicated page: `Base Template Documentation <base/index.html>`_.

.. rubric:: Logs

The **Logs Template** provides a structured logging system that enhances error tracking and debugging capabilities. It includes **log rotation**, configurable **logging levels**, and multiple output formats to ensure all application logs are properly stored and organized.  

This template features a **customized Logger** that automatically saves logs in **time-organized files**, making it easier to locate specific entries. In **debug mode**, it leverages the libs **structlog, better-exceptions, and rich** to improve log readability in the terminal.  

Seamlessly integrated into the **Core** of the framework, the logging system operates **automatically**, requiring no additional imports or manual configuration, ensuring a smooth developer experience.

For more information about this template, you can check the dedicated page: `Logs Template Documentation <logs/index.html>`_.

.. rubric:: Locales

The **Locales Template** provides a **built-in internationalization (i18n) system** for managing multilingual support in applications. It automatically handles **language detection, message translation, and formatted output**, ensuring seamless adaptation to different locales.  

At its core, the **MessageManager** class manages **gettext-based translations**, loading the preferred language dynamically based on system settings or user configuration. It supports **.po and .mo files**, automatically compiling translation files when necessary.  

This template also enhances **CLI interactions** by intercepting the standard print function, ensuring that messages are automatically translated before being displayed. Integrated directly into the framework’s **Core**, the **Locales Template** requires no additional setup, providing a modular and efficient solution for multilingual applications.

For more information about this template, you can check the dedicated page: `Locales Template Documentation <locales/index.html>`_.

.. rubric:: Flask UI

The **Flask UI Template** provides an integrated **FlaskApp** that can function independently or in combination with the **Flask API** and **SQLAlchemy** templates if installed. It ensures a seamless integration within a **layered architecture**, maintaining modularity and flexibility in web application development.  

This template introduces a well-structured **presentation layer** for UI endpoints under `presentation/web/ui`, offering built-in support and examples for constructing **Web UIs** efficiently.. It automatically sets up a **Flask application**, configures **routing** for **dynamic views, static views, and assets** and includes **error handling** for missing routes.  

Additionally, if the **SQLAlchemy Template** is installed, the **Flask UI Template** will attempt to initialize the database connection, providing built-in support for ORM-based persistence. Otherwise, it gracefully operates without database integration, ensuring versatility in different application setups.

For more information about this template, you can check the dedicated page: `Flask UI Template Documentation <flask_ui/index.html>`_.

.. rubric:: Flask API

The **Flask API Template** provides an integrated **FlaskApp** that can function independently or in combination with the **Flask API** and **SQLAlchemy** templates if installed. It ensures a seamless integration within a **layered architecture**, maintaining modularity and flexibility in web application development.

This template introduces a well-structured **presentation layer** for API endpoints under `presentation/web/api/v1`, offering built-in support and examples for constructing **RESTful APIs** efficiently.. It automatically sets up a **Flask application**, configures **routing** for **APIs** and includes **error handling** for missing routes.  

This template is designed to manage **APIs**, offering built-in support and examples for constructing **RESTful APIs** efficiently. It automatically sets up a **Flask application**, configures **routing** and includes **error handling** for missing routes. 

This template includes essential **API dependencies**, such as:

- **flask-login** (user authentication)  

- **flask-restful** (simplified API routing)  

- **flask-cors** (cross-origin resource sharing)  

- **flask-compress** (response compression)  

Additionally, if the **SQLAlchemy Template** is installed, the **Flask API Template** will attempt to initialize the database connection, providing built-in support for ORM-based persistence. Otherwise, it gracefully operates without database integration, ensuring versatility in different application setups.

For more information about this template, you can check the dedicated page: `Flask API Template Documentation <flask_api/index.html>`_.

.. rubric:: Web Scrapping

The **Web Scraping Template** provides a structured environment for efficiently extracting data from websites. It includes **pre-configured scripts** and essential libraries for handling web requests, parsing HTML, and automating interactions with web pages.  

- **Key Features**

   - **Multiple Web Scraping Adapters:** The template includes an **adapter for each scraping library**, allowing flexibility in choosing the best approach for different use cases.  

   - **Standardized Architecture:** It provides an **abstract base class** for web scraping adapters, ensuring a **consistent and reusable** structure across different implementations.  

   - **Service Demonstrations:** It includes examples of **data extraction and storage services**, showcasing best practices for handling scraped data.  

- **Included Dependencies**  

   This template integrates powerful web scraping tools, such as:  

   - **browser_manager** (headless browser management)  

   - **scrapy** (high-level web scraping framework)  

   - **selenium** (browser automation)  

   - **requests & requests-html** (HTTP requests and dynamic content rendering)  

   - **beautifulsoup4, lxml, pyquery** (HTML/XML parsing)  

   - **fake-useragent** (randomized user agents for avoiding detection)  

   - **retrying & tenacity** (automatic request retrying for failed attempts)  

By offering **pre-built adapters and service examples**, this template simplifies the process of building **scalable and maintainable** web scraping solutions while following best development practices.

For more information about this template, you can check the dedicated page: `Web Scrapping Template Documentation <web_scrapping/index.html>`_.