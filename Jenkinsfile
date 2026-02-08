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
                sh './mvnw clean package -DskipTests -s settings.xml'
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
                    # 直接构建镜像，Docker 会自动寻找目录下的 Dockerfile
                    docker build -t course-test-runner .
                    
                    # 清理并创建结果目录
                    rm -rf allure-results && mkdir allure-results
                    
                    # 运行测试
                    docker run --rm \
                        --network coursehub_course-network \
                        -v /home/kafka/jenkins_workspace/coursehub/coursehub-auto-test/allure-results:/app/allure-results \
                        course-test-runner || true
                    '''
                }
            }
        }
    }

    post {
        always {
            // 注意：因为我们映射了物理路径，清理工作区会删除宿主机上的代码
            //cleanWs()
            echo '暂保留工作区'
        }
        success {
            echo '部署成功'
        }
        failure {
            echo '部署失败'
        }
    }
}