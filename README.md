# Intelligent Expense Tracker

Track your expenses intelligently, analyze spending habits, and make smarter financial decisions!  
This open-source application leverages AI-driven insights to give you a clear view of your finances.

---

## 🧑‍💻 Tech Stack

- **Backend**: Django and Django Rest Framework
- **Frontend**: React
- **Styling**: CSS
- **Database**: PostgreSQL
- **Charts & Visualization**: recharts from react
- **Authentication**: JWT

---

## ✨ Features

- **Smart Dashboard**: Central overview of expenses, income, savings, and budgets
- **Add/Edit/Delete Transactions**: Manage your daily spending or earnings easily
- **Categories**: Group expenses (Food, Travel, Shopping, Bills, etc.) 
- **Budgets & Alerts**: Set monthly/weekly budgets
- **Advanced Reports**: Visualize data with pie, bar, and trend charts
- **Search & Filter**: Find expenses by category, date, or amount
- **User Authentication**: Secure registration and login (if implemented)

---

## ⚙️ Configuration & Setup

### 1. Clone the repository

```bash
git clone https://github.com/chaitanya7113/intelligent-expense-tracker.git
cd intelligent-expense-tracker
```

### 2. Setup the Backend (Python)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure environment variables (if any):

Create a `.env` file in the backend root folder:

```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///expenses.db
DEBUG=True
# Add other configuration as needed
```

### 3. Setup the Frontend (JavaScript)

If there’s a separate frontend folder (for React/Vue/Angular):

```bash
cd frontend
npm install
# or
yarn install
```

**Note:** If frontend and backend are in a monorepo or together, adjust paths accordingly.

### 4. Run the Application

**Backend:**
```bash
python manage.py runserver
```

**Frontend:**
```bash
nom run dev
```

### 5. Access the Application

Visit [http://localhost:8000](http://localhost:8000) or the port shown in your terminal.

---

## 🗂️ Project Structure

```text
intelligent-expense-tracker/
│
├── backend/                 # Python backend code
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── ...
│
├── frontend/                # Frontend (React/Angular/View/Vanilla)
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── ...
│
├── README.md
└── ...
```
_Adjust folder names/structure as per your implementation._

---

## 📸 Screenshots

<!-- Uncomment and add your screenshots below -->
<!--
![Dashboard Screenshot](screenshots/dashboard.png)
![Expense Entry](screenshots/entry.png)
-->

---

## 🙌 Contributing

Contributions are welcome!

1. Fork the repo and create your branch:
   ```bash
   git checkout -b feature/new-feature
   ```
2. Commit your changes and push:
   ```bash
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```
3. Open a Pull Request describing your changes.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

**Made with ❤️ by [chaitanya7113](https://github.com/chaitanya7113)**
