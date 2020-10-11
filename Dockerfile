FROM ubuntu:bionic
LABEL manteiner="francis mujani <fmujani08@gmail.com>"


WORKDIR /audio

# ENV TZ = Europe/france
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN export DEBIAN_FRONTEND=noninteractive; \
    export DEBCONF_NONINTERACTIVE_SEEN=true; \
    echo 'tzdata tzdata/Areas select Etc' | debconf-set-selections; \
    echo 'tzdata tzdata/Zones/Etc select UTC' | debconf-set-selections; \
    apt-get update -y \
    && apt-get install -y --no-install-recommends \
            tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


    
RUN apt-get update -y && \
    apt-get install -y python3 && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get install -y python3-pip python3-dev -y && \
    apt-get install -y python3-tk ffmpeg portaudio19-dev python3-pyaudio build-essential -y --no-install-recommends libx11-dev -y && \
    pip3 install --upgrade pip && \
    pip3 install matplotlib termcolor scipy pydub PyAudio
    # apt-get -y install software-properties-common && \
    #add-apt-repository ppa: jonathonf / ffmpeg-4 && \
    #apt-get install -y python3-tk ffmpeg portaudio19-dev python3-pyaudio && \
    #apt-get install -y python3-pip python3-dev && \
    # pip3 install --upgrade pip && \
    # pip3 install matplotlib termcolor scipy pydub PyAudio

# RUN apt-get -y install software-properties-common && \
#     add-apt-repository ppa: jonathonf / ffmpeg-4 && \
#     apt-get install -y python3-tk_3.6.9-1 ffmpeg portaudio19-dev python3-pyaudio && \
#     pip3 install matplotlib termcolor scipy pydub PyAudio

COPY . /audio
RUN pip3 install -r requirements.txt

# make clear reset && \
# make tests && \
#RUN collect-fingerprints-of-songs.py && \
#    get-database-stat.py

RUN chmod +x script.sh
RUN bash script.sh

EXPOSE 5000

CMD ["python", "app/app.py"]
