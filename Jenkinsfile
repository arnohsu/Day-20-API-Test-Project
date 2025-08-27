pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/arnohsu/Day-20-API-Test-Project.git', credentialsId: 'gmail-credentials'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    # 建立虛擬環境（若已存在則更新套件即可）
                    python3 -m venv venv
                    . venv/bin/activate

                    # 安裝需求套件（不升級 pip 避免 PEP 668）
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
                    # 直接指定你現有的 test_api.py
                    pytest test_api.py --junitxml=pytest-results.xml --html=reports/report.html --self-contained-html
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

