pipeline {
    
    agent {
        label 'jenkins_test'
    }

    // options {
    //     // This is required if you want to clean before build with the "Workspace Cleanup Plugin"
    //     skipDefaultCheckout(true)
    // }

    environment {
        SONARQUBE_URL = 'https://sonarqube.my_company.com'
        SONAR='/sonar-scanner-4.6.2.2472-linux/bin/sonar-scanner'
        BUILD_WRAPPER='/build-wrapper-linux-x86/build-wrapper-linux-x86-64'
        // Mend Whitesource
        WS_HOME = "/opt/"
        WS_APIKEY = credentials('mend_apikey')
        WS_USERKEY = credentials('mend_userkey')
        WS_PROJECTNAME = "${JOB_NAME}"
        WS_PROJECTPERFOLDERINCLUDES = "../cxx"
        WS_INCLUDES = "**/*.c;**/*.cc;**/*.cp;**/*.cpp;**/*.cxx;**/*.c++;**/*.h;**/*.hpp;**/*.hxx"
    }    

    stages {
        stage('C++ Build') {
            agent {
                dockerfile {
                    dir './'
                    filename 'Dockerfile.cxx'
                    reuseNode true
                }
            }
            steps {
                sh """
                  cd ../cxx/
                  pwd
                  ls -l
                  mkdir build
                  cd build
                  cmake ..       
                  ${BUILD_WRAPPER} --out-dir bw-output make gcov
                """
            }
        }

        stage('C++ SonarQube Analysis') {
            agent {
                dockerfile {
                    dir '.jenkins'
                    filename 'Dockerfile.cxx'
                    reuseNode true
                    args '--volume sonar:/home/jenkins/.sonar/'
                }
            }
            steps {
                script {
                    withSonarQubeEnv("sonarqube") {
                        sh """
                        cd ../cxx/
                        pwd
                        ls -l
                        ${SONAR} -Dsonar.branch.name=${env.BRANCH_NAME} -X
                        """
                    }
                }
            }
        }
        stage('Download and Run Mend Unified Agent') {
            agent {
                dockerfile {
                    dir './'
                    filename 'Dockerfile.cxx'
                    args '--user root'
                    reuseNode true
                }
            }
            steps {
                // sh 'curl -LJO https://unified-agent.s3.amazonaws.com/wss-unified-agent.jar'
                sh "java -jar ${WS_HOME}wss-unified-agent.jar" 
            }
        }
    }
    post {
        always {
            // Always delete the workspace
            cleanWs()
        }
    }
}