pipeline {
    agent any
    environment { 
        repository = "shurikby.jfrog.io/final-docker/wmp/$BRANCH_NAME" 
        dockerImage = ''
        DBPASS = credentials('github')
    }
    stages {
        stage('Build docker image') {
            steps {
                script {
                    dockerImage = docker.build repository + ":$BUILD_NUMBER" 
                }
            }
        }
        stage('Store image on artifactory') {
            steps {
                script {
                    docker.withRegistry('https://shurikby.jfrog.io', 'artifactory' ) { 
                        dockerImage.push("$BUILD_NUMBER") 
                        dockerImage.push("latest") 
                    }
                }
            }
        }
        stage('Prepare cluster enviroment') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'kubectl', serverUrl: 'https://192.168.1.16:6443']) {
                        sh 'envsubst < k8s/env-prep.yaml | kubectl apply -f -'
                    }
                }
            }
        }
        stage('Deploy application') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'kubectl', serverUrl: 'https://192.168.1.16:6443']) {
                        sh 'envsubst < k8s/deploy.yaml | kubectl apply -f -'
                        sh 'kubectl rollout status deployment wmp -n wmp'
                    }
                }
            }
        }
    }
	post{
		success {
			echo "Success"
		}
		failure {
			echo "There was some error"
		} 
		cleanup {
			deleteDir() // cleaning up working directory
		} 
    }
}
