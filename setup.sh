echo "Annoybot 1.9.0 setup"

poetry install #install python dependencies
javac SetupDb.java #compile java pgrm to create db
java -classpath sqlite-jdbc-3.41.0.0.jar:. SetupDb #run with jdbc
python3 main.py #run main


