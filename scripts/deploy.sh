#!/bin/bash

# Global variables
APP_NAME="mca-application-processor"
DOCKER_REPO="your-docker-repo"
KUBE_NAMESPACE="mca-system"

# Function to build Docker image
build_docker_image() {
    echo "Building Docker image..."
    
    # Build Docker image using docker build command
    docker build -t ${DOCKER_REPO}/${APP_NAME}:latest .
    
    # Tag the image with the Docker repository and version
    docker tag ${DOCKER_REPO}/${APP_NAME}:latest ${DOCKER_REPO}/${APP_NAME}:$(git rev-parse --short HEAD)
    
    # Print success or failure message
    if [ $? -eq 0 ]; then
        echo "Docker image built successfully."
    else
        echo "Failed to build Docker image."
        exit 1
    fi
}

# Function to push Docker image to the repository
push_docker_image() {
    echo "Pushing Docker image to repository..."
    
    # Push the Docker image to the repository using docker push command
    docker push ${DOCKER_REPO}/${APP_NAME}:latest
    docker push ${DOCKER_REPO}/${APP_NAME}:$(git rev-parse --short HEAD)
    
    # Print success or failure message
    if [ $? -eq 0 ]; then
        echo "Docker image pushed successfully."
    else
        echo "Failed to push Docker image."
        exit 1
    fi
}

# Function to update Kubernetes deployment with the new image
update_kubernetes_deployment() {
    echo "Updating Kubernetes deployment..."
    
    # Set the new image for the deployment using kubectl set image command
    kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_REPO}/${APP_NAME}:$(git rev-parse --short HEAD) -n ${KUBE_NAMESPACE}
    
    # Wait for the rollout to complete using kubectl rollout status command
    kubectl rollout status deployment/${APP_NAME} -n ${KUBE_NAMESPACE}
    
    # Print success or failure message
    if [ $? -eq 0 ]; then
        echo "Kubernetes deployment updated successfully."
    else
        echo "Failed to update Kubernetes deployment."
        exit 1
    fi
}

# Function to run database migrations
run_database_migrations() {
    echo "Running database migrations..."
    
    # Create a temporary pod for running migrations
    kubectl run ${APP_NAME}-migrations --image=${DOCKER_REPO}/${APP_NAME}:$(git rev-parse --short HEAD) -n ${KUBE_NAMESPACE} --restart=Never -- sleep infinity
    
    # Wait for the pod to be ready
    kubectl wait --for=condition=ready pod/${APP_NAME}-migrations -n ${KUBE_NAMESPACE} --timeout=60s
    
    # Execute alembic upgrade command inside the pod
    kubectl exec ${APP_NAME}-migrations -n ${KUBE_NAMESPACE} -- alembic upgrade head
    
    # Delete the temporary pod
    kubectl delete pod ${APP_NAME}-migrations -n ${KUBE_NAMESPACE}
    
    # Print success or failure message
    if [ $? -eq 0 ]; then
        echo "Database migrations completed successfully."
    else
        echo "Failed to run database migrations."
        exit 1
    fi
}

# Main function to orchestrate the deployment process
main() {
    echo "Starting deployment process for ${APP_NAME}..."
    
    # Call build_docker_image function
    build_docker_image
    
    # Call push_docker_image function
    push_docker_image
    
    # Call update_kubernetes_deployment function
    update_kubernetes_deployment
    
    # Call run_database_migrations function
    run_database_migrations
    
    # Print overall success message
    echo "Deployment process completed successfully for ${APP_NAME}."
}

# Execute the main function
main