## Objectives:

1. Writing a python web service that accepts images in JSON object format, uses YOLO and OpenCV to process images, and returns a JSON object with a list of detected objects.

2. Building a Docker Image for the object detection web service.

3. Creating a Kubernetes cluster on virtual machines (instances) in the Oracle Cloud Infrastructure (OCI).

4. Deploying a Kubernetes service to distribute inbound requests among pods that are running the object detection service.

5. Testing the system under varying load and number of pods conditions

## Instruction:

You can run this to use Cloudiod_client.py that sends image data from inputfolder to an endpoint
python Cloudiod_client.py <inputfolder> <endpoint> <num_threads>
python Cloudiod_client.py inputfolder/ http://118.138.43.2:5000/api/object_detection 16

You can pull my image using this code
docker pull jwrm/code

run the image, it will create a python flask web service, use Cloudiod_client.py to send data to that web service

it will output data like this
![image](https://user-images.githubusercontent.com/93886913/236833510-7ea91042-2953-4675-ae1a-7260360c83e3.png)
