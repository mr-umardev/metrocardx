pipeline {
    agent any

    environment {
        // Placeholder values (will be overwritten in Prepare stage)
        BUILD_TS = ""
        LOG_DIR  = "C:\\tmp\\metrocardx-build"
    }

    options {
        timestamps()
    }

    stages {

        stage('Prepare') {
            steps {
                script {
                    // Create timestamp
                    env.BUILD_TS = new Date().format("yyyyMMdd-HHmmss")

                    echo "Generated Timestamp: ${env.BUILD_TS}"
                    echo "Log Directory: ${env.LOG_DIR}"

                    // Create log directory on Windows
                    bat """
                    if not exist "${env.LOG_DIR}" mkdir "${env.LOG_DIR}"
                    """
                }
            }
        }

        stage('Environment check: Python3') {
            steps {
                bat """
                echo Checking python3...
                where python
                python --version
                """
            }
        }

        stage('Build / Virtualenv') {
            steps {
                bat """
                python -m venv .venv
                call .venv\\Scripts\\activate
                python -m pip install --upgrade pip
                """
            }
        }

        stage('Test') {
            steps {
                bat """
                call .venv\\Scripts\\activate
                python -m unittest discover -v > test-output-${env.BUILD_TS}.log 2>&1
                copy /Y test-output-${env.BUILD_TS}.log "${env.LOG_DIR}\\"
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: "test-output-${env.BUILD_TS}.log", fingerprint: true
                }
            }
        }

        stage('Validate') {
            steps {
                bat """
                call .venv\\Scripts\\activate
                python -c "from recharge.recharge import calculate_received_amount; print('Validation OK')"
                """
            }
        }
    }

    post {
        always {
            echo "Build finished. Timestamp = ${env.BUILD_TS}"
        }
        failure {
            echo "Build failed!"
        }
    }
}
