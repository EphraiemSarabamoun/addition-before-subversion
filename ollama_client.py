import ollama, logging, json

logging.basicConfig(level=logging.INFO)

def chat_with_memory(model: str, priming_prompts: list[str], sensitive_prompt: str):
    history = []
    for priming_prompt in priming_prompts:
        escaped_priming_prompt = json.dumps(priming_prompt)
        history.append({'role': 'user', 'content': escaped_priming_prompt})
        logging.info(f"Priming prompt: {escaped_priming_prompt}")
        logging.info(f"History: {history}")
        response = ollama.chat(model=model, messages=history, options={'temperature': 0})
        model_answer = response['message']['content']
        model_thinking = response['message']['thinking'] 
        logging.info(f"Model answer: {model_answer}")
        logging.info(f"Model thinking: {model_thinking}")
        history.append({'role': 'assistant', 'content': model_answer})

    
    history.append({'role': 'user', 'content': sensitive_prompt})
    logging.debug(f"History: {history}")
    response = ollama.chat(model='gpt-oss:20b', messages=history, options={'temperature': 0})
    logging.debug(f"Response: {response}")
    model_answer = response['message']['content']
    model_thinking = response['message']['thinking'] 
    logging.info(f"Model answer: {model_answer}")
    logging.info(f"Model thinking: {model_thinking}")
    return model_answer, model_thinking
