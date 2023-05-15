pipeline {
  agent any  
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub')
  }
    stages {
    stage('Build') {
        steps {
        sh 'sudo docker build -t my-spark-image .'
        }
    }
    stage('Login') {
        steps {
        sh 'sudo echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
        }
    }
    stage('Push') {
        steps {
        sh 'sudo docker tag sentimentanalysis:latest danyalfaheem/my-spark-image'
        sh 'sudo docker push danyalfaheem/my-spark-image'
        }
    }
    stage('Execute') {
        steps {
            sh 'sudo docker run -d sentimentanalysis:latest'
        }
    }
  }
}
