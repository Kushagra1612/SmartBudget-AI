import ChatMessage from "./ChatMessage";

export default function ChatWindow({ messages }) {

    return (

        <div
            className="
                bg-[var(--surface)]
                border
                border-[var(--border)]
                rounded-2xl
                shadow-[var(--shadow)]
                p-6
                h-[500px]
                overflow-y-auto
                mt-8
            "
        >

            {messages.length === 0 ? (

                <div className="h-full flex items-center justify-center">

                    <p className="text-[var(--text-light)]">
                        Start a conversation with SmartBudget AI.
                    </p>

                </div>

            ) : (

                messages.map((message, index) => (

                    <ChatMessage
                        key={index}
                        message={message}
                    />

                ))

            )}

        </div>

    );

}