# Deployment Script for CSC Rahti
# Eemeli Karjalainen's Personal Demo Application

#!/bin/bash

set -e

PROJECT_NAME="eemeli-demo"
REPO_URL="https://github.com/YOUR_USERNAME/cloudserv4.git"

echo "🚀 Deploying Eemeli's Personal CSC Rahti Demo Application"
echo "=================================================="

# Function to check if oc command exists
check_oc() {
    if ! command -v oc &> /dev/null; then
        echo "❌ OpenShift CLI (oc) not found. Please install it first."
        echo "   Download from: https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/"
        exit 1
    fi
}

# Function to check if logged in to OpenShift
check_login() {
    if ! oc whoami &> /dev/null; then
        echo "❌ Not logged in to OpenShift. Please login first:"
        echo "   oc login https://api.2.rahti.csc.fi:6443"
        exit 1
    fi
    
    echo "✅ Logged in as: $(oc whoami)"
}

# Function to create or select project
setup_project() {
    echo "📁 Setting up project: $PROJECT_NAME"
    
    if oc get project $PROJECT_NAME &> /dev/null; then
        echo "✅ Project $PROJECT_NAME already exists, using it."
        oc project $PROJECT_NAME
    else
        echo "🆕 Creating new project: $PROJECT_NAME"
        read -p "Enter your CSC project number (e.g., 2015319): " csc_project
        oc new-project $PROJECT_NAME --description="csc_project: $csc_project"
    fi
}

# Function to build images from Git repository
build_images() {
    echo "🔨 Building container images from Git repository"
    
    # Update REPO_URL with actual repository
    echo "📝 Update REPO_URL in this script with your actual GitHub repository URL"
    echo "   Current: $REPO_URL"
    
    # Delete existing build configs if they exist
    oc delete bc backend frontend 2>/dev/null || true
    
    # Create build configs from Git repository
    echo "🏗️ Creating backend build config..."
    oc new-build --strategy=docker --name=backend "$REPO_URL" --context-dir=backend
    
    echo "🏗️ Creating frontend build config..."
    oc new-build --strategy=docker --name=frontend "$REPO_URL" --context-dir=frontend
    
    # Start builds
    echo "⏳ Starting builds (this may take several minutes)..."
    oc start-build backend --follow
    oc start-build frontend --follow
    
    echo "✅ Builds completed successfully!"
}

# Function to deploy application
deploy_application() {
    echo "🚀 Deploying application components..."
    
    # Apply all OpenShift configurations
    oc apply -f openshift/backend-deployment.yaml
    oc apply -f openshift/frontend-deployment.yaml
    oc apply -f openshift/routes.yaml
    oc apply -f openshift/hpa.yaml
    
    # Wait for deployments
    echo "⏳ Waiting for deployments to be ready..."
    oc rollout status deployment/backend --timeout=300s
    oc rollout status deployment/frontend --timeout=300s
    
    echo "✅ Application deployed successfully!"
}

# Function to show application URLs
show_urls() {
    echo "🌐 Application URLs:"
    echo "=================================================="
    
    frontend_url=$(oc get route frontend-route -o jsonpath='{.spec.host}' 2>/dev/null || echo "Route not found")
    backend_url=$(oc get route backend-route -o jsonpath='{.spec.host}' 2>/dev/null || echo "Route not found")
    
    if [ "$frontend_url" != "Route not found" ]; then
        echo "🖥️  Frontend:  https://$frontend_url"
        echo "🔗 Name API:  https://$frontend_url/api/name"
        echo "📊 Info API:  https://$frontend_url/api/info"
    fi
    
    if [ "$backend_url" != "Route not found" ]; then
        echo "⚙️  Backend:   https://$backend_url"
    fi
    
    echo ""
    echo "📝 Note: It may take a few minutes for the routes to become fully accessible."
}

# Function to show deployment status
show_status() {
    echo "📊 Deployment Status:"
    echo "=================================================="
    
    echo "🏗️ Pods:"
    oc get pods -l app=eemeli-demo
    
    echo ""
    echo "🔗 Services:"
    oc get services -l app=eemeli-demo
    
    echo ""
    echo "🌐 Routes:"
    oc get routes -l app=eemeli-demo
    
    echo ""
    echo "📈 Horizontal Pod Autoscalers:"
    oc get hpa -l app=eemeli-demo
}

# Main deployment function
main() {
    echo "Eemeli Karjalainen - Personal CSC Rahti Demo"
    echo "Multi-container application deployment script"
    echo ""
    
    check_oc
    check_login
    setup_project
    
    case "${1:-deploy}" in
        "deploy")
            build_images
            deploy_application
            show_urls
            show_status
            ;;
        "status")
            show_status
            ;;
        "urls")
            show_urls
            ;;
        "build")
            build_images
            ;;
        "clean")
            echo "🧹 Cleaning up application resources..."
            oc delete all,routes,hpa -l app=eemeli-demo
            oc delete bc backend frontend 2>/dev/null || true
            echo "✅ Cleanup completed!"
            ;;
        *)
            echo "Usage: $0 [deploy|status|urls|build|clean]"
            echo ""
            echo "Commands:"
            echo "  deploy  - Full deployment (default)"
            echo "  status  - Show deployment status"
            echo "  urls    - Show application URLs"
            echo "  build   - Build images only"
            echo "  clean   - Clean up all resources"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
