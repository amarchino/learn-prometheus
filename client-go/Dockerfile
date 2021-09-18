FROM golang:1-alpine

WORKDIR /app
RUN apk update \
    && apk add git
COPY ./go.mod /app/
RUN go get github.com/gorilla/mux \
        github.com/prometheus/client_golang/prometheus \
        github.com/prometheus/client_golang/prometheus/promauto \
        github.com/prometheus/client_golang/prometheus/promhttp
COPY *.go /app/
RUN go build -o /app/counter counter.go \
    && go build -o /app/gauge gauge.go \
    && go build -o /app/histogram histogram.go \
    && go build -o /app/summary summary.go
