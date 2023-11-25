environment=dev
date=$(date '+%Y-%m-%d-%H-%M')

### Pull branch
echo "Please enter branch name to pull:"
read branch
echo you have entered branch : $branch
sleep 1
git stash; git branch -f origin/$branch; git checkout $branch; git pull;

echo "creating docker image"
docker build -t jmdev .

### Complete Deployment
echo "killing the running docker"
docker ps -a | egrep 'jmdev' | awk '{print $1}'| xargs docker kill
docker ps -a | egrep 'jmdev' | awk '{print $1}'| xargs docker rm

echo "running the using docker"
docker run -d --restart=unless-stopped --name jmdev -p 8000:8000 jmdev

## Write the deployment history in a file
#echo "$date --- $branch --- re-brnad-sts-$environment-$branch_name-$date">> deployment-version-$environment.txt

echo "We are done !"