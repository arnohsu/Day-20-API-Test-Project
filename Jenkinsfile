pipeline {
    agent any

    environment {
        REPORT_DIR = "reports"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/arnohsu/Day-20-API-Test-Project.git', credentialsId: 'gmail-credentials'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip setuptools wheel
                    python -m pip install -r requirements.txt
                    python -m pip install pytest-html==4.1.1
                '''
            }
        }

        stage('Run Flask in Background') {
            steps {
                sh '''
                    . venv/bin/activate
                    nohup python api.py &
                '''
            }
        }

        stage('Run pytest Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=${REPORT_DIR}/results.xml --html=${REPORT_DIR}/report.html --self-contained-html || true
                '''
            }
        }

        stage('Run Newman Tests') {
            steps {
                sh '''
                    newman run postman_collection.json -r cli,html --reporter-html-export ${REPORT_DIR}/newman.html || true
                '''
            }
        }

        stage('Collect Results') {
            steps {
                junit "${REPORT_DIR}/results.xml"
                archiveArtifacts artifacts: "${REPORT_DIR}/*.html", fingerprint: true
            }
        }
    }
}
