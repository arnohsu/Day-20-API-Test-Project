pipeline {
    agent any
    environment {
        VENV_NAME = "venv_jenkins"
    }
    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Setup Environment') {
            steps {
                sh """
                rm -rf ${VENV_NAME}
                python3 -m venv ${VENV_NAME}
                . ${VENV_NAME}/bin/activate
                pip install --upgrade pip setuptools wheel --break-system-packages
                pip install -r requirements.txt
                """
            }
        }
        stage('Run Flask in Background') {
            steps {
                sh """
                . ${VENV_NAME}/bin/activate
                nohup python api.py &
                sleep 3
                """
            }
        }
        stage('Run pytest Tests') {
            steps {
                sh """
                . ${VENV_NAME}/bin/activate
                pytest -v --junitxml=${WORKSPACE}/pytest-results.xml
                """
            }
        }
        stage('Run Newman Tests') {
            steps {
                sh """
                newman run collection.json --reporters cli,junit --reporter-junit-export ${WORKSPACE}/newman-results.xml
                """
            }
        }
        stage('Collect Results') {
            steps {
                junit allowEmptyResults: true, testResults: "${WORKSPACE}/pytest-results.xml"
                junit allowEmptyResults: true, testResults: "${WORKSPACE}/newman-results.xml"
            }
        }
    }
    post {
        always {
            echo "Pipeline finished. Flask will auto exit if nohup closes."
        }
    }
}

