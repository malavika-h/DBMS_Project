A comprehensive, role-based College Club Management Platform designed to streamline club registrations, membership workflows, and administrative privileges. Built using **Django** and **SQLite**, this project was developed as part of a Database Management Systems (DBMS) course to demonstrate relational integrity, complex query handling, and state-driven workflows.

---

## 🚀 Key Features

* **Multi-Tiered Access Control (RBAC):** Distinct permissions and UI dashboards for General Students, Club Members, Club Officers (Leadership), and Campus Administrators.
* **Membership Lifecycle Workflow:** Fully stateful application pipeline managing user registration $\rightarrow$ join requests $\rightarrow$ pending status $\rightarrow$ conditional acceptance or rejection.
* **Role Promotion & Privileges:** Club leaders can dynamically assign roles, delegate officer positions, and manage specific club-wide permissions.
* **Relational Integrity:** A strictly structured SQLite schema enforcing cascading deletes, unique constraints, and foreign key relationships to prevent anomalous data states.

---

## 📊 Database Schema & Relationships

The backend architecture is built upon a highly normalized relational structure mapping the following core entities:
* **Users / Students:** The base identity layer handling authentication.
* **Clubs:** Stores club metadata, founding dates, and status.
* **Memberships:** A bridge table mapping Users to Clubs with attributes for `Role` (Member, Treasurer, President) and `Status` (Pending, Approved, Rejected).
* **Events / Logs:** Tracks internal club actions and registrations.

---

## 🛠️ Tech Stack

* **Backend Framework:** Django (Python)
* **Database Engine:** SQLite3
* **Frontend:** Django Templates + Bootstrap (for a clean, responsive dashboard layout)

---
