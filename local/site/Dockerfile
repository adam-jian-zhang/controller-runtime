FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the public folder
COPY public /app/public

# Expose port
EXPOSE 9005

# Change to public directory and serve
WORKDIR /app/public

# Run simple HTTP server
CMD ["python3", "-m", "http.server", "9005"]
