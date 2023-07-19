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
        stage('Kubectl Apply') {
            environment {
               KUBECONFIG = "/home/ubuntu/.kube/config" // Caminho para o arquivo kubeconfig com as credenciais do cluster Kubernetes
            }
            steps {
                script {
                    // Faça o download do kubectl no Jenkins usando o plugin "Kubernetes CLI"
                    //def kubectl = tool 'kubectl'
                    
                    // Execute o comando kubectl apply usando o arquivo deployment.yaml
                    sh 'kubectl apply -f src/PedeLogo.Catalogo.Api/k8s/mongodb/ --kubeconfig=${KUBECONFIG}'
                }
            }
        }
    }
}