FROM python:3-alpine

# Update and install deps
RUN apk -U upgrade && apk add --update --no-cache tzdata bash && \
  apk --purge -v del py-pip && \
  rm /var/cache/apk/*

# Make workdir
ENV WORKDIR="/app"
ENV MAINSITE="https://www.state.nj.us/mvc/locations/agency.htm"
ENV TZ="America/New_York"

# run as app user
RUN adduser --disabled-password --no-create-home app app && mkdir -p ${WORKDIR} && chown -R app:app ${WORKDIR}
USER app
WORKDIR ${WORKDIR}

COPY --chown=app:app src/requirements.txt ${WORKDIR}/

RUN python -m venv venv && source ./venv/bin/activate && pip install -r requirements.txt

COPY --chown=app:app src/* ${WORKDIR}/
COPY --chown=app:app scripts/* /usr/local/bin/

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
CMD [ "start" ]