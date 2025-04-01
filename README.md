# 📚 BoiBinimoy - A Book Selling & Social Platform

## 📌 Project Overview
BoiBinimoy is a feature-rich **Book Selling Website with Social Media Functionality**, built using **Python Django**. Users can register, verify their email, log-in, create and update their user-profiles. They can post text-based or image-based advertisements for books they want to buy, sell, or exchange. The platform also includes social media-like interactions - users can comment on book posts, search for books, and visit other users' profiles.

In addition to customer functionalities, BoiBinimoy includes **Admin and Manager roles** with specific permissions. Admins can create and manage users, while Managers have post-approval powers and can pin announcements for all users.

---

## 🚀 Features
### 🎯 Customer Features
- 📝 **User Registration with Email Verification**
- 🔐 **User Login & Profile Management**
- 📚 **Post Book Advertisements with Images or Text-only Content**
- 🔍 **Search for Books by Title, Author, or Category**
- 💬 **Comment on Book Posts**
- 👥 **View Other Users' Profiles and Posts**
- 📄 **Text and Image Posts**
- 🏷️ **Manage Own Book Listings**

### 👨‍💼 Manager Features 
- 🏛️ **Manager Dashboard**: Oversee platform activities and manage profiles.
- 👤 **Manage Manager Profiles**: Administer manager accounts and settings.
- 👥 **Manage Customer Users**: Activate or deactivate customer-users who violate platform rules.
- 📚 **Create & Manage Book Categories**: Define categories for users to post books.
- 📋 **Manage Categories & Book Listings**: Edit and organize book posts.
- ✍️ **Create Blogs & Announcements**: Publish blogs or platform updates for users.
- ✅ **Approve Content**: Review and approve posts, blogs, and book advertisements.

### 👑 Admin Features
- 🔑 **Admin Dashboard**: Oversee administrative activities and manage profiles.
- 👤 **Admin Profile**: Manager Admin own profile and settings.
- 👥 **Manage Administrators**: Admins can create and manage **Managers** and other **Admins**.
- 🛠️ **Activate/Deactivate Admins & Managers**.

### 🖥️ Fully Responsive
- ✅ **Optimized for Mobile, Tablet, and Desktop Screens**
- ✅ **Fast Performance and Secure Authentication**

---

## 🏗️ Project Structure
```
BoiBinimoy/
 ├── blogs/                # Blog module
 ├── boibinimoy/           # Main Django project folder
 ├── books/                # Book listing and advertisement module
 ├── static/               # Static files (CSS, JS, Images)
 ├── staticfiles/          # Collected static files
 ├── templates/            # HTML templates for the project
 ├── users/                # User authentication and profile management
 ├── db.sqlite3            # SQLite Database
 ├── manage.py             # Django management script
 ├── requirements.txt      # Dependencies
 ├── vercel.json           # Deployment configuration
```

---

## 🔧 Installation & Setup

### 📌 Prerequisites
Ensure you have the following installed:
- **Python 3.9+**
- **pip (Python Package Manager)**
- **Virtual Environment (Recommended)**

### 🔽 Clone the Repository
```sh
git clone https://github.com/Mahmud-Alam/boibinimoy.git
cd boibinimoy
```

### 📦 Create Virtual Environment & Install Dependencies
```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 🛠️ Apply Migrations
```sh
python manage.py migrate
```

### 🔑 Create a Superuser
```sh
python manage.py createsuperuser
```
Follow the instructions to set up an admin user.

### 🚀 Run the Development Server
```sh
python manage.py runserver
```
Access the app at **http://127.0.0.1:8000/**.

---

## 📜 API Endpoints
| Endpoint                          | Method | Description              |
|-----------------------------------|--------|--------------------------|
| `/`                               | GET    | Home Page                |
| `/about/`                         | GET    | About Page               |
| `/contact/`                       | GET    | Contact Page             |
| `/register/`                      | POST   | User Registration        |
| `/login/`                         | POST   | User Login               |
| `/logout/`                        | POST   | User Logout              |
| `/profile/<username>/`            | GET    | View User Profile        |
| `/edit-profile/`                  | POST   | Edit User Profile        |
| `/change-username/`               | POST   | Change Username          |
| `/change-email/`                  | POST   | Change User email        |
| `/change-password/`               | POST   | Change User password     |
| `/books/`                         | GET    | List All Books           |
| `/books/create-post/`             | POST   | Create New Book Post     |
| `/books/update-post/<id>/`        | POST   | Update Book Post         |
| `/books/delete-post/<id>/`        | POST   | Delete Book Post         |
| `/books/details/<path>/`          | GET    | View Book Details        |
| `/books/category/<path>/`         | GET    | List Books by Category   |
| `/blogs/`                         | GET    | List All Blogs           |
| `/blogs/create-blog/`             | POST   | Create New Blog Post     |
| `/blogs/update-blog/<id>/`        | POST   | Update Blog Post         |
| `/blogs/delete-blog/<id>/`        | POST   | Delete Blog Post         |
| `/blogs/manager/`                 | GET    | List All Manager's Blogs |
| `/manager-dashboard/<username>/`  | GET    | Manager's Dashboard      |
| `/manager-profile/<username>/`    | GET    | Manager's Profile        |
| `/category-list/`                 | GET    | View All Categories      |
| `/create-category/`               | POST   | Create New Category      |
| `/update-category/<path>/`        | POST   | Update Category          |
| `/delete-category/<path>/`        | POST   | Delete Category          |
| `/pending-post/`                  | GET    | View all Pending Posts   |
| `/blogs/accept-book/<id>`         | POST   | Accept Book Post Request |
| `/blogs/accept-blog/<id>`         | POST   | Accept Blog Post Request |
| `/admin-panel/<username>/`        | GET    | Admin Dashboard          |
| `/create-admin/`                  | POST   | Create New Admin         |
| `/create-manager/`                | POST   | Create New Manager       |
| `/manage-administrators/`         | GET    | List of Administrators   |
| `/reactive-user/<username>/`      | POST   | Reactive Users           |
| `/delete-user/<username>/`        | POST   | Delete Users             |

---

## 🛠️ Technologies Used
- **Django 5.1.7** - Python Web Framework
- **SQLite3** - Lightweight Database
- **Django Filter** - For search and filtering
- **Bootstrap** - For UI styling
- **Django Widget Tweaks** - Enhancing form customization
- **Pillow** - Image handling for user uploads
- **Django Bootstrap Form** - Simplified form rendering

---

## 🔐 Authentication & Security
- **Django’s built-in authentication system**
- **Hashed passwords** using Django’s `pbkdf2_sha256`
- **Session & Cookie-based authentication**
- **Email Verification** using Django's Email Backend
- **CSRF Protection** enabled
- **Role-based access control** for Admin & Managers

---

## 📜 Meta Tags (SEO)
```html
<meta name="description" content="BoiBinimoy - Buy & Sell Books, Engage with the Community. A Django-powered social book trading platform.">
<meta name="keywords" content="Book selling, book trade, buy books, sell books, Django, social book platform">
<meta name="author" content="Mahmud Alam">
<meta name="robots" content="index, follow">
```

---

## 🏆 Author
**Mahmud Alam**  
- 🌍 Portfolio: [Mahmud Alam](https://mahmudalam.com/)  
- 📧 Email: mahmudalam.official@gmail.com  
- 🔗 **GitHub:** [GitHub](https://github.com/Mahmud-Alam)  
- 🔗 **LinkedIn:** [LinkedIn](https://www.linkedin.com/in/mahmudalamofficial/)  

---

## 🎉 Acknowledgments
- Inspired by modern book trading platforms.
- Thanks to the **Django Community** for extensive documentation and support.

Happy coding! 🚀
