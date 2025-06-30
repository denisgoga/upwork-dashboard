# Upwork Dashboard

Upwork Dashboard është një aplikacion Django për menaxhimin e projekteve, detyrave dhe integrimin me Upwork API. Ofron autentikim me role, UI moderne me Tailwind CSS, komente për detyra dhe admin panel të avancuar.

## 🚀 Funksionalitetet Kryesore
- Autentikim me role (admin/developer)
- Listim, detaje, krijim/editim projektesh dhe detyrash
- Komente për detyra
- Admin panel me filtra të avancuar
- Seed i të dhënave fillestare
- Import projekte nga Upwork API
- UI moderne me Tailwind CSS (ngjyra sticky notes për forma)
- Dashboard me statistika (task count by status)

## ⚙️ Instalimi

1. **Klononi projektin:**
   ```sh
   git clone https://github.com/denisgoga/upwork-dashboard.git
   cd upwork-dashboard
   ```
2. **Krijoni dhe aktivizoni virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Instaloni varësitë:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Krijoni file-in `.env` në root:**
   ```env
   DB_NAME=db.sqlite3
   UPWORK_API_URL=https://api.upwork.com/example/projects
   UPWORK_API_TOKEN=your_token_here
   ```
5. **Migrimi i databazës:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Seed i të dhënave fillestare (opsionale):**
   ```sh
   python manage.py seed_data
   ```
7. **Krijoni një superuser (opsionale):**
   ```sh
   python manage.py createsuperuser
   ```
8. **Nisni serverin:**
   ```sh
   python manage.py runserver
   ```

Aksesoni aplikacionin te: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 👤 Kredenciale Testuese (nga seed)
- **Admin:**
  - Username: `admin`
  - Password: `admin123`
- **Developer:**
  - Username: `dev1` / `dev2`
  - Password: `dev123`

## 📦 Funksione Shtesë
- **Import nga Upwork:**
  ```sh
  python manage.py import_upwork
  ```
- **Admin Panel:**
  [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 📝 UI & Dizajn
- Të gjitha pamjet kryesore janë të stilizuara me Tailwind CSS.
- Forma për detyra dhe komente kanë background të verdhë (sticky notes).
- Tabelat, butonat dhe input-et janë të qarta dhe moderne.

## 📝 Kontributi
Pull request-et dhe sugjerimet janë të mirëpritura!

---

© 2025 Upwork Dashboard. Build with Django & Tailwind CSS. 