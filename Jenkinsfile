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

        stage('编译环境检查') {
            steps {
                sh 'chmod +x mvnw'
                sh 'java -version'
                sh './mvnw -version'
            }
        }

        stage('后端打包') {
            steps {
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
                sh '''
                if [ ! -f "./docker-compose" ]; then
                    curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o ./docker-compose
                    chmod +x ./docker-compose
                fi
                ./docker-compose up -d
                docker image prune -f
                docker ps
                '''
            }
        }

        stage('自动化接口测试') {
            steps {
                dir('coursehub-auto-test') {
                    // 使用 python 镜像运行测试，这样不需要在服务器手动装 python 环境
                    sh '''
                    rm -rf allure-results && mkdir allure-results
                    # 创建一个名为 python_cache 的 Docker 卷（如果不存在）
                    docker volume create python_test_cache || true

                    docker run --rm --network coursehub_course-network \
                        -v $(pwd):/app \
                        -v python_test_cache:/root/.cache/pip \
                        -w /app python:3.10-slim \
                        sh -c "pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
                        pytest --env=prod --alluredir=./allure-results" || true 
                    '''
                }
            }
        }

    }

    post {
        always {
            // 读取 coursehub-auto-test/allure-results 下的数据生成报告
            // allure includeProperties: false, jdk: '', results: [[path: 'coursehub-auto-test/allure-results']]
            cleanWs()
        }
        success {
            echo '部署成功'
        }
        failure {
            echo '部署失败'
        }
    }
}
