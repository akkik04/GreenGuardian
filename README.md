# GreenGuardian 🌎🛡️

Green Guardian is an advanced deep learning object detection model designed to contribute to a greener environment by accurately detecting and highlighting plastic objects within images. By leveraging cutting-edge machine learning techniques and cloud-based infrastructure, this project aims to enable effective identification and monitoring of plastic presence, promoting environmental sustainability and conservation efforts.

## Overview 👀

Green Guardian is an advanced deep learning model that accurately detects and highlights plastic objects within images, contributing to a greener environment. Leveraging AWS SageMaker and associated cloud technologies, Green Guardian achieves scalable and efficient plastic detection while promoting environmental sustainability. SageMaker enables optimal model training and hyperparameter tuning, Step Functions orchestrates the detection pipeline, and Lambda functions provide serverless compute capabilities. This technical infrastructure ensures accurate results, cost-effectiveness, and scalability, making Green Guardian an impactful solution for a greener and more sustainable planet. 🌿🛡️

## Key Features 📝

- **Deep Learning Object Detection**: Green Guardian employs advanced deep learning techniques to accurately detect and locate plastic objects within images, providing valuable insights for environmental analysis.

- **Cloud Infrastructure**: Leveraging AWS cloud-based tools, Green Guardian ensures efficient processing, accessibility, and availability for users across different platforms.

- **Environmental Impact**: By highlighting and raising awareness about plastic presence, Green Guardian promotes conscious decision-making, waste reduction, recycling initiatives, and the preservation of ecosystems.

- **Intuitive User Experience**: Green Guardian offers a user-friendly interface, allowing users to conveniently submit images, visualize detection results, and take necessary actions for a greener environment.


## Architecture 🏗️

The architecture of Green Guardian incorporates various AWS services to achieve efficiency and scalablity.

- **AWS SageMaker**: Green Guardian utilizes SageMaker for model training, hyperparameter tuning, and inference. SageMaker provides a managed environment for developing and deploying machine learning models at scale, giving rise to efficient training and inference processes.

- **AWS Step Functions**: Step Functions is used to orchestrate the plastic detection pipeline. Gave me the opportunity to define a state machine that coordinates the execution of Lambda functions, ensuring that the pipeline runs smoothly and efficiently.

- **AWS EventBridge**: AWS EventBridge is utilized here to schedule and trigger the plastic detection pipeline at specific intervals using cron jobs. It allows you to define rules based on time schedules and events, ensuring that the detection pipeline runs at regular intervals to process newly submitted images.

- **AWS Lambda**:  Lambda functions provide serverless compute capabilities in response to events triggered by AWS EventBridge for this project. When EventBridge schedules the plastic detection pipeline, it invokes the Lambda function responsible for processing the images.

- **AWS S3 (Simple Storage Service)**: When users submit images, they are stored in an S3 bucket. S3 provides scalable and durable object storage, ensuring the availability and accessibility of the images for further processing.

## Ultimate Goal 🎯

- Turn GreenGuardian into a production-ready ML-pipeline that can accept inference requests from a web app (via REST-APIs, MERN, all that good web dev stuff) and return the inference results to the user.

