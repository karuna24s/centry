# Centry 🏛️
### **AI-Native Infrastructure & Security Auditor**

**Centry** is an automated auditing agent designed to identify "silent" production killers in modern web applications. By combining **deterministic Python-native security scanning** with **LLM-powered architectural reasoning**, Centry bridges the gap between basic linting and senior-level code reviews.



---

## 🚀 Core Capabilities

### 1. Architectural Reasoning (via Claude 4.6)
Centry analyzes code for long-term scalability and reliability, focusing on:
* **N+1 Query Detection:** Identifies lazy-loading traps in ActiveRecord (Ruby) or Prisma (TS) that saturate database connections.
* **Transaction Integrity:** Flags external API calls (Stripe, Twilio, AWS) made inside database transactions—a critical scaling risk.
* **Concurrency Analysis:** Detects **TOCTOU** (Time-of-check to time-of-use) race conditions in state-sensitive logic like bookings or payments.
* **Worker Idempotency:** Audits background jobs (Sidekiq/BullMQ) for retry safety and atomic failures.

### 2. Native Security Guardrails
A high-precision Python engine performs multi-pass regex scans to prevent credential leakage:
* **Hardcoded Secrets:** Detects AWS Access Keys, Stripe Secret Keys, Google API Keys, and Postgres Connection Strings.
* **Generic Secret Detection:** Identifies unencrypted passwords, tokens, and sensitive ENV variables in plain text.



---

## 🛠️ Technical Architecture
* **The Brain (API):** A **FastAPI** (Python 3.12) server orchestrating the dual-pass audit (Security + AI).
* **The Intelligence:** Integrated with the **Anthropic 2026 SDK** using the Claude-Sonnet-4-6 frontier model.
* **The Scanner:** A modular directory crawler that transmits local source code to the auditor via secure HTTP.

---

## 🚦 Installation & Setup

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd centry
```

### 2. Environment Configuration
Create a `.env` file in the root directory to store your credentials:
```bash
touch .env
```
Add your Anthropic API key to the `.env` file:
```bash
ANTHROPIC_API_KEY=your_key_here
```

### 3. Virtual Environment Setup
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install fastapi uvicorn anthropic pydantic requests
```

---

## 💻 Usage

### 1. Start the Auditor Engine (The Server)
In your first terminal window, start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

### 2. Run the Directory Scanner (The Client)
In a second terminal window (with the venv activated), run the scanner logic:
```bash
python3 -m app.scanner.logic
```

---

## 📊 Sample Audit Output

| Issue | Severity | Category | Impact |
| :--- | :--- | :--- | :--- |
| **Hardcoded Stripe Key** | 🔴 Critical | Security | Total account compromise |
| **N+1 on @refunds.user** | 🔴 Critical | Performance | DB connection pool exhaustion |
| **API Call in Transaction** | 🟠 High | Reliability | Locked DB rows during HTTP latency |
| **No Idempotency Key** | 🟠 High | Integrity | Duplicate charges on retry |

---

## 🏛️ Project Structure

```
centry/
├── app/
│   ├── main.py                # FastAPI Entry Point (The Server)
│   ├── scanner/
│   │   └── logic.py           # Directory Crawler & Client Logic
│   └── services/
│       ├── ai_logic.py        # LLM Architectural Reasoning Service
│       └── security_logic.py  # Regex-based Security Engine
├── venv/                      # Python Virtual Environment
├── .env                       # Environment Variables (Local only)
└── README.md                  # System Documentation
```
---