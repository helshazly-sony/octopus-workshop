#!/bin/bash

function clone_repo() {
    # Clone the octupos repository
    git clone git@github.com:helshazly-sony/octupos.git

    # Check if cloning was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to clone the octupos repository."
        exit 1
    fi
}

function run_build() {
    # Change directory to the server directory
    cd octupos/server

    # Run the build script (assuming it's named 'build.sh')
    ./build.sh -s 
}

function run_serve() {
    # clean previous serve runs
    clean

    # Change directory to the data-transfer examples bin directory
    cd octupos/server/data-transfer/examples/bin || exit 1

    # Run the flight server script in the background, redirecting output to /tmp/flight_server.log
    ./run_flight_server.sh > /tmp/flight_server.log 2>&1 &

    # Change directory to the job-dispatcher directory
    cd ../../../job-dispatcher || exit 1

    # install dependencies
    poetry install

    # Start the server using poetry
    poetry run uvicorn src.main:app --reload
}

function clean() {
    # Kill the process listening on port 8888
    lsof -ti :8888 | xargs kill -9 2>/dev/null

    # Remove /tmp/flight_server.log if it exists
    rm -f /tmp/flight_server.log

    # Remove octupos-server.log if it exists
    rm -f /tmp/octupos-server.log
}

# Parse command line options
while [[ $# -gt 0 ]]; do
    case "$1" in
        --fish)
            clone_repo
            exit 0
            ;;
        --cook)
            run_build
            exit 0
            ;;
        --serve)
            run_serve
            exit 0
            ;;
        --clean)
            clean
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'"
            exit 1
            ;;
    esac
done

# If no options provided, clone and run build
#clone_repo
#run_build
#clean
#run_serve
