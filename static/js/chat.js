let currentUser = "";

function openConversation(name) {
    currentUser = name;
    document.getElementById("chatUser").innerText = name;
    document.getElementById("messages").innerHTML = "";
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    if (!input.value) return;

    const msg = document.createElement("div");
    msg.classList.add("message", "sent");
    msg.innerText = input.value;

    document.getElementById("messages").appendChild(msg);
    input.value = "";

    // Auto scroll
    document.getElementById("messages").scrollTop =
        document.getElementById("messages").scrollHeight;
}