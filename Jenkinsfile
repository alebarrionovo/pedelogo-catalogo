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
                        '-f Dockerfile .')                  
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
        stage ('Deploy Kubernetes') {
            agent {
                kubernetes {
                    cloud 'kubernetes'
                }
            }
            environment {
                tag_version = "${env.BUILD_ID}"
            }
            steps {             
                script {
                    sh 'sed -i "s/{{TAG}}/$tag_version/g" k8s/deployment.yaml'
                    sh 'cat k8s/deployment.yaml'
                    kubernetesDeploy(configs: '**k8s/**', kubeconfigId: 'kubeconfig')
                    } 
                }
        }        
    }
}
