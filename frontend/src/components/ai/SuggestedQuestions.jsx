const QUESTIONS = [
    "Give me a summary of my finances.",
    "Where did I spend the most this month?",
    "How much did I save this month?",
    "Which budget is closest to exceeding its limit?",
    "How can I reduce my expenses?",
    "What is my financial health score?",
];

export default function SuggestedQuestions({
    onSelect,
}) {

    return (

        <div className="mt-8 mb-6">

            <h3 className="text-lg font-semibold mb-3">
                Suggested Questions
            </h3>

            <div className="flex flex-wrap gap-3">

                {QUESTIONS.map((question) => (

                    <button
                        key={question}
                        onClick={() => onSelect(question)}
                        className="
                            px-4
                            py-2
                            rounded-full
                            border
                            bg-white
                            hover:bg-blue-600
                            hover:text-white
                            hover:border-blue-600
                            transition
                        "
                    >
                        {question}
                    </button>

                ))}

            </div>

        </div>

    );

}