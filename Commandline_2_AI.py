import subprocess
import openai
import time

with open('file.txt', 'r') as f:
    open_ai_api_key = f.read()
openai.api_key = open_ai_api_key.strip()

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
    #print(message_stack)
    with open('logs.txt','a') as g:
        g.write(prompt+'\n')
        g.write('\n'+openai_response+'\n')
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



if __name__ == "__main__":
    
    
    command = "nc -nvlp 4444"
    while True:
        print("Command:\n"+command)    
        result =  subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        query = result.stdout.decode('utf-8')
        print("Stdout:\n"+query)
        query2= str(command)+'\n'+str(result)
        explaination = explainer(query2,message_stack2)
        with open('enum_logs.txt','a') as h:
            h.write(explaination)
        command = enumerator(query,message_stack)
        
        #time.sleep(1)
        input()
        



