### Build the image
docker build -t github-comment-counter .

### Prepare config file
Set Github username, Github password, Organization to analyze in config/leaderboard-server.yml

### Start the docker container manually (the terminal will print the logs)
docker run -p 8080:8080 -p 8081:8081 -v //Users/eusebiu.rizescu/Data/Git/randomScriptsAndProjects/dockerfileGithubCommentCounter/config/:/application/config/ github-comment-counter

### Run the docker container from docker-compose
docker-compose -up -d github-comment-counter

### Stop the docker container from docker-compose
docker-compose stop github-comment-counter

### Use the application
Application:

http://localhost:8080

Maintenance/Metrics:

http://localhost:8081