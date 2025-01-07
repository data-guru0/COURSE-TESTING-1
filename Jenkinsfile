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

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-service-account-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Setting up Google Cloud SDK and pushing Docker image to GCR...'
                        sh '''
                            # Clean up any existing Google Cloud SDK directory
                            if [ -d "/var/jenkins_home/google-cloud-sdk" ]; then
                                echo "Removing old Google Cloud SDK directory..."
                                rm -rf /var/jenkins_home/google-cloud-sdk
                            fi

                            # Install Google Cloud SDK
                            curl https://sdk.cloud.google.com | bash -s -- --disable-prompts --install-dir=/var/jenkins_home
                            export PATH=/var/jenkins_home/google-cloud-sdk/bin:$PATH

                            # Authenticate with Google Cloud
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}

                            # Build, tag, and push Docker image
                            docker build -t ${DOCKERHUB_REPOSITORY}:latest .
                            docker tag ${DOCKERHUB_REPOSITORY}:latest gcr.io/${GCP_PROJECT}/course-testing:latest
                            docker push gcr.io/${GCP_PROJECT}/course-testing:latest
                        '''
                    }
                }
            }
        }
    }
}
