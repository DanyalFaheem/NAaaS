pipeline {
  agent any  
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub')
  }
    stages {
    stage('Build') {
        steps {
        sh script:"""
        #!/bin/bash
        cd Spark/Updated
        ls
        sudo docker build -t my-spark-image .
        """
        }
    }
    stage('Login') {
        steps {
        sh 'sudo echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
        }
    }
    stage('Push') {
        steps {
        sh 'sudo docker tag my-spark-image danyalfaheem/my-spark-image'
        sh 'sudo docker push danyalfaheem/my-spark-image'
        }
    }
    stage('Execute') {
        steps {
        sh script:"""
        #!/bin/bash
        cd Spark/Updated
        ls
        sudo docker-compose up
        """
        }
    }
  }
}
