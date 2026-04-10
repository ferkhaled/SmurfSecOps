# Part 2 — Build and Containerize the BerryShop API

<!-- ALREADY WRITTEN — paste content here -->
<!-- Phase 2: Application -->
<!-- Covers: FastAPI app structure, running tests locally, writing the Dockerfile, -->
<!--         building and exporting the image for the k3s lab -->
<!-- Lab files: app/berryshop-api/ -->
---

🛡️ SmurfSecOps Lab - Part 2
🍓 Build the BerryShop Application (FastAPI)

---

🧭 Quick Introduction
In Part 1, we prepared our environment and deployed a working Kubernetes cluster.
Now it's time to build something real.
👉 In this article, we will create our application: BerryShop 🍓
This application will be:
simple
easy to understand
and intentionally not secure (for now)

👉 We will use it later to:
introduce vulnerabilities
scan it
attack it
and secure it step by step

---

🎯 What you will achieve
By the end of this article, you will have:
A working API application
A basic project structure
A runnable service locally
An application ready for containerization

---

📦 Project Repository
👉 https://github.com/ferkhaled/SmurfSecOps

---

📁 Step 1 - Navigate to the Application Folder
From your project root:
cd SmurfSecOps/app
Create the project:
mkdir berryshop-api
cd berryshop-api

---

🐍 Step 2 - Create a Python Virtual Environment
python -m venv venv
Activate it:
Windows:
venv\Scripts\activate
Linux/macOS:
source venv/bin/activate

---

📦 Step 3 - Install Dependencies
pip install fastapi uvicorn
FastAPI → API framework
Uvicorn → application server

---

🧱 Step 4 - Create the First API
Create a file:
touch main.py
Add the following code:
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Welcome to SmurfBerries Shop 🍓"}
@app.get("/berries")
def get_berries():
    return ["smurfberry", "golden-smurfberry", "wild-smurfberry"]

---

▶️ Step 5 - Run the Application
uvicorn main:app --reload
You should see:
Uvicorn running on http://127.0.0.1:8000

---

🌐 Step 6 - Test the API
Open your browser:
👉 http://127.0.0.1:8000
👉 http://127.0.0.1:8000/docs

---

🔥 Important Feature
FastAPI automatically generates interactive API documentation.
👉 This allows you to:
test endpoints easily
understand API structure
debug quickly

---

🧩 Step 7 - Add Basic Functionality
Let's simulate a simple store.
Update your code:
from fastapi import FastAPI
app = FastAPI()
berries_db = []
@app.get("/")
def root():
    return {"message": "Welcome to SmurfBerries Shop 🍓"}
@app.get("/berries")
def get_berries():
    return berries_db
@app.post("/berries")
def add_berry(name: str):
    berries_db.append(name)
    return {"message": f"{name} added!"}

---

🧠 What is happening here?
GET /berries → returns all berries
POST /berries → adds a berry
data is stored in memory

👉 Simple, but enough for our lab.

---

⚠️ Important - Intentional Weakness
At this stage, the application:
❌ has no authentication
❌ has no input validation
❌ stores data in memory
❌ has no security controls

👉 This is intentional.
We will:
break it
scan it
fix it

in the upcoming articles.

---

🧪 Quick Test
Add a berry:
curl -X POST "http://127.0.0.1:8000/berries?name=evil-smurfberry"
Check data:
curl http://127.0.0.1:8000/berries

---

🧠 What we did
At this stage, you have:
a working API
a simple backend logic
an intentionally vulnerable app
a base for DevSecOps

👉 Exactly what we need for the next steps.

---

⚠️ Common Issues
FastAPI not running
👉 Make sure your virtual environment is activated

---

Port already in use
Run on a different port:
uvicorn main:app --reload --port 8001

---

🏁 Conclusion
We now have our BerryShop application 🍓
It is:
simple
functional
intentionally insecure

---

🔜 Next Article
👉 Part 3 - Containerize the Application (Docker)
We will:
build a Docker image
run the app in a container
prepare it for Kubernetes deployment

---

💬 Final Note
Keep the application as it is.
Do not try to fix anything yet.
Because very soon…
👉 Gargamel will start exploiting it 😈