pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/arnohsu/Day-20-API-Test-Project
'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask in Background') {
            steps {
                sh '''
                    . venv/bin/activate
                    nohup python api.py > flask.log 2>&1 &
                    sleep 3
                '''
            }
        }

        stage('Run pytest Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v --junitxml=pytest-results.xml
                '''
            }
        }

        stage('Run Newman Tests') {
            steps {
                sh '''
                    newman run collection.json --reporters cli,junit --reporter-junit-export newman-results.xml
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
}
