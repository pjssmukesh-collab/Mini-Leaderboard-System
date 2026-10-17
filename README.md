# Mini Leaderboard System Frontend

The frontend is a React single-page application for creating events, configuring scoring rules, uploading results, and viewing ranked participants. It uses Vite for development and communicates with the FastAPI backend through the API client in `src/api/client.js`.

## Features

- Register and sign in as a creator or player
- Create and manage leaderboard events
- Configure event scoring rules
- Upload result files and review validation reports
- Join events as a participant
- View event leaderboards and player dashboards

## Tech Stack

- React 19
- Vite
- React Router
- Axios
- Bootstrap
- Chart.js and `react-chartjs-2`
- Lucide React icons

## Prerequisites

- Node.js 18 or newer
- npm
- The backend running at `http://127.0.0.1:8000`

The backend setup is documented in the repository root. The frontend currently uses `http://127.0.0.1:8000` as its API base URL in `src/api/client.js`.

## Getting Started

From this directory:

```bash
npm install
npm run dev
```

Vite will print the local development URL, normally `http://localhost:5173`.

Start the backend in a second terminal before using authenticated pages:

```bash
cd ../backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Available Scripts

| Command | Description |
| --- | --- |
| `npm run dev` | Start the Vite development server with hot reload |
| `npm run build` | Create a production build in `dist/` |
| `npm run preview` | Serve the production build locally |
| `npm run lint` | Run Oxlint against the frontend source |

## Project Structure

```text
src/
	api/              Axios client and backend requests
	components/       Shared navigation, footer, and home sections
	contexts/         Authentication state
	pages/
		auth/            Login and registration
		creator/         Event, rule, and creator dashboard views
		player/          Player dashboard and leaderboard views
		results/         Result upload flow
	App.jsx            Application routes and layout
	App.css            Application-level styles
	index.css          Global styles
```

## Typical Workflow

1. Register or log in.
2. Create an event as a creator.
3. Add the event's scoring rules.
4. Upload participant results and validate the upload.
5. Process valid results to calculate scores and rankings.
6. Join the event or open its leaderboard to review results.

## Troubleshooting

- **Network errors:** Confirm the backend is running on port `8000` and that the browser URL matches the CORS origins configured in `backend/app/core/config.py`.
- **Unauthorized requests:** Log in again. The access token is stored in browser local storage and cleared automatically after a `401` response.
- **Build issues:** Remove `node_modules`, run `npm install`, and retry `npm run build`.
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.
