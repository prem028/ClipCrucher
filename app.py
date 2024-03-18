from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

# Explicitly specify the model name and revision
model_name = "sshleifer/distilbart-cnn-12-6"
revision = "a4f8f3e"
summarizer = pipeline('summarization', model=model_name, revision=revision)

@app.route('/')
def home():
    # Return the HTML form to the user
    return open('index.html').read()

@app.route('/summary', methods=['GET'])
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    transcript_or_error = get_transcript(video_id)
    if isinstance(transcript_or_error, str) and transcript_or_error.startswith('Error:'):
        return transcript_or_error
    summary = get_summary(transcript_or_error)
    return summary

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        return transcript
    except Exception as e:
        return f"Error: {str(e)}"

def get_summary(transcript):
    summary = ''
    for i in range(0, len(transcript)//1000 + 1):
        summary_text = summarizer(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary += summary_text + ' '
    return summary

if __name__ == '__main__':
    app.run(debug=True)
