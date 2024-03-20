# The configuration of the server within the container
ARG HOST=0.0.0.0
ARG PORT=3000

### STAGE 1: Build Frontend ###
FROM node:21 as frontend-builder

WORKDIR /app/frontend

# Install (and hopefully hit cached) node_modules
COPY frontend/package*.json ./
RUN npm ci

# Now copy over the source code and build it with Vite
# The static site files should be located at /app/frontend/dist in the container
COPY frontend .
RUN npm run build



### STAGE 2: Build Backend and Run ###
FROM python:3.12-slim
# Reexport args for this layer
ARG HOST 
ARG PORT

WORKDIR /app/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Install ffmpeg
RUN apt-get update
RUN apt-get install -y ffmpeg

# Install Python dependencies
COPY Pipfile Pipfile.lock .
RUN pip3 install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile

# Copy the source code
# TODO: will probably want this in a separate `src` directory, especially 
# if more modules are added
COPY main.py .

# Set up uvicorn environment defined by ARGS
ENV UVICORN_HOST=${HOST}
ENV UVICORN_PORT=${PORT}

ENV PYTHON_ENV=production

# create a non root user, give it access to the application files, and switch to it
RUN groupadd -r nonroot
RUN useradd -r -g nonroot nonroot
RUN chown -R nonroot:nonroot /app
USER nonroot

EXPOSE $PORT
CMD ["pipenv", "run", "uvicorn", "main:app"]
# CMD ["tail", "-f", "/dev/null"]