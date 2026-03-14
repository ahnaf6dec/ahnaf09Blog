# ahnaf09Blog

Live Site: [https://ahnaf09blog.onrender.com](https://ahnaf09blog.onrender.com)
*(May take 30–60 seconds to load on free Render tier)*

---

**Overview**
ahnaf09Blog is a personal blogging platform built with Python (Flask) and PostgreSQL. Users can read posts, comment, and send messages. Admins can manage posts, comments, and uploads.

---

**Features**

* Blog post creation and management
* Comment system
* Contact form
* Admin dashboard
* Image uploads
* PostgreSQL integration

---

**Tech Stack**
Backend: Python, Flask
Database: PostgreSQL
Frontend: HTML, CSS, Bootstrap
Deployment: Render

---

**Setup**

1. Clone repo:
   `git clone https://github.com/yourusername/ahnaf09Blog.git`
   `cd ahnaf09Blog`
2. Create virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file with:

   ```
   DATABASE_URL=your_postgresql_database_url
   SECRET_KEY=your_secret_key
   UPLOAD_FOLDER=app/static/uploads
   ```
5. Run app: `python run.py`
   Open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

**Security**
Keep credentials and secret keys private. Use `.env` for sensitive info.
