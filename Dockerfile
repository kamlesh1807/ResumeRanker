FROM python:3.7.9
ENV PORT 8080

COPY  website /opt/website/
WORKDIR /opt/website
RUN pip install -r /opt/website/requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python /opt/website/TrainingModel.py


COPY entrypoint.sh /opt/website
RUN chmod +x /opt/website/entrypoint.sh

ENTRYPOINT ["/opt/website/entrypoint.sh"]
