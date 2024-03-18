# Use a base image with Python 3.12
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the Python code, templates, &, session file into the container
COPY main.py /app/
COPY engine.py /app/
COPY data_layer.py /app/
COPY templates /app/templates
COPY WhatsappAutomation/Default_WA_personal_whatsapp /app/WhatsappAutomation/Default_WA_personal_whatsapp
COPY requirements.txt /app/requirements.txt

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies within the virtual environment
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install playwright && \
    pip install psutil && \
    playwright install && \
    playwright install-deps

EXPOSE 80

# Set the entry point for the container
CMD ["python3", "main.py"]
