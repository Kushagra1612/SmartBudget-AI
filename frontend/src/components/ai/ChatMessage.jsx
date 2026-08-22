import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function AgentsUsedBadge({ agents }) {

    if (!agents || agents.length === 0) {
        return null;
    }

    const labels = agents.map(
        (agent) => agent.charAt(0).toUpperCase() + agent.slice(1)
    );

    return (
        <p className="mt-3 text-xs text-gray-400">
            Consulted: {labels.join(", ")}
        </p>
    );

}

export default function ChatMessage({ message }) {

    const isUser = message.role === "user";

    return (

        <div
            className={`flex mb-4 ${
                isUser
                    ? "justify-end"
                    : "justify-start"
            }`}
        >

            <div
                className={`max-w-[75%] rounded-2xl px-5 py-4 shadow ${
                    isUser
                        ? "bg-blue-600 text-white"
                        : "bg-white text-gray-900 border"
                }`}
            >

                {isUser ? (

                    message.text

                ) : (

                    <>

                        <article className="prose prose-sm max-w-none">

                            <ReactMarkdown
                                remarkPlugins={[remarkGfm]}
                            >
                                {message.text}
                            </ReactMarkdown>

                        </article>

                        <AgentsUsedBadge agents={message.agentsUsed} />

                    </>

                )}

            </div>

        </div>

    );

}