
# Logistics Management System

## Overview

The Logistics Management System is a Django-based web application designed to manage logistics operations efficiently. 
The system supports features such as user authentication, role-based access control, spare parts management, and dynamic search capabilities.

---

## Features

### Core Features

- **User Authentication**: Register, login, and logout functionalities.
- **Role-Based Access Control**: Different levels of access based on user roles (e.g., Admin, Manager).
- **Spare Parts Management**: Add, edit, delete, and search spare parts dynamically using AJAX.
- **User Action Logging**: Capture and log user actions for auditing purposes.
- **Responsive Design**: Clean and simple frontend templates.

### Advanced Features

- **Dynamic Search**: Real-time search for spare parts with JavaScript and AJAX.
- **Form Validation**: Client-side form validation to improve user experience.
- **Database Transactions**: Atomic operations to ensure data consistency.
- **Confirmation Dialogs**: JavaScript-powered confirmation before critical actions like deletions.

---

## Installation

### Prerequisites

1. Python 3.8+
2. Django 4.x
3. Virtualenv (optional but recommended)
4. reportlab

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Thimethane/logistics-management-system.git
   cd logistics-management-system
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the server:

   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000`.

---

## Usage

### Admin Panel

1. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

2. Login to the admin panel at `http://127.0.0.1:8000/admin`.

### Spare Parts Management

1. Navigate to the Spare Parts section.
2. Add, edit, delete, or search for spare parts.

### Logs

- User actions are logged automatically for auditing purposes.

---

## Project Structure

```
logistics-management-system/
├── manage.py
├── logistics/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── spare_parts/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── spare_parts/
│   │       ├── add_spare_part.html
│   │       ├── edit_spare_part.html
│   │       ├── spare_parts_list.html
│   │       └── delete_spare_part.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── scripts.js
│   └── img/
│       └── (place any images here)
```

---

## Development

### Adding Features

1. Add models to `models.py`.
2. Create views in `views.py`.
3. Update templates in the respective app's `templates/` directory.
4. Add JavaScript for dynamic features in `static/js/scripts.js`.

### Testing

Run tests to ensure the application works as expected:

```bash
python manage.py test
```

---

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- **Django Framework**: For providing an excellent backend framework.
- **Bootstrap**: For frontend responsiveness and styling.
- **Contributors**: Thanks to everyone who contributed to this project.

---

## Contact

For questions or suggestions, feel free to contact:

- **Email**: thimethane@outlook.com
- **GitHub**: [yourusername](https://github.com/Thimethane)

---

### Screenshots

![Dashboard Screenshot](static/img/dashboard_screenshot.png)
![Spare Parts List Screenshot](static/img/spare_parts_list_screenshot.png)
