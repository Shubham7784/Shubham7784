# 📚 Library Management System

A web-based Library Management System built with **Flask** and **MySQL** for managing books and member accounts. This application provides two distinct roles: **Admin** (for librarians) and **User** (for members).

This project uses a simple frontend built with **HTML** and **CSS** and a powerful **Flask** backend to handle all logic and database operations.

## ✨ Features

### 👤 User (Member) Features

  * **Authentication:** Secure user registration and login.
  * **View Catalog:** Browse and search the complete list of available books.
  * **Search & Filter:** Find books by title, author, or genre.
  * **Borrow Books:** Issue a book, which is then added to their borrowed list.
  * **Return Books:** Mark a borrowed book as returned.
  * **View Profile:** See their borrowing history, due dates, and any outstanding fines.
  * **Manage Account:** Update their personal details (e.g., password).

### 🔑 Admin (Librarian) Features

  * **All User Features:** Admins can perform all actions a regular user can.
  * **Book Management (CRUD):**
      * **Add** new books to the catalog (title, author, copies, etc.).
      * **View** all book details.
      * **Update** existing book information.
      * **Delete** books from the catalog.
  * **Member Management:**
      * View a list of all registered members.
      * Edit member details.
      * Delete member accounts.
  * **Circulation Control:**
      * Manually issue books to users.
      * Manually mark books as returned.
      * View a complete history of all transactions (borrows/returns).
  * **Admin Dashboard:** A dashboard with key statistics (e.g., total books, total members, books currently on loan).

-----

## 💻 Tech Stack

  * **Backend:** **Flask** (Python)
  * **Database:** **MySQL**
  * **Frontend:** **HTML5**, **CSS3**
  * **Python Libraries:** `flask`, `SQLAlchemy`
-----

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

  * **Python 3.8** or newer
  * **Flask**
  * **MySQL Server** (Make sure it's running)
  * **Git**

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create a virtual environment:**

    ```sh
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    (It's a good idea to have a `requirements.txt` file. If not, install manually.)

    ```sh
    pip install Flask flask-mysqldb flask-bcrypt
    ```

4.  **Set up the MySQL Database:**

      * Log in to your MySQL server.
      * Create a new database for the project:
        ```sql
        CREATE DATABASE library_db;
        ```
      * (Optional) If you have a `.sql` schema file, import it:
        ```sh
        mysql -u your_user -p library_db < schema.sql
        ```

5.  **Configure Environment Variables:**

      * In your Flask app (`app.py`), you'll need to configure the database connection. It's best practice to use environment variables.
      * Update your `app.py` or config file with your database details:
        ```python
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/librarymanagement_flask'  Replace user with your username & password with your password
        ```

6.  **Run the application:**

    ```sh
    flask run
    ```

      * Your application should now be running at `http://127.0.0.1:5000/`.

-----

## Usage

  * Open your browser and navigate to `http://127.0.0.1:5000/`.
  * **Register** a new account to use the system as a user.
  * **To get admin access:** You may need to either:
    1.  Create a separate admin registration page.
    2.  Manually update your user's role in the database (e.g., `UPDATE users SET is_admin = 1 WHERE id = 1;`).
  * Log in as an admin to access the admin dashboard and management features.

-----

## 🤝 Contributing

Contributions are welcome\! If you have suggestions to improve this project, please fork the repository and create a pull request.

1.  **Fork** the Project
2.  **Create** your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  **Push** to the Branch (`git push origin feature/AmazingFeature`)
5.  **Open** a Pull Request

-----

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.