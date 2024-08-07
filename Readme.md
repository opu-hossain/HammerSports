# Hammer Sports

Welcome to Hammer Sports, an innovative, fully open-sourced blog website developed using Python and the Django framework. This platform boasts essential features like robust user authentication, a dynamic commenting system, integrated email marketing powered by Mailchimp, and seamless social media connectivity. Currently in its inception phase, Hammer Sports aims to evolve into a leading open-source solution for bloggers and content creators worldwide.

## 💻 Technologies Used

- Python
- Django
- Django CKEditor (Rich Text Editor)
- Tailwind CSS (CSS Framework)
- Node.js

## 📝 Observations

- The project uses a customized user model, suggesting customization in user management.
- The `marketing/` folder indicates features for audience engagement, such as newsletters.
- The presence of a `media/` directory with subfolders `featured_images` and `profile_images` indicates an image management system for posts and user profiles.

## 🚀 Getting Started

This guide will walk you through the process of setting up the Hammer Sports project on your local machine.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/opu-hossain/HammerSports.git
   cd HammerSports
   ```

2. **Set Up a Virtual Environment:**

    Virtual environments are a crucial part of Python development, allowing you to manage project-specific dependencies separately. 

    - **Install virtualenv:**

        ```bash
        pip install virtualenv
        ```

    - **Verify the Installation:**

        ```bash
        virtualenv --version
        ```

    - **Create a Virtual Environment:**

        You can name your virtual environment as you prefer. In this example, we're using 'my_env'.

        ```bash
        virtualenv my_env
        ```

    - **Activate the Virtual Environment:**

        Activating the virtual environment will put the environment-specific `python` and `pip` executables into your shell’s `PATH`.

        On macOS and Linux:

        ```bash
        source my_env/bin/activate
        ```

        On Windows:

        ```cmd
        .\my_env\Scripts\activate
        ```

    Now, you're in the virtual environment. Any package you install will be placed in the `my_env` folder, isolated from the global Python environment.

3. **Install Project Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize and Install Node.js Dependencies:** If you have changed styles! 

   ```bash
    npm init -y
    npm install
    ```

5. **Configure Environment Variables:**

    Create a .env file in the root directory (HammerBlog/) and add the following environment variables:

    ```dotenv
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port

    MAILCHIMP_API_KEY=your_mailchimp_api_key
    MAILCHIMP_DATA_CENTER=your_mailchimp_data_center
    MAILCHIMP_EMAIL_LIST_ID=your_mailchimp_email_list_id
    ```

6. **Run Migrations and Start the Development Server:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

7. **Access the Application:**

    Open your web browser and navigate to <http://127.0.0.1:8000> to view the Hammer Sports website.

Remember: This guide is intended for initial setup. For a more comprehensive understanding, we encourage you to explore the source code and customize it according to your needs.

I welcome anyone who want's to contribute to this project!