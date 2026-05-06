# See ../triqs/packaging for other options
FROM flatironinstitute/triqs:unstable-ubuntu-clang
ARG APPNAME=minipole_interface

COPY --chown=build . $SRC/$APPNAME
WORKDIR $SRC/$APPNAME
USER build
ARG BUILD_ID
RUN pip install --no-cache-dir -e ".[test]"
