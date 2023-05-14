pipeline {
  agent any  
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub')
  }
    stages {
    stage('Build') {
        steps {
        sh 'sudo docker build -t sentimentanalysis:latest .'
        }
    }
    stage('Login') {
        steps {
        sh 'sudo echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
        }
    }
    stage('Push') {
        steps {
        sh 'sudo docker tag sentimentanalysis:latest danyalfaheem/sentimentanalysis:latest'
        sh 'sudo docker push danyalfaheem/sentimentanalysis:latest'
        }
    }
    stage('Execute') {
        steps {
            sh 'sudo docker run -d -p 5000:5000/tcp -p 5000:5000/udp sentimentanalysis:latest'
        }
    }
  }
}
