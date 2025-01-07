pipeline {
    agent any
    
    stages {
        stage('Cloning from Github') {
            steps {
                script {
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/COURSE-TESTING-1.git']])
                }
            }
        }
    }
}