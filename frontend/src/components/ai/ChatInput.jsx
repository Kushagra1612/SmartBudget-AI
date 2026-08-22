export default function ChatInput({

    message,

    setMessage,

    loading,

    onSend,

}) {

    function handleKeyDown(e) {

        if (e.key === "Enter" && !loading) {

            onSend();

        }

    }

    return (

        <div className="flex gap-4 mt-6">

            <input
                type="text"
                value={message}
                onChange={(e) =>
                    setMessage(e.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder="Ask SmartBudget AI anything..."
                className="
                    flex-1
                    border
                    rounded-xl
                    px-5
                    py-4
                    outline-none
                    focus:ring-2
                    focus:ring-blue-500
                "
            />

            <button
                onClick={() => onSend()}
                disabled={loading}
                className="
                    bg-blue-600
                    hover:bg-blue-700
                    disabled:bg-gray-400
                    text-white
                    px-8
                    rounded-xl
                    font-semibold
                    transition
                "
            >

                {loading
                    ? "Thinking..."
                    : "Send"}

            </button>

        </div>

    );

}