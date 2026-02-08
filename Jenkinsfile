pipeline {
    agent any

    environment {
        IMAGE_NAME = "course-app"
        // 这里的物理路径必须与 docker run 命令中的映射一致
        HOST_WORKSPACE = "/home/kafka/jenkins_workspace/${JOB_NAME}"
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

        stage('构建Docker镜像') {
            steps {
                // 构建后端镜像
                sh 'docker build -t ${IMAGE_NAME}:latest .'
                // 构建前端镜像 (Dockerfile 会在容器内执行构建，无需宿主机 node)
                sh 'docker build -t course-frontend:latest ./frontend-vue'
            }
        }

        stage('部署服务') {
            steps {
                sh '''
                # 1. 预防性清理：如果 init.sql 意外变成了文件夹，直接删掉
                [ -d "init.sql" ] && rm -rf init.sql
                
                # 2. 准备 docker-compose
                if [ ! -f "./docker-compose" ]; then
                    curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o ./docker-compose
                    chmod +x ./docker-compose
                fi
                
                # 3. 停止并启动服务 (--remove-orphans 确保清理干净)
                ./docker-compose down --remove-orphans
                ./docker-compose up -d
                
                # 4. 打印状态
                docker ps
                '''
            }
        }

        stage('自动化接口测试') {
            steps {
                dir('coursehub-auto-test') {
                    sh '''
                    # 1. 动态生成测试用的 Dockerfile (解决 requirements.txt 路径问题)
                    cat <<EOF > Test.Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD ["pytest", "--env=prod", "--alluredir=./allure-results"]
EOF

                    # 2. 构建临时测试镜像
                    docker build -t course-test-runner -f Test.Dockerfile .
                    
                    # 3. 运行测试（将结果映射回宿主机，方便后续查看报告）
                    rm -rf allure-results && mkdir allure-results
                    docker run --rm \
                        --network coursehub_course-network \
                        -v ${HOST_WORKSPACE}/coursehub-auto-test/allure-results:/app/allure-results \
                        course-test-runner || true
                    '''
                }
            }
        }
    }

    post {
        always {
            // 注意：因为我们映射了物理路径，清理工作区会删除宿主机上的代码
            // 如果你想保留代码方便调试，可以暂时注释掉 cleanWs()
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