pipeline {
    agent { label 'controler' }
    stages {
        stage('Build') {
            steps {
                sh """python main2.py"""
            }

        }
    }
}