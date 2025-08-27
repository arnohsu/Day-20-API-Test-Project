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
                    . venv/bin/activate
                    pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask in Background') {
            steps {
                sh '''
                    . venv/bin/activate
                    nohup python app.py > flask.log 2>&1 &
                    sleep 5
                '''
            }
        }

        stage('Run pytest Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q --junitxml=pytest-results.xml
                '''
            }
        }

        stage('Run Newman Tests') {
            steps {
                sh '''
                    newman run collection.json -e environment.json --reporters cli,junit --reporter-junit-export newman-results.xml
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
            sh 'pkill -f app.py || true'
            archiveArtifacts artifacts: '*.xml', allowEmptyArchive: true
        }
    }
}
