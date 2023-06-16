FROM python:3.9-bullseye

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git unzip curl

# uncomment below line if this file exist in your machine
# COPY ./en2indic.zip .
# RUN test -f "en2indic.zip" \
#     && unzip "en2indic.zip" -d . \
#     || { echo "File not found locally, downloading from URL"; \
#          curl -o en2indic.zip "https://ai4b-public-nlu-nlg.objectstore.e2enetworks.net/en2indic.zip"; \
#          unzip en2indic.zip -d .; \
#          rm en2indic.zip; }

# RUN git clone https://github.com/AI4Bharat/indicTrans.git && \
#     cd indicTrans && \
#     git clone https://github.com/anoopkunchukuttan/indic_nlp_library.git && \
#     git clone https://github.com/anoopkunchukuttan/indic_nlp_resources.git && \
#     git clone https://github.com/rsennrich/subword-nmt.git && \
#     cd .. && \
#     git clone https://github.com/pytorch/fairseq.git

RUN pip install --upgrade pip
RUN pip install gunicorn flask 
# sacremoses pandas mock sacrebleu tensorboardX && \
#     pip install mosestokenizer subword-nmt pyarrow indic-nlp-library
# RUN cd /app/fairseq && pip install ./ && pip install xformers

# RUN rm -rf /app/en2indic.zip

# ENV model_path=/app/en-indic

WORKDIR /app/indicTrans
COPY app.py .
COPY config.py .

RUN mkdir /var/log/gunicorn
RUN touch /var/log/gunicorn/access.log
RUN touch /var/log/gunicorn/debug.log
RUN touch /var/log/gunicorn/error.log

EXPOSE 5000

ENTRYPOINT /bin/bash -c "gunicorn app:app --config config.py"
