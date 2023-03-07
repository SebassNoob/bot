echo -e "Annoybot 1.9.0 setup\n\n"


export TOKEN="my_token_from_discord_dev_portal"
export uid="695076103768768605"

while true; do
    read -p "check! have you installed the prerequisites and bash commands specified in README.md and setup.sh? have you set your TOKEN and uid in setup.sh? [Y/N] " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo -e "Please answer y or n.\n";;
    esac
done

poetry install #install python dependencies
javac SetupDb.java #compile java pgrm to create db
java -classpath sqlite-jdbc-3.41.0.0.jar:. SetupDb #run with jdbc

python3 main.py #run main


