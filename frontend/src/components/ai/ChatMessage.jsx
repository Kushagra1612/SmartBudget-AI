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
        <p className="mt-3 text-xs text-[var(--text-light)]">
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
                className={`max-w-[75%] rounded-2xl px-5 py-4 shadow-[var(--shadow)] ${
                    isUser
                        ? "bg-blue-600 text-white"
                        : "bg-[var(--surface)] text-[var(--text)] border border-[var(--border)]"
                }`}
            >

                {isUser ? (

                    message.text

                ) : (

                    <>

                        {/* dark:prose-invert flips the Tailwind
                            Typography plugin's default light-mode text
                            colors (headings, paragraphs, links, code
                            blocks) for markdown-rendered assistant
                            replies -- without it, prose content stays
                            dark-on-dark same as everything else here
                            did before the CSS-variable fixes. */}
                        <article className="prose prose-sm dark:prose-invert max-w-none">

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