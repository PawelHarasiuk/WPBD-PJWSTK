FROM alpine:latest

# Install curl, bash, and dos2unix
RUN apk add --no-cache curl bash dos2unix

# Copy your setup script into the container
COPY connector.json .
COPY setup.sh .

# Normalize line endings and make executable
RUN dos2unix /setup.sh && chmod +x /setup.sh

# Run the script
ENTRYPOINT ["/setup.sh"]
