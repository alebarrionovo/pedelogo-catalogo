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
                        '-f ./src/PedeLogo.Catalogo.Api/Dockerfile .')                                          
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
        stage('Deploy') {
            steps {
                script {
                    kubernetesDeploy(
                        sh 'cat ./src/PedeLogo.Catalogo.Api/k8s/mongodb/deployment.yaml'
                        kubeconfigId: 'kube', // ID do Kubeconfig armazenado no Jenkins
                        configs: './src/PedeLogo.Catalogo.Api/k8s/mongodb/**', // Caminho para os arquivos YAML do Kubernetes                        
                    )
                }
            }       
        }
    }
}