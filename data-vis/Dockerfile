FROM python:3.8

ADD ./requirements.txt ./
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY python ./
RUN jupyter trust ./faker_analysis.ipynb ./marsweather_analysis.ipynb ./neo_analysis.ipynb ./weather_analysis.ipynb
EXPOSE 8888
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''