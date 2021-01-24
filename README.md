# Setup Guide..


## Deploying Redis
# Start Redis Container
```sudo docker run --name some-redis -p 6379:6379 -d redis```
# Remove Redis Container
```sudo docker rm some-redis -f``` 

## Building and Deploying Resume Ranker
# Clone the Resume Ranker Repository
```git clone https://github.com/kamlesh1807/ResumeRanker.git```
# Build the Docker image
``` cd ResumeRanker ```<br>
```sudo docker build -t resumeranker:1.0 .```

# Start the Resume Ranker Container
```sudo docker run --name resume-ranker -p 8080:8080 -d resumeranker:1.0```

# Remove Redis Container
```sudo docker rm resume-ranker -f``` 
      
      THANK YOU FOR VISITING PROJECT !!!
