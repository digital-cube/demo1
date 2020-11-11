#!/bin/sh
cd users && ./test.sh && cd - && \
cd contacts && ./test.sh && cd -
