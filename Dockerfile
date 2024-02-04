# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV OPENAI_API_KEY="YOUR_API_KEY"
ENV TAVILY_API_KEY="YOUR_API_KEY"
ENV ELEVEN_API_KEY="YOUR_API_KEY"

# Run server when the container launches
CMD ["python3", "langserve/serve.py", "--source", "PDF"]
