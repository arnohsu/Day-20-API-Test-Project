pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip setuptools wheel
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask in Background') {
            steps {
                sh '''
                    nohup ./venv/bin/python api.py > flask.log 2>&1 &
                    sleep 5
                '''
            }
        }

        stage('Run pytest Tests') {
            steps {
                sh '''
                    ./venv/bin/pytest --junitxml=pytest-results.xml || true
                '''
            }
        }

        stage('Run Newman Tests') {
            steps {
                sh '''
                    newman run postman_collection.json \
                        -e postman_environment.json \
                        --reporters cli,junit \
                        --reporter-junit-export newman-results.xml || true
                '''
            }
        }

        stage('Collect Results') {
            steps {
                junit 'pytest-results.xml'
                junit 'newman-results.xml'
            }
        }
    }

    post {
        always {
            sh 'pkill -f api.py || true'
            archiveArtifacts artifacts: '*.xml', fingerprint: true
        }
    }
}
