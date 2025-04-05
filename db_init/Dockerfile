FROM postgres:14

# Copy the initialization scripts
COPY ./01-init.sql /docker-entrypoint-initdb.d/

# Make sure the script is executable
RUN chmod +x /docker-entrypoint-initdb.d/01-init.sql