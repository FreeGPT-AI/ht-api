# Set the base image
FROM python:3.11

# Set the working directory
WORKDIR /code

# Copy and install requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code

# Specify the entrypoint and command
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 80 & python3 -m bot"]