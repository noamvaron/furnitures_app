pipeline {
    agent {
        kubernetes {
            label "furniture-agent"
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'dind'
        }
    }

    environment {
        DOCKER_IMAGE = 'noamva96/furnitures_app'
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_REPO = 'noamvaron/furnitures_app'
        GITHUB_TOKEN = credentials('github-creds')
    }

    stages {
        stage("Checkout code") {
            steps {
                checkout scm
            }
        }

        stage("Set up Docker Buildx and QEMU") {
            steps {
                container('dind') {
                    script {
                        // Install QEMU and register
                        sh 'docker run --rm --privileged multiarch/qemu-user-static --reset -p yes'
                        // Ensure QEMU setup completes successfully
                        sh 'docker run --rm --privileged multiarch/qemu-user-static:register --reset'
                        
                        // Set up Docker Buildx
                        sh 'docker buildx create --use --name multiarch_builder || true'
                        sh 'docker buildx inspect --bootstrap'
                    }
                }
            }
        }

        stage("Build multi-architecture Docker image") {
            steps {
                container('dind') {
                    script {
                        dockerImage = sh(returnStdout: true, script: """
                            docker buildx build --platform linux/amd64,linux/arm64 --push -t ${DOCKER_IMAGE}:latest .
                        """).trim()
                    }
                }
            }
        }

        stage("Unit Test") {
            steps {
                container('docker-compose') {
                    script {
                        sh "docker-compose -f docker-compose.yaml up --build -d"
                        sh "docker-compose -f docker-compose.yaml run test"
                        sh "docker-compose -f docker-compose.yaml down"
                    }
                }
            }
        }

        stage('Push Docker image') {
            when {
                branch 'main'
            }
            steps {
                container('dind') {
                    script {
                        docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                            sh 'docker buildx build --platform linux/amd64,linux/arm64 --push -t ${DOCKER_IMAGE}:latest .'
                        }
                    }
                }
            }
        }

        stage('Create merge request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                container('dind') {
                    withCredentials([string(credentialsId: 'github-creds', variable: 'GITHUB_TOKEN')]) {
                        script {
                            def branchName = env.BRANCH_NAME
                            def pullRequestTitle = "Merge ${branchName} into main"
                            def pullRequestBody = "Automatically generated merge request for branch ${branchName}"

                            sh """
                                curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                                -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "main" }' \
                                ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                            """
                        }
                    }
                }
            }
        }
    }
}