# 🩺 Medical Imaging and Report Assistant

An AI-powered full-stack web application to upload, annotate, and analyze medical images with automated report generation using GPT-4. Built with **FastAPI**, **React.js**, and **PostgreSQL**, this platform helps healthcare professionals manage patients, medical reports, and image diagnostics efficiently and securely.

---

## 🚀 Features

- 🔐 **Authentication**: JWT-based login + OAuth (Google, GitHub)
- 🧍‍♂️ **Patient Management**: Create, edit, delete, and view patients
- 📝 **Report Management**:
  - Create and edit diagnostic reports
  - Attach images
  - Search by title and filter by patient
  - Admin-only delete access
  - Export to PDF
- 🖼️ **Image Upload & Annotation**:
  - Upload medical images (e.g. X-rays)
  - Annotate with bounding boxes
  - Preview annotated images
- 🤖 **AI Integration**:
  - GPT-4-based report generation from image + metadata
  - Simulated image segmentation endpoint with labeled bounding boxes
- 👥 **Role-Based Dashboards**:
  - `admin`: Full access to users, reports, patients
  - `instructor`: Can create and view reports/images
  - `student`: Read-only access to assigned content

---

## 🧱 Tech Stack

### Backend – FastAPI
- Authentication (JWT & OAuth via Authlib)
- RESTful APIs for users, patients, reports, images
- GPT-4 integration for report generation
- PostgreSQL with SQLAlchemy ORM

### Frontend – React.js
- Role-based routing
- Google/GitHub OAuth login
- Image annotation (Canvas / Fabric.js)
- Report management UI with PDF export

---

## 🗃️ Project Structure

### Backend (FastAPI)

### RUN 
npm run dev

### Key points to notice
Change role to "admin" from db and fill with ur information in.env file
