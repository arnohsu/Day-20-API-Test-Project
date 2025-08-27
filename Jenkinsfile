pipeline {
    agent any

    environment {
        VENV_DIR = "venv_jenkins"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/arnohsu/Day-20-API-Test-Project.git',
                    credentialsId: 'gmail-credentials'
            }
        }

        stage('Setup Environment') {
            steps {
                sh """
                    # 刪掉舊 venv_jenkins
                    rm -rf \$VENV_DIR

                    # 建立獨立虛擬環境
                    python3 -m venv \$VENV_DIR

                    # 啟用虛擬環境
                    . \$VENV_DIR/bin/activate

                    # 安裝專案依賴
                    pip install --upgrade pip setuptools wheel --break-system-packages
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Flask in Background') {
            steps {
                sh """
                    . \$VENV_DIR/bin/activate
                    nohup python api.py > flask.log 2>&1 &
                    sleep 3
                """
            }
        }

        stage('Run pytest Tests') {
            steps {
                sh """
                    . \$VENV_DIR/bin/activate
                    pytest -v --junitxml=pytest-results.xml
                """
            }
        }

        stage('Run Newman Tests') {
            steps {
                sh """
                    newman run collection.json --reporters cli,junit --reporter-junit-export newman-results.xml
                """
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

