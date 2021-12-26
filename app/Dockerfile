###########
# BUILDER #
###########

# Pull official base image
FROM python:3.10-alpine as builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 dependencies
RUN apk update && apk add postgresql-dev libffi-dev gcc python3-dev musl-dev

# Update pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

##########
# DEPLOY #
##########

# Pull official base image
FROM python:3.10-alpine

# Create directory for the app user
RUN mkdir -p /home/app

# Create app user
RUN addgroup -S app && adduser -S app -G app

# Create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN chown -R app:app $APP_HOME/staticfiles
WORKDIR $APP_HOME

# Install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# Copy project with direct ownership to appropriate user
COPY --chown=app:app . $APP_HOME

# Change to the app user
USER app

# Run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]