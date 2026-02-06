pipeline {
    agent any

    environment {
        IMAGE_NAME = "course-app"
    }

    stages {

        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('后端打包') {
            steps {
                sh 'chmod +x mvnw'
                sh './mvnw clean package -DskipTests'
            }
        }

        stage('构建Docker镜像') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('部署服务') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }

    }

    post {
        success {
            echo '部署成功'
        }
        failure {
            echo '部署失败'
        }
    }
}
