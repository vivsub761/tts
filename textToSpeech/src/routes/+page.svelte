<script>
    let wordInterval = 3;
    import { onMount, onDestroy } from 'svelte';
    let text = ''
    let enableAutoCorrect = false;
    // @ts-ignore
    let IntervalID;
    async function sendText() {
        const response = await fetch('http://localhost:14366/text-to-speech',
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: text }),
                    }
                )

    }
    onMount(() => {
    IntervalID = setInterval(IntervalSender, 100);
    });

    onDestroy(() => {
    // @ts-ignore
    clearInterval(IntervalID);
  });

  async function autocorrectLastWord(erase) {
    let typedWords= text.trim().split(" ");
    let index = typedWords.length - 1;
    let prevWord = typedWords[index]
    if (prevWord !== '') {
        const response = await fetch('http://localhost:14366/autocorrect',
                    {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: prevWord }),
                    }
                )
        
        let autocorrectedWord = await response.json()
        typedWords[index] = autocorrectedWord["text"];
        if (!erase) {
            text = typedWords.join(" ") + ' ';
        }
    }
  }
    // @ts-ignore
    async function EventHandler(event) {
        if (event.key === 'Enter') {
            if (enableAutoCorrect) {
                autocorrectLastWord(true)
            }
            event.preventDefault()
            
            try {
                sendText()
                text = ''
            } catch (error) {
                console.log(error)
            }
        } else if (event.code === 'Space') {
            // event.preventDefault()
            console.log("SPACE KEY HIT")
            if (enableAutoCorrect) {
                autocorrectLastWord(false);
            }
        }
    }

    async function IntervalSender() {
        const lastChar = text.charAt(text.length - 1)
        if (text.trim() !== "" && lastChar === " " && text.trim().split(" ").length >= wordInterval) {
            sendText();
            text = '';
        }
    }
    function toggle() {
        enableAutoCorrect = !enableAutoCorrect;
    }

</script>


<main class = "centered">
    <div style = "display: flex; flex-direction: column;">
    <div style = "display: flex; flex-direction: row;">
    <input class = "numChooser" type = "number" bind:value={wordInterval}/>
    <input type = "checkbox" id = "toggleButton" on:click={toggle}/>
    </div>
    <textarea class = "input" bind:value={text} on:keydown= {EventHandler} placeholder="Enter text here" />
</div>
</main>



<style>
.input {
    width: 500px;
    height: 200px;
    margin-top: 150px;
    vertical-align: top;
    margin-top: 5px;
}

.centered {
    display: flex;
    justify-content: center;
    align-items: center;
}
.numChooser {
    width: 50px;
    margin-bottom: 0px;
}
</style>