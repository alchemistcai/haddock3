pipeline {
  agent {
    docker {
      image 'python:3'
    }

  }
  stages {
    stage('Install') {
      steps {
        sh 'pip install codecov'
      }
    }
    stage('Test') {
      steps {
        sh '''export HADDOCK3=`pwd`
chmod +x `pwd`/haddock/src/*
python -m coverage run -m unittest discover'''
      }
    }
  }
}