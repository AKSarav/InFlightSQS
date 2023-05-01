# InFlightSQS

To Filter and delete specific messages from SQS which are in flight. or accidentally sent to SQS Queue

You can read more about this in my blog post [here]()


## Prerequisites

1. Python3
2. pip3
3. boto3

## Usage

```bash

usage: inFlightSQS.py [-h] [-t THREADS] [-s SEARCH] [-q QUEUE] [-d DELETE]

```

## Examples

```bash
# Search for string "stringTOsearch" in SQS Queue "mysqsqueue" and delete the messages
python InFlightSQS.py \
-t 10 \
-s stringTOsearch \
-q mysqsqueue \
-d True \

# Search for string "stringTOsearch" in SQS Queue "mysqsqueue" and do not delete the messages
python InFlightSQS.py \
-t 10 \
-s stringTOsearch \
-q mysqsqueue \
-d False
```


## Installation

Install the dependencies

```bash
pip3 install -r requirements.txt
```

Run the script

```bash
python InFlightSQS.py -t 10 -s stringTOsearch -q mysqsqueue -d False
```

## License
MIT License

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
