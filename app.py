from flask import Flask, request, jsonify, render_template
import azure.cognitiveservices.speech as speechsdk
import logging
import wave
import io
import os
from pydub import AudioSegment

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

logging.getLogger('flask').disabled = True
logging.basicConfig(filename='voice_assistant_log.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_key = '179e7e84d92d4c508a533f8e99e009f7'
service_region = "eastus"

def save_audio_stream(audio_stream, file_path):
    with wave.open(file_path, 'wb') as wave_file:
        wave_file.setnchannels(1)  
        wave_file.setsampwidth(2)  
        wave_file.setframerate(16000)  
        wave_file.writeframes(audio_stream.getbuffer())

def recognize_speech_from_mic(audio):

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename='processed_file.wav')
   
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_interaction_end', methods=['POST'])
def log_interaction_end():
    data = request.get_json()
    logging.info(data.get('message', 'Interaction ended without a message.'))
    return jsonify({'status': 'success'}), 200

@app.route('/log_question', methods=['POST'])
def log_question():
    data = request.get_json()
    logging.info(data.get('message', 'Fetching question...'))
    return jsonify({'status': 'success'}), 200

@app.route('/process_voice', methods=['POST'])
def process_voice():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']

    try:
        audio = AudioSegment.from_file(file)
        
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export('processed_file.wav', format='wav', parameters=["-acodec", "pcm_s16le"])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    audio_stream = io.BytesIO(file.read())
    file.save(audio_stream)
    audio_stream.seek(0) 
    
    try:
        text = recognize_speech_from_mic(audio_stream)
        if text:
            response_text = text.lower().replace(".", "").replace("?", "").replace("!", "")
            if "yes" == response_text or "no" == response_text:
                answer = "yes" if "yes" == response_text else "no"
                logging.info(f"Answer: {answer}")
                return jsonify({'message': f"You answered {answer}!"})
            else:
                print('response_text is: ',response_text)
                logging.info(f"Answer: {response_text}.. Taking response for the same question again")
                return jsonify({'message': f"Please say 'Yes' or 'No'. But you said {response_text}"}), 200
        else:
            logging.info("Speech not recognized. Asking to try again")
            return jsonify({'message': "Speech not recognized. Please say 'Yes' or 'No'."}), 200
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        return jsonify({'error': 'Error processing the voice input', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
