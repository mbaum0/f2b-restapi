
# Sets the base image for subsequent instructions
FROM python:3.11.1-bullseye

# Setup fail2ban
WORKDIR /tmp/f2b
RUN git clone https://github.com/fail2ban/fail2ban.git
RUN cd fail2ban \
    && ./fail2ban-2to3 \
    && python3 setup.py install \
    && rm -r /tmp/f2b

# Sets the working directory in the container  
WORKDIR /app

# Copies the dependency files to the working directory
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip3 install -r requirements.txt

# Copies everything to the working directory
COPY . /app

# Command to run on container start    
CMD [ "python3" , "./app.py" ]
