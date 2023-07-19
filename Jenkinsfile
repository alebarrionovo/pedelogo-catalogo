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
               // Variavel KUBECONFIG com o caminho para o arquivo kubeconfig com as credenciais do cluster Kubernetes dentro da maquina do jenkins
               KUBECONFIG = "/home/ubuntu/.kube/config" 
            }
            steps {
                script {                                   
                    // Execute o comando kubectl apply passando o caminho do mongodb como todos yamls utiliznado o variavel kubeconfig
                    sh 'kubectl apply -f src/PedeLogo.Catalogo.Api/k8s/mongodb/ --kubeconfig=${KUBECONFIG}'
                    DEPLOY = sh 'sed -i "s/{{TAG}}/$tag_version/g" src/PedeLogo.Catalogo.Api/k8s/api/deployment.yaml'
                    // Execute o comando kubectl apply passando o caminho do api como todos yamls utiliznado o variavel kubeconfig
                    sh 'kubectl apply -f ${DEPLOY} --kubeconfig=${KUBECONFIG}'
                }
            }
        }
    }
}