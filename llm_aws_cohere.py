# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use the  Cohere Command R model.
"""
import json
import logging
import boto3


from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using a Cohere Command R model.
    Args:
        model_id (str): The model ID to use.
        body (str) : The reqest body to use.
    Returns:
        dict: The response from the model.
    """

    logger.info("Generating text with Cohere model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id
    )

    logger.info(
        "Successfully generated text with Cohere Command R model %s", model_id)

    return response


def main():
    """
    Entrypoint for Cohere example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    # model_id = 'cohere.command-r-v1:0'
    model_id = 'cohere.command-r-plus-v1:0'
    chat_history = [
        {"role": "USER", "message": "What is an interesting new role in AI if I don't have an ML background?"},
        {"role": "CHATBOT", "message": "You could explore being a prompt engineer!"}
    ]
    message = "What are some skills I should have?"

    try:
        body = json.dumps({
            "message": message,
            "chat_history": chat_history,
            "max_tokens": 2000,
            "temperature": 0.6,
            "p": 0.5,
            "k": 250
        })
        response = generate_text(model_id=model_id,
                                 body=body)

        response_body = json.loads(response.get('body').read())
        response_chat_history = response_body.get('chat_history')
        print('Chat history\n------------')
        for response_message in response_chat_history:
            if 'message' in response_message:
                print(f"Role: {response_message['role']}")
                print(f"Message: {response_message['message']}\n")
        print("Generated text\n--------------")
        print(f"Stop reason: {response_body['finish_reason']}")
        print(f"Response text: \n{response_body['text']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    else:
        print(f"Finished generating text with Cohere model {model_id}.")


if __name__ == "__main__":
    main()
