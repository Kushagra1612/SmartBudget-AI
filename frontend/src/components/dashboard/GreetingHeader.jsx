export default function GreetingHeader() {

    const hour = new Date().getHours();

    let greeting = "Good Evening";

    if (hour < 12)
        greeting = "Good Morning";

    else if (hour < 18)
        greeting = "Good Afternoon";

    return (

        <div className="mb-10">

            <p className="text-sm text-gray-500">

                {new Date().toLocaleDateString(
                    "en-IN",
                    {
                        weekday: "long",
                        day: "numeric",
                        month: "long",
                    }
                )}

            </p>

            <h1 className="mt-2 text-5xl font-bold">

                {greeting} 👋

            </h1>

            <p className="mt-3 text-lg text-gray-500">

                Welcome back to SmartBudget AI

            </p>

        </div>

    );

}