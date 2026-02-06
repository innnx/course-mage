pipeline {
    agent any

    environment {
        IMAGE_NAME = "course-app"
        DOCKER_COMPOSE = "/usr/local/bin/docker-compose"
    }

    stages {

        stage('拉取代码') {
            steps {
                checkout scm
            }
        }

        stage('编译环境检查') {
            steps {
                sh 'chmod +x mvnw'
                sh 'java -version'
                sh './mvnw -version'
            }
        }

        stage('后端打包') {
            steps {
                sh 'chmod +x mvnw'
                sh './mvnw clean package -DskipTests'
            }
        }

        stage('前端打包') {
            steps {
                dir('frontend-vue') {
                    // sh 'npm install && npm run build'
                    echo '跳过前端打包，假设 dist 已存在或已在 Dockerfile 中处理'
                }
            }
        }

        stage('构建Docker镜像') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
                sh 'docker build -t course-frontend:latest ./frontend-vue'
            }
        }

        stage('部署服务') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d'
                sh 'docker image prune -f'
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
