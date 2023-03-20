@echo off
title "Don't Stop Me !"
java -jar agent.jar -jnlpUrl http://192.168.16.166:5016/computer/jenkins-win-191/jenkins-agent.jnlp -secret 45d6a4e45c86cc0060ffe7d5060e93d1e8638e0e38c6478882e8bbeb3fe5ae86 -workDir "D:\Jenkins"