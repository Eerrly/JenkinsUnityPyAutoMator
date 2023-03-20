#! /bin/sh

mytitle="(Don't Stop Me !)"
echo -e '\033k'$mytitle'\033\\'

echo ---------------------------------------------------------------------------
echo "                " start up jenkins salves
echo JENKINS_HOME=$JENKINS_HOME
echo ---------------------------------------------------------------------------

nohup java -jar -Xmx4096m -Xrs /Users/lmd/Desktop/JenkinsSoftWare/agent.jar -jnlpUrl http://192.168.16.166:5016/computer/jenkins-mac/jenkins-agent.jnlp -secret 017883dae0ee4063d222616944880af9bdbcc3484fead6871793492fc69e31a9 -workDir "/Volumes/sam_cha/Jenkins"
