pipeline {
    agent any

    stages {
        stage ('Checkout Source') {
            steps {
                git url: 'https://github.com/alebarrionovo/pedelogo-catalogo.git', branch: 'main'              
            }
        }
        stage ('Build Image') {
            steps {
                script {
                    dockerapp = docker.build("alebarrionovo/pedelogo-catalogo:${env.BUILD_ID}", 
                        '-f src/PedeLogo.Catalogo.Api/Dockerfile .')
                }
            }
        }
        stage ('Push Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub'){
                    dockerapp.push('latest')
                    dockerapp.push("${env.BUILD_ID}")
                    } 
                }
            }
        }
        node {
            stage('Apply Kubernetes files') {
                withKubeConfig([credentialsId: 'kube', serverUrl: 'https://api.k8s.192.168.64.2']) {
                sh 'kubectl apply -f src/PedeLogo.Catalogo.Api/k8s/mongodb/deployment.yaml'
                }
            }
        }
    }
}