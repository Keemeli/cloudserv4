# Eemeli's Personal CSC Rahti Demo Application

A personalized multi-container web application deployed on CSC Rahti platform, featuring a Flask backend API and React frontend with personal information and interactive features.

## 🚀 Features

- **Personal API**: REST endpoints returning personal information including my name
- **Interactive Dashboard**: React-based frontend with modern UI
- **Multi-Container Architecture**: Flask backend + React frontend + Redis coordination
- **CSC Rahti Optimized**: Configured for OpenShift deployment
- **Health Monitoring**: Built-in health checks and monitoring endpoints
- **Auto-Scaling**: Kubernetes HPA for handling traffic loads

## 🏗️ Architecture

```
┌─────────────────┐    HTTP    ┌─────────────────┐
│   React SPA     │ ---------> │  Flask Backend  │
│  (Frontend)     │    API     │     (API)       │
│   Port: 8080    │            │   Port: 5000    │
└─────────────────┘            └─────────────────┘
         │                              │
         └──────────┬───────────────────┘
                    ▼
         ┌─────────────────┐
         │     Redis       │
         │ (Coordination)  │
         └─────────────────┘
```

## 📁 Project Structure

```
.
├── backend/                 # Flask API
│   ├── app.py              # Main backend application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # React SPA
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   ├── Dockerfile          # Frontend container
│   └── nginx.conf          # Nginx configuration
├── openshift/              # CSC Rahti deployment configs
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   └── routes.yaml
├── docker-compose.yml      # Local development
└── README.md              # This file
```

## 🎯 Personal Features

- **GET /api/name** - Returns "Eemeli Karjalainen" 
- **GET /api/info** - Personal information and system details
- **GET /api/projects** - List of my projects and achievements
- **Interactive UI** - Personal dashboard with information about me

## 🚀 Quick Start

### Local Development

1. Clone and navigate to project:
   ```bash
   git clone <your-repo-url>
   cd cloudserv4
   ```

2. Start all services:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Name endpoint: http://localhost:5000/api/name

### Deploy to CSC Rahti

1. Login to CSC Rahti:
   ```bash
   oc login https://api.2.rahti.csc.fi:6443
   ```

2. Create project:
   ```bash
   oc new-project eemeli-demo --description="csc_project: YOUR_PROJECT_NUMBER"
   ```

3. Build from Git:
   ```bash
   REPO="https://github.com/YOUR_USERNAME/cloudserv4.git"
   oc new-build --strategy=docker --name=backend "$REPO" --context-dir=backend
   oc new-build --strategy=docker --name=frontend "$REPO" --context-dir=frontend
   ```

4. Deploy:
   ```bash
   oc apply -f openshift/
   ```

5. Get your app URL:
   ```bash
   oc get routes
   ```

## 📊 API Endpoints

- **GET /** - Frontend dashboard
- **GET /api/name** - Returns "Eemeli Karjalainen"
- **GET /api/info** - Personal and system information
- **GET /api/health** - Health check endpoint
- **GET /api/projects** - My projects and achievements

## 👨‍💻 About Me

This application was created by **Eemeli Karjalainen** (eekarjal24@students.oamk.fi) as part of cloud services coursework at OAMK - Oulu University of Applied Sciences, demonstrating containerization, multi-service architecture, and deployment to CSC Rahti platform.

## 📄 License

Educational project for CSC Rahti demonstration.
