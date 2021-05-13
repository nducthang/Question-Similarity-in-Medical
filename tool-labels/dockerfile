FROM python:3.7
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
RUN mkdir -p .streamlit
RUN mv config.toml .streamlit
CMD ["streamlit", "run", "app.py"]