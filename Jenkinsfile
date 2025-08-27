pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/arnohsu/Day-20-API-Test-Project.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest-html==4.1.1
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
                    # 直接抓目前目錄下的 test_*.py 檔案，不用 tests/ 資料夾
                    pytest test_api.py --junitxml=pytest-results.xml --html=pytest-report.html --self-contained-html
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

    post {
        always {
            echo 'Pipeline finished. Flask will auto exit if nohup closes.'
        }
    }
}

