pipeline {
  agent any

  // Keep default env variables, we'll set dynamic ones in 'Prepare' stage
  environment {
    // placeholders (will be overwritten in Prepare)
    BUILD_TS = ''
    LOG_DIR = ''
  }

  options {
    // keep build logs for some time (optional)
    timestamps()
    ansiColor('xterm')
  }

  stages {

    stage('Prepare') {
      steps {
        script {
          // timestamp used to avoid overwrites
          env.BUILD_TS = new Date().format("yyyyMMdd-HHmmss")
          if (isUnix()) {
            env.LOG_DIR = "/tmp/metrocardx-build"
          } else {
            // Windows: choose C:\tmp\metrocardx-build (make sure Jenkins agent has permission)
            env.LOG_DIR = "C:\\tmp\\metrocardx-build"
          }
          echo "BUILD_TS=${env.BUILD_TS}"
          echo "LOG_DIR=${env.LOG_DIR}"

          // create log dir
          if (isUnix()) {
            sh "mkdir -p ${env.LOG_DIR}"
          } else {
            bat "if not exist \"${env.LOG_DIR}\" mkdir \"${env.LOG_DIR}\""
          }
        }
      }
    }

    stage('Environment check: Python3') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              echo "Checking python3..."
              if command -v python3 >/dev/null 2>&1; then
                python3 --version
              elif command -v python >/dev/null 2>&1; then
                python --version
              else
                echo "Python3 not found" >&2
                exit 1
              fi
            '''
          } else {
            // Windows: try 'py -3' then 'python'
            bat '''
              echo Checking python3...
              where python >nul 2>&1
              if %ERRORLEVEL%==0 (
                python --version
              ) else (
                py -3 --version >nul 2>&1
                if %ERRORLEVEL%==0 (
                  py -3 --version
                ) else (
                  echo Python3 not found
                  exit /b 1
                )
              )
            '''
          }
        }
      }
    }

    stage('Build / Virtualenv') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              python3 -m venv .venv || python -m venv .venv
              . .venv/bin/activate
              pip install --upgrade pip
              pip install -r requirements.txt 2>/dev/null || true
            '''
          } else {
            // Windows
            bat '''
              REM create venv
              python -m venv .venv
              call .venv\\Scripts\\activate
              python -m pip install --upgrade pip
              if exist requirements.txt (
                pip install -r requirements.txt
              )
            '''
          }
        }
      }
    }

    stage('Test') {
      steps {
        script {
          // Run tests and tee output into a timestamped log in workspace and copy to LOG_DIR
          if (isUnix()) {
            sh """
              . .venv/bin/activate || true
              python -m unittest discover -v | tee test-output-${env.BUILD_TS}.log
              cp test-output-${env.BUILD_TS}.log ${env.LOG_DIR}/
            """
          } else {
            bat """
              call .venv\\Scripts\\activate
              python -m unittest discover -v > test-output-${env.BUILD_TS}.log 2>&1
              copy /Y test-output-${env.BUILD_TS}.log "${env.LOG_DIR}\\"
            """
          }
        }
      }
    }

    stage('Validate') {
      steps {
        script {
          // Example validation step: run a tiny smoke script that imports the module
          if (isUnix()) {
            sh """
              . .venv/bin/activate || true
              python - <<'PY'
import sys
try:
    from recharge.recharge import calculate_received_amount
except Exception as e:
    print("Import/validation failed:", e)
    sys.exit(2)
print("Validation OK")
PY
            """
          } else {
            bat """
              call .venv\\Scripts\\activate
              python - <<PY
import sys
try:
    from recharge.recharge import calculate_received_amount
except Exception as e:
    print("Import/validation failed:", e)
    sys.exit(2)
print("Validation OK")
PY
            """
          }
        }
      }
    }

    stage('Archive logs & artifacts') {
      steps {
        script {
          // Archive test logs with timestamp in filename to avoid overwrites
          // Ensure files exist under workspace or LOG_DIR
          if (isUnix()) {
            sh """
              ls -la ${env.LOG_DIR} || true
            """
          } else {
            bat "dir \"${env.LOG_DIR}\" || echo no-log-dir"
          }

          // Copy any workspace artifacts matching the timestamp into LOG_DIR (already copied test log)
          if (isUnix()) {
            sh "cp -f test-output-${env.BUILD_TS}.log ${env.LOG_DIR} || true"
          } else {
            bat "copy /Y test-output-${env.BUILD_TS}.log \"${env.LOG_DIR}\\\" || echo no-test-log"
          }

          // Use Jenkins archiveArtifacts step to keep them with the build record
          // (archiveArtifacts runs on the master controller, but path is workspace relative)
        }
        // Archive artifacts (patterns relative to workspace)
        archiveArtifacts artifacts: "**/test-output-${env.BUILD_TS}.log, **/*${env.BUILD_TS}*.log", fingerprint: true
      }
    }
  }

  post {
    always {
      script {
        echo "Build finished. Logs available in ${env.LOG_DIR} and in Jenkins archived artifacts."
      }
    }
    failure {
      echo "Build failed!"
    }
  }
}
