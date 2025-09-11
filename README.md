# Task-Accomplisher
# 📝 Task Accomplisher  

**Task Accomplisher** is a full-stack **Flask-based web application** designed to help users organize, track, and complete their tasks efficiently. It provides an intuitive dashboard where users can add, edit, delete, and monitor tasks with deadlines, while also keeping track of their progress through a visual timeline and achievement bar. The app also supports user authentication, secure profile management, and a responsive design for a smooth experience across devices.  

---

## 🌟 What is Task Accomplisher?  

Task Accomplisher is more than just a to-do list — it’s a **personal productivity assistant**.  
It is designed to:  

- Help users **create and manage tasks** with priorities and deadlines.  
- Show **progress visualization** so users can see how much time they have before a task is due.  
- Provide a **personal dashboard** with completed vs total tasks.  
- Allow users to **register, log in securely, and manage their profiles**, including uploading profile pictures.  

This makes it suitable for students, professionals, and anyone who wants to **stay organized** and **accomplish more**.  

---

## 🔧 Technologies Used  

### Backend  
- **Flask** – Lightweight web framework  
- **Flask-WTF** – Form handling & validation  
- **Flask-Bcrypt** – Secure password hashing  
- **Flask-Migrate** – Database migrations  
- **SQLAlchemy** – ORM for database management  

### Frontend  
- **Bootstrap 5** – Responsive styling & layout  
- **Bootstrap Icons** – Icon set for better UI  
- **Custom CSS** – Enhanced styling and animations  
- **Vanilla JavaScript** – Interactive features (typewriter effect, progress bar animations, password toggle, etc.)  

### Database & File Handling  
- **SQLite** (default, can be replaced with PostgreSQL or MySQL)  
- **UUID** – Unique naming for uploaded profile pictures
- **Werkzeug `secure_filename`** – Safe file upload handling  

---


---

## ⚙️ Installation & Setup  

Follow these steps to run the project locally:  

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/task-accomplisher.git
cd task-accomplisher
```
2. **Install vertual env**  
```bash
pip install virtualenv
```
3. **Create a virtual environment**  
```bash
python -m venv venv
```
4. **Activate virtual environment**
>Windows
```bash
venv\Scripts\activate
```
>Mac/Linux
```bash
source venv/bin/activate
```
5. **Install dependencies**
```bash
pip install -r requirements.txt
```
6. **Set up the database**
```bash
flask --app app db init
flask --app app db migrate -m "Initial migration"
flask --app app db upgrade

```
7. **Run the application**
```bash
flask --app app run
```
8. **Open your browser and visit:**
[http://127.0.0.1:5000](http://127.0.0.1:5000)
_(open in new tab)_

---
## 🔐 Security Highlights

- **Passwords are securely hashed** using bcrypt (never stored in plain text).
- **CSRF protection** – via Flask-WTF. 
- Safe file uploads with **UUID renaming** – + `secure_filename`.
---
## 📸 Example Screens 

- **Homepage** – Clean landing page with navigation.
<img src="./screenExamples/homepage.png" width="600" alt="Homepage"/> 
<img src="./screenExamples/homepage2.png" width="600" alt="Homepage"/> 
<img src="./screenExamples/homepage3.png" width="600" alt="Homepage"/> 

- **User Dashboard** – Displays active and completed tasks.

- **Task Timeline** – Visual progress bar showing deadline tracking.

- **Profile Page** – Edit username, email, phone, address, and photo.

--- 

## 🚀 Future Enhancements

- **Email verification & password reset**

- **Task categorization & filtering**

- **Overdue task notifications**

- **Multi-user task collaboration**

---


