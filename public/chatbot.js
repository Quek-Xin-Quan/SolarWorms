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
            let generatedText = response[0].generated_text;
            let cleanedText = generatedText.replace(text1, ''); // This will remove the user's input from the generated text
            console.log(cleanedText);
            let msg2 =  {name: "Bot", message: cleanedText};
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
    const response = await fetch(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
        {
            headers: { 
                Authorization: "Bearer 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",
                'Content-Type': 'application/json' // Add this line
            },
            method: "POST",
            body: JSON.stringify(data),
        }
    );
    const result = await response.json();
    return result;
}
// query({"inputs": "Can you please let us know more details about your "}).then((response) => {
//     console.log(JSON.stringify(response));
// });
const chatbox = new Chatbox();
chatbox.display();