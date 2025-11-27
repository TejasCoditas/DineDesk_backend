pipeline {
    agent { label "new-bond-agent" }

    environment {
        AWS_REGION = "ap-south-1"
        ECR_REPO   = credentials('aws_ecr_repo_name') 
        CONTAINER_NAME = "restaurant_reviews_backend"
    }

    stages {

        stage('Checkout') {
            steps {
                script {
                    def commit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.COMMIT_ID = commit
                    env.IMAGE_TAG = "build-${env.BUILD_NUMBER}-${commit}"
                    echo "Commit ID: ${commit}"
                    echo "Image Tag: ${env.IMAGE_TAG}"
                }
            }
        }

    
        stage('Build & Push to ECR') {
            steps {
                withCredentials([string(credentialsId: 'aws_ecr_repo_name', variable: 'ECR_REPO')]) {
                    sh '''
                        export PATH=$PATH:/usr/local/bin

                        echo "Login to ECR"
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin $ECR_REPO

                        echo "Building Image: $IMAGE_TAG"
                        docker build -t $ECR_REPO:${IMAGE_TAG} .

                        echo "Pushing image"
                        docker push $ECR_REPO:${IMAGE_TAG}

                        echo "Tag & push latest"
                        docker tag $ECR_REPO:${IMAGE_TAG} $ECR_REPO:latest
                        docker push $ECR_REPO:latest
                    '''
                }
            }
        }


        stage('Update Lambda Image') {
            steps {
                sh """
                    echo "Updating Lambda to ${IMAGE_TAG}"

                    aws lambda update-function-code \
                        --function-name dine_desk_backend \
                        --image-uri ${ECR_REPO}:${IMAGE_TAG} --region ${AWS_REGION}
                """
            }
        }

    }

    post {
        success {
            googlechatnotification(
                url: "id:gchat-jenkins-webhook",
                message: "${env.JOB_NAME} #${env.BUILD_NUMBER}-${COMMIT_ID} SUCCESS"
            )
        }
        failure {
            googlechatnotification(
                url: "id:gchat-jenkins-webhook",
                message: "${env.JOB_NAME} #${env.BUILD_NUMBER}-${COMMIT_ID} FAILED"
            )
        }
    }
}
