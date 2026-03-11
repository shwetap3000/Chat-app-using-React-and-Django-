import React, { useState, useEffect } from "react";

function Chat() {

  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {

    const ws = new WebSocket("ws://localhost:8000/ws/chat/1/");

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      setMessages((prev) => [
        ...prev,
        data
      ]);
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };

  }, []);


  const sendMessage = () => {

    socket.send(
      JSON.stringify({
        message: message,
        sender: 1
      })
    );

    setMessage("");
  };


  return (

    <div>

      <h2>Chat</h2>

      <div>
        {messages.map((msg, index) => (
          <p key={index}>
            <b>{msg.sender}:</b> {msg.message}
          </p>
        ))}
      </div>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <button onClick={sendMessage}>
        Send
      </button>

    </div>

  );
}

export default Chat;