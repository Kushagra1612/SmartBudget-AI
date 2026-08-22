import ChatMessage from "./ChatMessage";

export default function ChatWindow({ messages }) {

    return (

        <div
            className="
                bg-white
                rounded-2xl
                shadow
                p-6
                h-[500px]
                overflow-y-auto
                mt-8
            "
        >

            {messages.length === 0 ? (

                <div className="h-full flex items-center justify-center">

                    <p className="text-gray-400">
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