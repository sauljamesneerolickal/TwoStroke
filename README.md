# Two Stroke Spare Parts Management System

## 🚀 Project Overview
A modern, role-based e-commerce platform for managing and selling two-stroke engine spare parts. The system connects customers with sellers and provides administrators with powerful tools for oversight.

## 🛠 Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML5, Vanilla CSS (Custom "Whitie" Theme), Bootstrap 5.3 + Icons
- **Database**: SQLite (Development) / MySQL or PostgreSQL (Production Ready)
- **Version Control**: Git & GitHub

## ✅ Current Status (In Progress)

### 🔹 Core Features implemented:
- **User Authentication**:
  - Secure Login & Registration for Customers and Sellers.
  - Role-Based Access Control (RBAC): Admin, Seller, Customer.
  - Profile Management: Edit personal details, Change Password with visibility toggle.

- **Admin Dashboard**:
  - Fully modular admin panel (`admin/dashboard/`).
  - **User Management**:
    - View all users (Customers, Sellers).
    - **Actions**: Approve Sellers, Block/Unblock Users, Delete Users (with confirmation modal).
    - **Add New User**: Create accounts manually (Seller/Customer/Admin) directly from the dashboard.
  - **Status Indicators**: Visual badges for verification status (Pending/Verified) and account status (Active/Blocked).
  
- **UI/UX Enhancements**:
  - **Premium Design**: Glassmorphism cards, smooth fade-in animations, and a clean white/gray aesthetic ("Whitie Theme").
  - **Responsive Layout**: Mobile-friendly sidebar and navigation using Bootstrap offcanvas.
  - **Interactive Elements**: Dropdown menus for actions, password visibility toggles, and modals for critical actions.

### 🚧 Future Roadmap (Next Steps):
- **Product Management**: Complete CRUD operations for adding/editing spare parts.
- **Order System**: Flow for Cart -> Checkout -> Order History.
- **Review System**: Allow customers to rate products.
- **Reporting**: Visual charts for sales analytics.

## 📦 Application Status
| Module | Status | Notes |
| :--- | :---: | :--- |
| **Authentication** | ✅ Done | Login, Register, Logout working reliably. |
| **Admin - Users** | ✅ Done | Full CRUD + Approval flow for Sellers. |
| **Admin - Profile** | ✅ Done | Edit profile & Password separate sections working. |
| **Product Catalog** | 🟡 In Progress | Basic structure ready, need detailed add/edit forms. |
| **Shopping Cart** | 🟡 In Progress | Skeleton implemented. |
| **Orders** | 🔴 Pending | Logic to be implemented. |

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/sauljamesneerolickal/TwoStroke.git
   ```
2. Create a virtual environment and activate it.
3. Install dependencies:
   ```bash
   pip install django
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (if needed):
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```
7. Open `http://127.0.0.1:8000` in your browser.

---
*Last Updated: 2026-02-19*
