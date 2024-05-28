class Chatbox {
    constructor() {
            this.args = {
                openButton: document.querySelector('.chatbox__button'),
                chatBox: document.querySelector('.chatbox__support'),
                sendButton: document.querySelector('.send__button')
            }
            this.state = false;
            this.messages = [];
    }

    display() {
    const { openButton, chatBox, sendButton } = this.args;
    openButton.addEventListener('click', () => this.toggleState(chatBox));

    sendButton.addEventListener('click', () => this.onSendButton(chatBox));

    const node = chatBox.querySelector('input');
    node.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
        this.onSendButton(chatBox);
        }
    });
    
    }

    toggleState(chatBox) {
        this.state = !this.state;

        if(this.state) {
            chatBox.classList.add('chatbox--active');
        }
        else { 
            chatBox.classList.remove('chatbox--active');
        }
    }
    onSendButton(chatBox) {
        var textfield = chatBox.querySelector('input');
        let text1 = textfield.value;
        if (text1 === '') {
            return;
        }
        let msg1 =  {name: "User", message: text1};
        this.messages.push(msg1);
        
        query({"inputs": text1}).then((response) => {
            console.log(response);
            let generatedText = response.choices[0].text;
            // let cleanedText = generatedText.replace(text1, ''); // This will remove the user's input from the generated text
            console.log(generatedText);
            let msg2 =  {name: "Bot", message: generatedText};
            this.messages.push(msg2);
            textfield.value = '';
            this.updateChatText(chatBox);

        }),
        (error) => {
            console.error('Error:', error);
        };
    
    }
    
    updateChatText(chatBox)
    {
        var html = '';
        this.messages.slice().reverse().forEach((msg) => {
            if (msg.name === "User") {
                html += '<div class="messages__item messages__item--operator">' + msg.message + '</div>';
            }
            else {
                html += '<div class="messages__item messages__item--visitor">' + msg.message + '</div>';
            }
            
        });
        const chatmessages = chatBox.querySelector('.chatbox__messages');
        chatmessages.innerHTML = html;
    }
    
    


}
async function query(data) {
    const endpoint = 'https://ai-s10242300ai943195149526.openai.azure.com';
    const apiKey = '340562357d824bc2a47c3ab18a1ec4e4'; // Replace with your actual API key
    const model = 'gpt-35-turbo';   

    const response = await fetch(`${endpoint}/openai/deployments/${model}/completions?api-version=2022-12-01`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api-key': apiKey
        },
        body: JSON.stringify({
            prompt: [data.inputs],
            max_tokens: 1000
        })
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    console.log(result);
    return result;
}

const chatbox = new Chatbox();
chatbox.display();