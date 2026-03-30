pipeline {
    agent any

    environment {
        IMAGE_NAME = "inventory-api"
        CONTAINER_NAME = "inventory-api-container"
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                checkout scm
            }
        }

        stage('Check Tools') {
        steps {
            bat 'echo %PATH%'
            bat 'python --version'
            bat 'docker --version'
            bat 'node --version'
            bat 'npm install newman'
            bat 'newman --version'
        }
    }

        stage('Generate README') {
            steps {
                bat 'python generate_readme.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker rm -f %CONTAINER_NAME% >nul 2>&1 || exit /b 0'
                bat 'docker run -d --name %CONTAINER_NAME% -p 8000:8000 %IMAGE_NAME%'
            }
        }

        stage('Wait for API Startup') {
            steps {
                bat '''
powershell -Command ^
"$maxAttempts=20; ^
for($i=1; $i -le $maxAttempts; $i++){ ^
  try { ^
    $response = Invoke-WebRequest -Uri 'http://localhost:8000/docs' -UseBasicParsing; ^
    if($response.StatusCode -eq 200){ exit 0 } ^
  } catch {} ^
  Start-Sleep -Seconds 3 ^
} ^
exit 1"
'''
            }
        }

        stage('Run Newman Tests') {
            steps {
                bat 'npx newman run .postman/InventoryAPI.postman_collection.json'
            }
        }

        stage('Create ZIP Artifact') {
            steps {
                bat '''
powershell -Command ^
"$timestamp = Get-Date -Format 'yyyy-MM-dd-HH-mm-ss'; ^
$zipName = 'complete-' + $timestamp + '.zip'; ^
Compress-Archive -Path app.py,database.py,models.py,load_csv.py,requirements.txt,Dockerfile,.dockerignore,generate_readme.py,README.txt,.postman -DestinationPath $zipName -Force"
'''
            }
        }
    }

    post {
        always {
            bat 'docker rm -f %CONTAINER_NAME% >nul 2>&1 || exit /b 0'
            archiveArtifacts artifacts: 'README.txt, complete-*.zip', fingerprint: true
        }
    }
}