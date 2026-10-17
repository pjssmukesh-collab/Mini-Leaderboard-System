# Mini Leaderboard System — Selenium WebDriver UI Automation Test Suite

Comprehensive end-to-end UI automation testing suite for the **Mini Leaderboard System**, built with **Python 3**, **Selenium WebDriver 4**, and **PyTest**, implementing the **Page Object Model (POM)** design pattern.

---

## 📑 Table of Contents
1. [Overview & Architecture](#overview--architecture)
2. [Test Directory Structure](#test-directory-structure)
3. [Prerequisites & System Requirements](#prerequisites--system-requirements)
4. [Environment Configuration](#environment-configuration)
5. [Installation & Setup](#installation--setup)
6. [Test Suites & Coverage Catalog](#test-suites--coverage-catalog)
7. [Running the Tests](#running-the-tests)
8. [Page Object Model Design](#page-object-model-design)
9. [Troubleshooting & Gotchas](#troubleshooting--gotchas)

---

## Overview & Architecture

- **Application Stack**:
  - **Frontend**: React 19 + Vite (Running at `http://localhost:5173`)
  - **Backend**: FastAPI REST API (Running at `http://127.0.0.1:8000`)
  - **Database**: SQLite
- **Test Framework**: PyTest 8+ with `pytest-html`
- **Automation Driver**: Selenium WebDriver 4.20+ with Chrome / Headless Chrome
- **Design Pattern**: **Page Object Model (POM)** separating page locators, actions, and assertions.
- **Reliability Principles**:
  - Zero arbitrary `time.sleep()` calls — utilizes `WebDriverWait` and `expected_conditions`.
  - Service liveness pre-check: auto-validates that both React and FastAPI are up before running tests.
  - Non-destructive test data strategy using isolated test accounts and parameterization.

---

## Test Directory Structure

```
test/ui_testing/
├── .env.example              # Sample environment variables template
├── config.py                 # Central configuration and environment loader
├── conftest.py               # PyTest fixtures (driver, auth, service checks)
├── pytest.ini                # PyTest configuration, test paths, markers, and options
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation file
│
├── fixtures/                 # Match results fixtures for testing upload & validation
│   ├── valid_results.csv     # Valid CSV with player_id, match_id, kills, placement
│   └── invalid_results.csv   # Invalid CSV missing player identifier column
│
├── pages/                    # Page Object Model classes
│   ├── base_page.py          # Core methods (waits, clicks, typing, viewport)
│   ├── navbar_component.py   # Global navigation bar & profile dropdown
│   ├── home_page.py          # Landing / Home page
│   ├── login_page.py         # Login form, inputs, error states
│   ├── register_page.py      # Registration form, role selection, validation
│   ├── creator_dashboard_page.py  # Creator studio metrics, search, edit/delete modals
│   ├── create_event_page.py  # Tournament creation form & category chips
│   ├── rule_builder_page.py  # Dynamic scoring engine & rule builder table
│   ├── upload_flow_page.py   # Multi-step match result upload, validate & process
│   ├── player_dashboard_page.py   # Player dashboard, tournament cards, join modal
│   └── leaderboard_page.py   # Live tournament leaderboard, podium, export CSV/JSON
│
└── tests/                    # Automated PyTest test suites
    ├── test_application.py   # App launch, title, footer, responsive viewport
    ├── test_navigation.py    # Main navigation links, navbar, hero CTA
    ├── test_login.py         # Full login matrix (valid, invalid, empty, role redirect, logout)
    ├── test_registration.py  # Registration validations, unique user creation, duplicate error
    ├── test_dashboard.py     # Creator & Player dashboard metrics and search filter
    ├── test_events.py        # Tournament creation workflow, category selection, validation
    ├── test_event_rules.py   # Scoring rules creation, active rules table, finish flow
    ├── test_participants.py  # Player tournament enrollment, status modal handling
    ├── test_results_upload.py# CSV result upload, validation report, error handling
    ├── test_leaderboard.py   # Leaderboard rankings, search filter, export functionality
    └── test_profile.py       # Profile dropdown info (name, email, role badge), session logout
```

---

## Prerequisites & System Requirements

1. **Python 3.10+** (Tested with Python 3.11.7)
2. **Google Chrome** browser installed
3. **Running FastAPI Backend** on `http://127.0.0.1:8000`
4. **Running React Frontend** on `http://localhost:5173`

---

## Environment Configuration

Copy `.env.example` to `.env` or set environment variables:

```bash
cd test/ui_testing
cp .env.example .env
```

| Variable | Default Value | Description |
|---|---|---|
| `APP_BASE_URL` | `http://localhost:5173` | React frontend URL |
| `BACKEND_BASE_URL` | `http://127.0.0.1:8000` | FastAPI backend URL |
| `TEST_CREATOR_EMAIL` | `test_creator@example.com` | Dedicated creator test account |
| `TEST_CREATOR_PASSWORD` | `Password123!` | Password for test creator |
| `TEST_PLAYER_EMAIL` | `test_player@example.com` | Dedicated player test account |
| `TEST_PLAYER_PASSWORD` | `Password123!` | Password for test player |
| `HEADLESS` | `true` | `true` for headless execution, `false` to view browser |
| `EXPLICIT_WAIT_TIMEOUT`| `10` | Default timeout (seconds) for element presence/clickability |
| `PAGE_LOAD_TIMEOUT` | `20` | Maximum page navigation timeout (seconds) |

---

## Installation & Setup

1. **Install Python test dependencies**:
   ```powershell
   pip install -r test/ui_testing/requirements.txt
   ```

2. **Verify services are running**:
   - Backend:
     ```powershell
     cd backend
     .\venv\Scripts\activate
     uvicorn app.main:app --reload --port 8000
     ```
   - Frontend:
     ```powershell
     cd frontend
     npm run dev
     ```

---

## Test Suites & Coverage Catalog

### 1. Application Launch & Navigation (`test_application.py`, `test_navigation.py`)
- Application opens successfully and validates document title.
- Hero heading (`Turn every result into a leaderboard.`) renders cleanly.
- Responsive design test: validates usable layout at mobile viewport (375x812, iPhone size).
- Navigation links from Navbar, Hero CTA, and brand logo redirection back to root.

### 2. Login UI (`test_login.py`)
- Initial load & elements verification (email input, password input, sign in button).
- HTML5 client validation for empty email & password, empty email, empty password.
- Email format validation (rejects invalid emails without `@` or domain).
- Server error validation: incorrect password shows error alert.
- Unregistered user login shows error alert.
- Role-based redirect: Creator logs in and lands on `/creator/dashboard`.
- Role-based redirect: Player logs in and lands on `/player/dashboard`.
- Session persistence across navigation to home page.
- Logout flow destroys token and redirects to `/login`.
- Protected route guard: unauthenticated access to `/creator/dashboard` automatically redirects to `/login`.

### 3. Registration UI (`test_registration.py`)
- Required field validation (Name, Email, Password).
- Password minimum length validation (`minLength=6`).
- Invalid email format rejected by client-side validation.
- Duplicate email detection: displays error message when registering an existing email.
- Successful registration with unique timestamped credentials redirects to `/login`.

### 4. Dashboards (`test_dashboard.py`)
- **Creator Dashboard**: renders metric cards, "Create Tournament" button, search input.
- Search filter interaction on creator tournament list.
- **Player Dashboard**: renders open tournaments count, active categories, and search bar.

### 5. Events Management (`test_events.py`)
- Create tournament page loads with category chips, inputs, and submit button.
- Required validation on tournament name.
- Cancel button returns to creator dashboard.
- Full tournament creation: selects "Gaming" category, fills details, sets max participants, and advances to the rule builder.

### 6. Scoring Rules (`test_event_rules.py`)
- Rule builder page loads for tournament.
- Required fields validation on metric and points.
- Adding a valid scoring rule (e.g. `kills`, `operator: each`, `points: 5`).
- Active rules table updates dynamically with new rule.
- "Finish Setup & Return" navigates back to creator dashboard.

### 7. Participants (`test_participants.py`)
- Player dashboard lists available tournaments.
- Join tournament workflow: clicks "Join Event" and handles confirmation modal ("Successfully Registered!" or "Already Registered").
- Navigation from player dashboard directly to the tournament's public leaderboard.

### 8. Results Upload & Validation Pipeline (`test_results_upload.py`)
- Upload page renders file dropzone and `.csv,.xlsx,.json` input.
- File upload with valid fixture (`fixtures/valid_results.csv`) advances to Step 2 and displays the Validation Report (valid records count).
- File upload with invalid fixture (`fixtures/invalid_results.csv`) triggers extraction error state.

### 9. Leaderboard (`test_leaderboard.py`)
- Tournament leaderboard page loads with official standings table.
- Search player filter works smoothly without uncaught errors.
- Export options: verifies that CSV and JSON export buttons are present and interactive.

### 10. User Profile & Session (`test_profile.py`)
- Profile dropdown button renders in navbar for authenticated users.
- Inspects profile details: confirms user name, email, and uppercase role badge (`CREATOR` / `PLAYER`).
- Logout from profile dropdown clears credentials and redirects to `/login`.

---

## Running the Tests

### Run All Tests
```powershell
python -m pytest -c test/ui_testing/pytest.ini test/ui_testing/tests/
```

### Run Tests in Headed Mode (Watch Browser Live)
Set `HEADLESS=false` in `.env` or pass the environment variable:
```powershell
$env:HEADLESS="false"
python -m pytest -c test/ui_testing/pytest.ini test/ui_testing/tests/
```

### Run a Specific Test Suite
```powershell
# Run Authentication tests
python -m pytest -c test/ui_testing/pytest.ini test/ui_testing/tests/test_login.py

# Run Navigation & Application tests
python -m pytest -c test/ui_testing/pytest.ini test/ui_testing/tests/test_navigation.py test/ui_testing/tests/test_application.py

# Run Events & Rules tests
python -m pytest -c test/ui_testing/pytest.ini test/ui_testing/tests/test_events.py test/ui_testing/tests/test_event_rules.py
```

### Run by Marker
```powershell
python -m pytest -c test/ui_testing/pytest.ini -m "smoke"
python -m pytest -c test/ui_testing/pytest.ini -m "auth"
python -m pytest -c test/ui_testing/pytest.ini -m "upload"
```

### Generate a Beautiful HTML Test Report
```powershell
python -m pytest -c test/ui_testing/pytest.ini --html=test/ui_testing/report.html --self-contained-html
```

---

## Page Object Model Design

Every page or major component in the application has a dedicated class inheriting from `BasePage`:

```
BasePage
├── NavbarComponent (Navbar, Profile dropdown, Role links, Logout)
├── HomePage (Hero section, CTA buttons, Footer)
├── LoginPage (Form inputs, HTML5 validation, Error alerts)
├── RegisterPage (Inputs, Role select, Password constraints)
├── CreatorDashboardPage (Tournament cards, Search filter, Edit/Delete modals)
├── CreateEventPage (Tournament metadata, Category presets, Schedule)
├── RuleBuilderPage (Metric inputs, Operator selects, Rules table)
├── UploadFlowPage (File upload dropzone, Stepper, Validation metrics)
├── PlayerDashboardPage (Tournament listings, Join action, Status modals)
└── LeaderboardPage (Podium standings, Table rankings, Search, Export buttons)
```

Each page class encapsulates element locators (using stable XPath, IDs, and name attributes) and user action methods (e.g. `login()`, `add_rule()`, `select_file()`), ensuring that tests remain readable, declarative, and resilient to UI changes.
