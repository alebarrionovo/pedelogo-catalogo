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
        stage('Deploy Kubernetes') {
            environment {
               // Variavel KUBECONFIG com o caminho para o arquivo kubeconfig com as credenciais do cluster Kubernetes dentro da maquina do jenkins
               KUBECONFIG = "/home/ubuntu/.kube/config" 
               // variavel tag_version contendo Id do build.
               tag_version = "${env.BUILD_ID}"
            }
            steps {
                script {                                   
                    // Execute o comando kubectl apply passando o caminho do mongodb como todos yamls utilizando o variavel kubeconfig
                    sh 'kubectl apply -f src/PedeLogo.Catalogo.Api/k8s/mongodb/ --kubeconfig=${KUBECONFIG}'
                    // Execute o comando kubectl apply passando o caminho da api menos o deployment, utilizando o variavel kubeconfig
                    sh 'kubectl apply -f src/PedeLogo.Catalogo.Api/k8s/api/ --kubeconfig=${KUBECONFIG}'
                    // Colocar o codigo do build na varivel tag, alterando o deployment da api
                    sh 'sed -i "s/{{TAG}}/$tag_version/g" src/PedeLogo.Catalogo.Api/k8s/api/deployment/deployment.yaml'
                    // Execute o comando kubectl apply passando o caminho do deployment da api após alteração da variavel tag, utilizando o variavel kubeconfig
                    sh 'kubectl apply -f src/PedeLogo.Catalogo.Api/k8s/api/deployment/deployment.yaml --kubeconfig=${KUBECONFIG}'
                }
            }
        }
    }
}