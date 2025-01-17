pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        DOCKERHUB_CREDENTIAL_ID = 'dockerhub-token'
        GCP_PROJECT = 'vocal-antler-447107-i9'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'  // Path to gcloud binary
    }

    stages {
        stage('Cloning from GitHub') {
            steps {
                script {
                    echo 'Cloning from GitHub...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/COURSE-TESTING-1.git']])
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                script {
                    echo 'Setting up virtual environment...'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Authenticating with Google Cloud and pushing Docker image to GCR...'
                        sh '''
                            # Ensure gcloud is available in the PATH
                            export PATH=$PATH:${GCLOUD_PATH}

                            # Authenticate with Google Cloud using the service account
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}

                            # Configure Docker to authenticate with GCR
                            gcloud auth configure-docker --quiet

                            # Build and push the Docker image to both DockerHub and GCR
                            docker build -t gcr.io/${GCP_PROJECT}/course-testing:latest .
                            docker push gcr.io/${GCP_PROJECT}/course-testing:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Cloud Run') {
    steps {
        withCredentials([file(credentialsId: 'gcp-key-2', variable: 'GOOGLE_APPLICATION_CREDENTIALS1')]) {
            script {
                echo 'Deploying to Cloud Run...'
                sh '''
                    # Ensure gcloud is available in the PATH
                    export PATH=$PATH:${GCLOUD_PATH}

                    # Authenticate with Google Cloud using the service account
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS1}
                    gcloud config set project ${GCP_PROJECT}

                    # Deploy the Docker image to Cloud Run
                    gcloud run deploy course-testing \
                        --image=gcr.io/${GCP_PROJECT}/course-testing:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated
                '''
            }
        }
    }
}

        
    }
}