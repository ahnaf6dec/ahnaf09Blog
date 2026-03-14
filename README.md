# ahnaf09Blog

**Live Site:** [https://ahnaf09blog.onrender.com](https://ahnaf09blog.onrender.com)
*Note: Hosted on Render free tier, first load may take 30–60 seconds.*

---

## Overview

**ahnaf09Blog** is a personal blogging platform built with **Python (Flask)** and **PostgreSQL**. Visitors can read posts, comment, and send messages, while admins can manage content, comments, and uploaded media efficiently.

---

## Features

* Blog post creation and management
* Comment system for readers
* Contact form for visitors
* Admin dashboard for content moderation
* Image upload support
* PostgreSQL database integration

---

## Tech Stack

* **Backend:** Python, Flask
* **Database:** PostgreSQL
* **Frontend:** HTML, CSS, Bootstrap
* **Deployment:** Render

---

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ahnaf09Blog.git
   cd ahnaf09Blog
   ```

2. **Create and activate a virtual environment**
   Linux/macOS:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root with:

   ```env
   DATABASE_URL=your_postgresql_database_url
   SECRET_KEY=your_secret_key
   UPLOAD_FOLDER=app/static/uploads
   ```

5. **Run the application**

   ```bash
   python run.py
   ```

   Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Security

* Keep credentials and secret keys private.
* Use `.env` files for sensitive information.
* Personal credentials for development are not included in the repository: [Secure Credentials](https://github.com/ahnaf6dec/sec-cred)

