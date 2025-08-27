pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                git url: 'https://github.com/arnohsu/Day-20-API-Test-Project.git', 
                    credentialsId: 'gmail-credentials', 
                    branch: 'main'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    # 刪掉舊 venv
                    rm -rf venv

                    # 建立虛擬環境
                    python3 -m venv venv
                    . venv/bin/activate

                    # 安裝 pip、setuptools、wheel
                    python -m pip install --upgrade pip==24.0 setuptools wheel

                    # 安裝專案依賴
                    python -m pip install -r requirements.txt

                    # 安裝 pytest-html（固定版本）
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
                    pytest tests/ --junitxml=reports/results.xml --html=reports/report.html --self-contained-html
                '''
            }
        }

        stage('Run Newman Tests') {
            steps {
                sh '''
                    newman run postman_collection.json -e postman_environment.json -r cli,html --reporter-html-export reports/newman_report.html
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. Flask will auto exit if nohup closes.'
        }
    }
}
