# ec2-autoscaling
Autoscale ec2 instances based on computation load

# Autoscaling

## 1. Problem Statement
We have been given an AMI(Amazon Machine Image) that contains an image recognition model
which classifies the input image. If there are multiple images to be processed it would be done
serially, thus taking a lot of time. To solve this problem of high latency, we are using AWS
resources so that we can scale up and down depending on the number of images/requests.
Multiple images can then be processed parallely thus providing a better response time.

## 2. Requirements 
* [x] The app should take images received from users as input and perform image recognition on these images using the provided deep learning model. It should also return the recognition result (the top 1 result from the provided model) as output to the users. The input is a .png file, and the output is the prediction result. For example, the user uploads an image named “test_0.JPEG”. For the above request, the output should be “bathtub” in plain text.
* [x] Your app should be able to handle multiple requests concurrently. It should automatically scale out when the request demand increases, and automatically scale in when the demand drops. Because we have limited resources from the free tier, the app should use no more than 20 instances, and it should queue all the pending requests when it reaches this limit. When there is no request, the app should use the minimum number of instances. Give your instances meaningful names, for example, a web-tier instance should be named in the fashion of “web-instance1” and an app-tier instance should be named “app-instance1”.
* [x] All the inputs (images) and outputs (recognition results) should be stored in S3 for persistence. S3 stores all the objects in a form of key-value pair. The inputs should be stored in one bucket. The key of each object in this bucket is in the form of .JPEG files, e.g., test_0.JPEG. and the value in this bucket is the image file. The outputs should be stored in another bucket. The key is the image name (e.g., test_0), and the value is in the form of (image name, top-1 result) pairs, e.g., (test_0, bathtub). Specify your bucket names in your project README file.
* [x] The app should handle all the requests as fast as possible, and it should not miss any requests. The recognition requests should all be correct.

## 3. Architecture

<img src="Architecture.PNG" width=800><br>

## 4. Gif demonstrating our Autoscaling of instances based on the load
<img src="AutoScaling.gif" width=800><br>
