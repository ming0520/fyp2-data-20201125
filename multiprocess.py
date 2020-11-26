from pydub import AudioSegment
import json
import subprocess
import os
import shutil
import simplejson as json
import speech_recognition as sr
import glob
import multiprocessing

def process_gentle(file_name):
    audio_path = 'UclassAudioV1'
    script_path = 'TranscriptTxt'
    output_path = 'GentleAligned'
    input_audio = f'./{audio_path}/{file_name}.wav'
    input_script = f'./{script_path}/{file_name}.txt'
    output_json = f'./{output_path}/{file_name}.json'
    
    try:
        result = subprocess.check_output(f'curl -F "audio=@{input_audio}" -F "transcript=@{input_script}" "http://localhost:8765/transcriptions?async=false"')
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    outjson = json.loads(result)
    with open(f'{output_json}', 'w') as f:
        json.dump(outjson, f)
    return

files = glob.glob(f'{script_path}/*.txt')
files_name = []
for file in files:
    print(file.split('\\')[1].split('.')[0])
    files_name.append(file.split('\\')[1].split('.')[0])

if __name__ == '__main__':
    jobs = []
    for file_name in files_name:
        p = multiprocessing.Process(target=process_gentle, args=(file_name,))
        jobs.append(p)
        p.start()
        print(p)