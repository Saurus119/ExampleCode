FROM python:3.8

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg lsb-release && \
    rm -rf /var/lib/apt/lists/*

# Check Ubuntu version
RUN VERSION=$(lsb_release -rs) && \
    if [ ! "18.04 20.04 22.04 23.04" == *"$VERSION"* ]; then \
        echo "Ubuntu $VERSION is not currently supported."; \
        exit 1; \
    fi

# Install ODBC driver dependencies
RUN apt-get update && \
    apt-get install -y gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev

# Set environment variables
ENV PATH="/opt/mssql-tools/bin:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Copy the SQL script into the container
COPY migration1.sql /migration1.sql

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["/bin/bash", "-c", "/opt/mssql-tools/bin/sqlcmd -S db -U sa -P StrongPassword!123 -d master -i /migration1.sql & python app.py"]
