pipeline {
    agent any

    environment {
        VENV_DIR = 'venv' // Directory for the virtual environment
        DOCKERHUB_CREDENTIAL_ID = 'dockerhub-token'
        DOCKERHUB_REPOSITORY = 'dataguru97/course-testing'
        GCP_PROJECT = 'vocal-antler-447107-i9' // Replace with your GCP project ID
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

        stage('Linting Code') {
            steps {
                script {
                    echo 'Linting Python code...'
                    sh '''
                        set -e
                        . ${VENV_DIR}/bin/activate
                        pylint application.py pipeline/training_pipeline.py || echo "Pylint completed with issues."
                        flake8 application.py pipeline/training_pipeline.py --ignore=E501,E302 || echo "Flake8 completed with issues."
                        black application.py pipeline/training_pipeline.py || echo "Black formatting completed."
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }

        stage('Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-service-account-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Setting up Google Cloud SDK and pushing Docker image to GCR...'
                        sh '''
                            # Install and configure Google Cloud SDK
                            curl https://sdk.cloud.google.com | bash -s -- --disable-prompts
                            export PATH=$HOME/google-cloud-sdk/bin:$PATH

                            # Authenticate with Google Cloud
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}

                            # Tag and push Docker image to Google Container Registry
                            docker tag ${DOCKERHUB_REPOSITORY}:latest gcr.io/${GCP_PROJECT}/course-testing:latest
                            docker push gcr.io/${GCP_PROJECT}/course-testing:latest
                        '''
                    }
                }
            }
        }
    }
}
