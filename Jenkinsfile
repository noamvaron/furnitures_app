pipeline{
    agent{
        kubernetes{
            label "furniture-agent"
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'dind'
        }
    }
 
    environment{
        DOCKER_IMAGE = 'noamva96/furnitures_app'
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_REPO = 'noamvaron/furnitures_app'
        GITHUB_TOKEN = credentials('github-creds')
    }
 
    stages{
        stage("Checkout code"){
            steps {
                checkout scm
            }
        }
 
        stage("Build docker image"){
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                }
            }
        }
 
        stage("Unit Test"){
            steps{
                script {
                    sh "docker-compose -f docker-compose.yaml up --build -d"
                    sh "docker-compose -f docker-compose.yaml run test"
                    sh "docker-compose -f docker-compose.yaml down"
                }
            }
        }
 
        stage('Push Docker image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                        dockerImage.push("latest")
                    }
                }
            }
        }
 
        stage('Create merge request'){
            when {
                not {
                    branch 'main'
                }
            }
            steps {
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