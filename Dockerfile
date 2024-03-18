# Use a base image with Python
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the Python code, templates, &, session file into the container
COPY main.py /app/
COPY engine.py /app/
COPY data_layer.py /app/
COPY templates /app/templates
COPY Default_WA_personal_whatsapp /app/Default_WA_personal_whatsapp
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install playwright && \
    playwright install && \
    playwright install-deps

EXPOSE 5000

# Set the entry point for the container
CMD ["python3", "main.py"]
