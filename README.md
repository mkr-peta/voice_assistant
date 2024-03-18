Voice Assistant Application

1. Language Flexibility -- Python is chosen due to its extensive support for natural language processing and its powerful libraries, such as Flask for web applications and azure-cognitiveservices-speech for voice recognition.

2. Voice Recognition -- Utilized Azure Cognitive Services' Speech-to-Text API for accurate voice recognition, focusing on capturing "Yes" or "No" responses.

3. Question Design -- The voice assistant asks a single, thought-provoking question designed to elicit a "Yes" or "No" response. This question is choosen at random from a set of pre defined questions given to it.

4. Response Handling 
First, the user must click the microphone button to start the conversation (for each time he needs to start the conversation, he needs to do this). Then the voice assistant asks the user a yes-or-no question, and he will have 4 seconds to answer it. After 2.5 seconds, the recording will be sent to the backend, where it will be processed using Azure Cognitive Services, and it will respond back to the frontend with a response.
-- If the response is yes or no, then the user will see "You answered {answer}".
-- If there is no response even after 2.5 seconds, the user will be displayed with "Speech not recognized. Please say 'Yes' or 'No'." and the process continues. The voice assistant records for another 2.5 seconds, and if the same happens again, it will show the same message again until it receives a response from the user.
-- If it receives any response other than yes or no, it displays "Please say 'Yes' or 'No'. But you said {response_text}" and it takes the response again for the next 2.5 seconds, and the process continues. If the voice assistant receives three wrong answers continuously, it terminates the interaction and displays "Interaction ended!!!".

5. Logging
Interaction logs are outputted to voice_assistant_log.txt, including the question asked and the user's response and termination of the interaction.


6. Docker Deployment
The application is packaged in a Docker container with a Dockerfile outlining the environment setup and application build process.

To build the Docker image, navigate to the directory containing the Dockerfile and run: 'docker build -t vs_voice_assistant .'

To run the container on your local machine: 'docker run -p 5002:5002 -e AZURE_SPEECH_KEY=<Your-Azure-Speech-Key> vs_voice_assistant'

Once the container is running, open a web browser and go to http://localhost:5002 to interact with the voice assistant.



1. Advanced handling of edge cases in speech recognition (e.g., background noise, different accents).
Azure Cognitive Services' Speech-to-Text has been utilized for its state-of-the-art noise reduction and accent recognition capabilities, which are crucial for handling various speech edge cases. The service provides Noise Reduction, Accent Recognition, Configurability. These features ensure that the voice assistant can understand and process "Yes" or "No" answers accurately, even in less-than-ideal audio conditions.

2. UI/Web Interface
A minimalistic and responsive web interface has been developed to interact with the voice assistant. The UI is built with HTML and styled with CSS to ensure a user-friendly experience. The functionality is achieved using Javascript and the server side is handled with flask.

3. Best Practices in Docker Usage
To adhere to Docker best practices and optimize the deployment process, the following strategies were implemented:
-- Efficient Layering: The Dockerfile was crafted to minimize the number of layers and combine commands where possible, reducing the overall image size.
-- .dockerignore File: A .dockerignore file was created to exclude unnecessary files from being copied into the Docker image, such as local development configurations and version control directories.
-- Environment Variables: Sensitive information, like the Azure Speech Service key, is passed to the container at runtime via environment variables rather than being included in the image, enhancing security.
-- Slim Base Image: The application uses a slim version of the official Python Docker image to reduce the footprint of the final Docker image.
