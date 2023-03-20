#! /bin/sh

mytitle="(Don't Stop Me !)"
echo -e '\033k'$mytitle'\033\\'

export JENKINS_HOME=/Users/lmd/Desktop/JenkinsSoftWare/Jenkins_Home

echo ---------------------------------------------------------------------------
echo "                " start up jenkins
echo JENKINS_HOME=$JENKINS_HOME
echo ---------------------------------------------------------------------------

java -jar /Users/lmd/Desktop/JenkinsSoftWare/jenkins.war --httpPort=5016
