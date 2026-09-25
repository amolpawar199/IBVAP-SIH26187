🛡️ IBVAP – Intelligent Border Video Analytics Platform

AI-Based Intelligent Video Analytics Platform for Border Surveillance using Existing CCTV Infrastructure

SIH 2026 | Problem Statement: SIH26187
Organization: Ministry of Home Affairs
Department: Sashastra Seema Bal (SSB), Police II Division
Category: Software
Theme: Blockchain & Cybersecurity

---

📌 Overview

IBVAP (Intelligent Border Video Analytics Platform) is an AI-powered software platform designed to transform existing CCTV infrastructure into an intelligent border surveillance system.

Instead of depending on expensive dedicated surveillance hardware, IBVAP uses existing IP-based CCTV/video streams and applies Artificial Intelligence, Computer Vision, OCR/ANPR, event logging, and blockchain-based integrity mechanisms to generate actionable security intelligence.

The platform is designed for deployment at Border Out Posts (BOPs), check posts, border roads, and other strategic locations.

---

🎯 Problem Statement

Conventional CCTV systems mainly provide live monitoring and video recording. Continuous human monitoring can be difficult, especially across large and remote border areas.

Advanced capabilities such as:

- Facial Recognition
- Automatic Number Plate Recognition
- Intrusion Detection
- Suspicious Activity Detection
- Object Tracking
- Real-time Alerting

often require specialized hardware and proprietary systems.

IBVAP addresses this challenge through a software-defined AI surveillance platform that works with existing CCTV infrastructure.

---

💡 Our Solution

IBVAP follows a simple pipeline:

Existing CCTV / Webcam
        ↓
Video Stream
        ↓
AI & Computer Vision Processing
        ↓
Human / Face / Vehicle / Number Plate Analysis
        ↓
Event & Intrusion Detection
        ↓
Real-Time Alert Generation
        ↓
Secure Event Logging
        ↓
Blockchain-Based Integrity Layer
        ↓
Monitoring Dashboard

The platform aims to provide intelligent surveillance without requiring replacement of existing CCTV infrastructure.

---

🚀 Key Features

👤 Human Detection & Tracking

Detects people appearing in the surveillance area and monitors their movement.

🚧 Virtual Fence / Restricted Zone Detection

Security personnel can define restricted zones within the camera view. Entry into these zones can generate an alert.

⏱️ Loitering Detection

Identifies prolonged presence within a defined surveillance zone and generates an event.

🌙 Night-Time Movement Detection

Designed to identify suspicious human movement during low-light/night surveillance scenarios.

😊 Face Detection

Detects faces from available video streams and provides a foundation for future facial recognition integration.

🚘 Automatic Number Plate Recognition

Uses OCR-based processing to extract vehicle number plates from suitable video frames.

🔔 Real-Time Alerts

Security events can be converted into structured alerts containing information such as:

- Event ID
- Camera ID
- Event type
- Timestamp
- Confidence
- Zone
- Status

🔐 Secure Event Logging

Important surveillance events are stored in a structured database for later investigation and auditing.

⛓️ Blockchain-Based Integrity

Event records can be hashed using SHA-256 and linked through a blockchain-style ledger.

This helps provide tamper-evident event records and improves the integrity of stored surveillance evidence.

📊 Monitoring Dashboard

A centralized dashboard is designed to provide:

- Camera status
- Surveillance events
- Alerts
- Event history
- System status
- Security information

---
🧠 Technology Stack
┌──────────────────────────────┐
                    │       EXISTING CCTV          │
                    │     IP Camera / Webcam       │
                    └──────────────┬───────────────┘
                                   ↓
                    ┌──────────────────────────────┐
                    │     VIDEO INGESTION LAYER    │
                    │       RTSP / OpenCV           │
                    └──────────────┬───────────────┘
                                   ↓
              ┌────────────────────────────────────────┐
              │          AI ANALYTICS ENGINE            │
              │                                        │
              │  YOLO11 │ OpenCV │ Computer Vision    │
              └────────────────────┬───────────────────┘
                                   ↓
       ┌───────────────────────────┼───────────────────────────┐
       ↓                           ↓                           ↓
┌───────────────┐          ┌────────────────┐          ┌────────────────┐
│ Human / Face  │          │ Intrusion &    │          │ ANPR / OCR     │
│ Detection     │          │ Loitering      │          │ Number Plate   │
└───────┬───────┘          └───────┬────────┘          └───────┬────────┘
        └──────────────────────────┼───────────────────────────┘
                                   ↓
                    ┌──────────────────────────────┐
                    │    EVENT & ALERT ENGINE      │
                    │ ID • Time • Zone • Confidence│
                    └──────────────┬───────────────┘
                                   ↓
                    ┌──────────────────────────────┐
                    │      SECURE DATABASE         │
                    │          SQLite              │
                    └──────────────┬───────────────┘
                                   ↓
                    ┌──────────────────────────────┐
                    │ BLOCKCHAIN INTEGRITY LAYER   │
                    │ SHA-256 • Event Hash • Chain │
                    └──────────────┬───────────────┘
                                   ↓
                    ┌──────────────────────────────┐
                    │     MONITORING DASHBOARD     │
                    │ Alerts • Events • Camera     │
                    │ Status • Verification        │
                    └──────────────────────────────┘

---

🏗️ System Architecture

                ┌───────────────────────┐
                │ Existing IP CCTV      │
                │ / Camera Stream       │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Video Processing      │
                │ OpenCV                │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ AI Analytics Engine   │
                │ YOLO / Computer       │
                │ Vision                │
                └───────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Human/Face      Intrusion      ANPR/OCR
        Detection       Detection      Analysis
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                ┌───────────────────────┐
                │ Event Detection       │
                │ & Alert Generation    │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Secure Event Database │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Blockchain Integrity  │
                │ SHA-256 Event Hash    │
                └───────────┬───────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Monitoring Dashboard  │
                └───────────────────────┘

---

🔐 Cybersecurity & Blockchain Layer

Since the SIH problem statement belongs to the Blockchain & Cybersecurity theme, IBVAP incorporates an integrity layer for surveillance events.

For every important event, the platform can generate an event hash using SHA-256.

Example event information:

Event ID
Camera ID
Event Type
Timestamp
Confidence
Zone
Status

The event information is hashed and recorded in the blockchain ledger.

Conceptually:

Event 1
   ↓
SHA-256 Hash
   ↓
Block 1
   ↓
Block 2
   ↓
Block 3
   ↓
Tamper-Evident Event Chain

This provides an additional layer for verifying whether recorded event information has been modified.

---

🗄️ Event Data Model

Example alert structure:

Alert
├── ID
├── Event ID
├── Camera ID
├── Event Type
├── Timestamp
├── Confidence
├── Zone
├── Status
└── Event Hash

---

📂 Project Structure

IBVAP-SIH26187/
│
├── ai/
│   ├── detection/
│   ├── tracking/
│   └── analytics/
│
├── backend/
│   ├── integration.py
│   ├── alert_database.py
│   └── ...
│
├── blockchain/
│   └── blockchain.py
│
├── frontend/
│   └── dashboard/
│
├── security/
│   └── ...
│
├── video/
│   └── ...
│
├── repository/
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md

---

⚙️ Installation

1. Clone the repository

git clone https://github.com/amolpawar199/IBVAP-SIH26187.git

2. Navigate to the project

cd IBVAP-SIH26187

3. Create a virtual environment

python -m venv venv

4. Activate the environment

Windows:

venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

If "requirements.txt" is not available yet:

pip install opencv-python ultralytics

---

▶️ Running the Prototype

Connect a webcam or compatible video source and run the required AI surveillance module.

Example:

python newloitering.py

The system processes the camera feed and identifies relevant surveillance events according to the configured detection zones and parameters.

---

🖥️ Dashboard

The planned monitoring dashboard provides a centralized interface for security personnel to observe:

Camera Status
      ↓
Live Surveillance
      ↓
Detected Events
      ↓
Alerts
      ↓
Event History
      ↓
Blockchain Verification

The objective is to provide a single software platform for monitoring and managing intelligent surveillance events.

---

🌐 Offline / Remote Deployment

IBVAP is designed with remote and connectivity-constrained border environments in mind.

The core AI processing can be performed locally on the deployment system, allowing surveillance analysis to continue without depending entirely on continuous internet connectivity.

This approach can reduce dependency on cloud infrastructure and help support deployment at remote locations.

---

💰 Cost Advantage

IBVAP focuses on utilizing existing CCTV infrastructure instead of requiring complete replacement with specialized AI surveillance cameras.

Conventional Approach

Existing CCTV
     +
Specialized AI Hardware
     +
Proprietary Systems
     +
Additional Infrastructure

IBVAP Approach

Existing CCTV
     +
Software-Based AI Analytics
     +
Secure Event Management

This can help reduce additional hardware requirements and make intelligent surveillance more scalable.

---

📈 Future Scope

Future versions of IBVAP can include:

- Advanced facial recognition
- Improved ANPR accuracy
- Multi-camera tracking
- Advanced suspicious activity detection
- Edge-AI deployment
- GPS/GIS-based surveillance mapping
- Multi-camera command center
- Role-based access control
- Encrypted communication
- Advanced blockchain networks
- Integration with existing command and control systems
- Offline-first synchronization
- Advanced cyber-threat monitoring

---

🎯 Expected Impact

IBVAP aims to:

- Reduce dependency on continuous manual monitoring
- Improve real-time situational awareness
- Generate faster security alerts
- Utilize existing CCTV infrastructure
- Improve event traceability
- Provide tamper-evident security event records
- Support scalable deployment across multiple surveillance locations
- Improve response time to detected incidents

---

🏆 Smart India Hackathon 2026

Problem Statement: SIH26187
Ministry: Ministry of Home Affairs
Department: Sashastra Seema Bal (SSB), Police II Division
Category: Software
Theme: Blockchain & Cybersecurity

Project

IBVAP – Intelligent Border Video Analytics Platform

«Transforming existing CCTV infrastructure into an intelligent, AI-powered and security-focused border surveillance platform.»

---

👥 Team

Team: SIH 2026 Team SYRIX
Team Leader: Amol Pawar

---

📜 Disclaimer

This repository contains an academic/prototype implementation developed for Smart India Hackathon 2026. Detection accuracy and operational performance may vary depending on camera quality, lighting conditions, hardware capabilities, video quality, and deployment environment.

---

⭐ Support

If you find the project interesting, consider giving the repository a ⭐ and following the development of IBVAP.


