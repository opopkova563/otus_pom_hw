pipeline {
    agent any

    parameters {
        string(
            name: 'SELENOID_URL',
            defaultValue: 'http://host.docker.internal/wd/hub',
            description: 'Адрес Selenoid executor'
        )

        string(
            name: 'base_url',
            defaultValue: 'http://host.docker.internal:8081',
            description: 'Адрес приложения PrestaShop'
        )

        choice(
            name: 'browser',
            choices: ['chrome', 'firefox'],
            description: 'Браузер'
        )
        string(
            name: 'browser_version',
            defaultValue: '',
            description: 'Версия браузера Selenoid. Chrome: 127.0 или 128.0; Firefox: 124.0 или 125.0'
        )

        choice(
            name: 'threads',
            choices: ['1', '2', '3', '4'],
            description: 'Количество потоков pytest-xdist'
        )
    }

    environment {
        VENV = "${WORKSPACE}/venv"
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/opopkova563/otus_pom_hw.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    set -e

                    python3 -m venv "$VENV"
                    "$VENV/bin/python" -m pip install --upgrade pip
                    "$VENV/bin/python" -m pip install -r requirements.txt
                '''
            }
        }

        stage('Check Selenoid') {
            steps {
                sh '''
                    set -e

                    echo "Checking Selenoid: ${SELENOID_URL}"

                    curl --fail --max-time 10 \
                      "${SELENOID_URL%/wd/hub}/status"
                '''
            }
        }

        stage('Run tests') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'prestashop-admin',
                        usernameVariable: 'ADMIN_EMAIL',
                        passwordVariable: 'ADMIN_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        rm -rf "$ALLURE_RESULTS"

                        export BASE_URL="${base_url}"

                        PYTEST_ARGS="
                            -v src/tests
                            --browser=${browser}
                            --selenoid-url=${SELENOID_URL}
                            --alluredir=${ALLURE_RESULTS}
                        "


                        echo "BASE_URL=${BASE_URL}"
                        echo "SELENOID_URL=${SELENOID_URL}"
                        echo "browser=${browser}"

                        "$VENV/bin/python" -m pytest $PYTEST_ARGS
                    '''
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                jdk: '',
                commandline: 'allure',
                results: [[path: "${ALLURE_RESULTS}"]]

            archiveArtifacts artifacts: "${ALLURE_RESULTS}/**", allowEmptyArchive: true

            cleanWs(
                deleteDirs: true,
                disableDeferredWipeout: true,
                notFailBuild: true
            )
        }
    }
}