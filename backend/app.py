from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import platform
import psutil
import redis
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Redis connection
try:
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True, socket_connect_timeout=5)
    r.ping()
    logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
except Exception as e:
    logger.warning(f"Redis connection failed: {e}")
    r = None

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to Eemeli Karjalainen's Personal CSC Rahti Demo!",
        "author": "Eemeli Karjalainen",
        "version": "1.0.0",
        "endpoints": {
            "/api/name": "Get my name",
            "/api/info": "Get personal and system info",
            "/api/projects": "Get my projects",
            "/api/health": "Health check",
            "/api/stats": "App statistics"
        }
    })

@app.route('/api/name')
def get_name():
    """Returns my name - required for identification"""
    name = "Eemeli Karjalainen"
    
    # Log to Redis if available
    if r:
        try:
            r.incr('name_requests')
            r.set('last_name_request', datetime.now().isoformat())
        except Exception as e:
            logger.warning(f"Redis logging failed: {e}")
    
    logger.info("Name endpoint accessed")
    return jsonify({
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "message": f"Hello! I'm {name}, and this is my CSC Rahti demonstration application."
    })

@app.route('/api/info')
def get_info():
    """Personal and system information"""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = {
            "personal": {
                "name": "Eemeli Karjalainen",
                "role": "Student",
                "course": "Cloud Services",
                "university": "OAMK - Oulu University of Applied Sciences",
                "email": "eekarjal24@students.oamk.fi"
            },
            "system": {
                "hostname": platform.node(),
                "platform": platform.system(),
                "platform_release": platform.release(),
                "architecture": platform.machine(),
                "python_version": platform.python_version(),
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "memory_percent": memory.percent,
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "disk_percent": round((disk.used / disk.total) * 100, 1)
            },
            "application": {
                "name": "Eemeli's CSC Rahti Demo",
                "version": "1.0.0",
                "port": os.environ.get('PORT', 5000),
                "environment": os.environ.get('FLASK_ENV', 'production'),
                "redis_connected": r is not None
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(info)
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return jsonify({"error": "Failed to get system information"}), 500

@app.route('/api/projects')
def get_projects():
    """My projects and achievements"""
    projects = {
        "projects": [
            {
                "name": "CSC Rahti Demo Application",
                "description": "Multi-container web application deployed on CSC Rahti platform",
                "technologies": ["Flask", "React", "Docker", "OpenShift", "Redis"],
                "status": "Active",
                "url": "This application"
            },
            {
                "name": "Cloud Services Course",
                "description": "Learning containerization, orchestration, and cloud deployment",
                "technologies": ["Docker", "Kubernetes", "OpenShift", "CSC Rahti"],
                "status": "In Progress",
                "achievements": [
                    "Successfully deployed multi-container application",
                    "Implemented REST API with personal endpoints",
                    "Configured auto-scaling and health monitoring"
                ]
            },
            {
                "name": "Container Architecture Study",
                "description": "Exploring different container deployment patterns",
                "technologies": ["Docker Compose", "Multi-stage builds", "Nginx proxy"],
                "status": "Learning",
                "topics": [
                    "Single-pod multi-container architecture",
                    "Service mesh communication",
                    "Container security best practices"
                ]
            }
        ],
        "skills": [
            "Python/Flask backend development",
            "React frontend development", 
            "Docker containerization",
            "OpenShift/Kubernetes deployment",
            "REST API design",
            "Multi-container orchestration"
        ],
        "contact": {
            "name": "Eemeli Karjalainen",
            "email": "eekarjal24@students.oamk.fi",
            "university": "OAMK - Oulu University of Applied Sciences",
            "note": "This is a demonstration application for educational purposes"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(projects)

@app.route('/api/health')
def health_check():
    """Health check endpoint for Kubernetes"""
    health = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "backend",
        "version": "1.0.0"
    }
    
    # Check Redis connection
    if r:
        try:
            r.ping()
            health["redis"] = "connected"
        except Exception as e:
            health["redis"] = f"disconnected: {e}"
    else:
        health["redis"] = "not configured"
    
    return jsonify(health)

@app.route('/api/ready')
def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    return jsonify({
        "status": "ready",
        "timestamp": datetime.now().isoformat(),
        "service": "backend"
    })

@app.route('/api/stats')
def get_stats():
    """Application statistics"""
    stats = {
        "uptime": "Available since startup",
        "total_requests": "Tracked if Redis available",
        "name_requests": 0,
        "last_name_request": None,
        "redis_status": "disconnected"
    }
    
    if r:
        try:
            stats["name_requests"] = int(r.get('name_requests') or 0)
            stats["last_name_request"] = r.get('last_name_request')
            stats["redis_status"] = "connected"
        except Exception as e:
            stats["redis_error"] = str(e)
    
    stats["timestamp"] = datetime.now().isoformat()
    return jsonify(stats)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "Try /api/name to get my name, or /api/info for more details",
        "available_endpoints": ["/api/name", "/api/info", "/api/projects", "/api/health"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on the server side"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Eemeli's Backend API on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Redis configured: {r is not None}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
