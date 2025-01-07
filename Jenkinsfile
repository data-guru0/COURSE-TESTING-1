pipeline {
    agent any

    environment {
        VENV_DIR = 'venv' // Directory for the virtual environment
        DOCKERHUB_CREDENTIAL_ID = 'dockerhub-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'dataguru97/course-testing'

        GCP_PROJECT = 'vocal-antler-447107-i9' // Replace with your GCP project ID
        GCP_REGION = 'us-central1'          // e.g., us-central1
        GCP_ZONE = 'us-central1-a'          // e.g., us-central1-a
        GOOGLE_APPLICATION_CREDENTIALS = 'vocal-antler-447107-i9-477919f97886.json'
    }

    stages {
        stage('Cloning from Github') {
            steps {
                script {
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/COURSE-TESTING-1.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setting up virtual environment'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Linting Code') {
            steps {
                script {
                    echo 'Linting Python Code...'
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate
                        pylint application.py pipeline/training_pipeline.py --output=pylint-report.txt --exit-zero || echo "Pylint completed with issues."
                        flake8 application.py pipeline/training_pipeline.py --ignore=E501,E302 --output-file=flake8-report.txt || echo "Flake8 completed with issues."
                        black application.py pipeline/training_pipeline.py || echo "Black formatting completed."
                    '''
                }
            }
        }

        stage('Trivy FS Scan') {
            steps {
                // Trivy Filesystem Scan
                script {
                    echo 'Scanning Filesystem with Trivy...'
                    sh "trivy fs ./ --format table -o trivy-fs-report.html"
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest") 
                }
            }
        }

        stage('Trivy Docker Image Scan') {
            steps {
                script {
                    echo 'Scanning Docker Image with Trivy...'
                    sh "trivy image ${DOCKERHUB_REPOSITORY}:latest --format table -o trivy-image-report.html"
                }
            }
        }

        stage('Push Docker Image to GCR') {
            steps {
                script {
                    echo 'Pushing Docker Image to Google Container Registry...'
                sh '''
                    # Install Google Cloud SDK temporarily for the pipeline run
                    curl https://sdk.cloud.google.com | bash
                    exec -l $SHELL

                    # Authenticate with Google Cloud
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    
                    # Tag the Docker image for Google Container Registry (GCR)
                    docker tag ${DOCKERHUB_REPOSITORY}:latest gcr.io/${GCP_PROJECT}/course-testing:latest
                    
                    # Push the image to GCR
                    docker push gcr.io/${GCP_PROJECT}/course-testing:latest
                '''
                }
            }
        }
    }
}
