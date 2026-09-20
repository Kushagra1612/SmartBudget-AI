import Card from "../common/Card";

export default function FinancialHealthCard({
    score,
    grade,
    status,
}) {

    const radius = 70;
    const stroke = 12;
    const normalizedRadius = radius - stroke / 2;
    const circumference = normalizedRadius * 2 * Math.PI;

    const clampedScore = Math.min(Math.max(score, 0), 100);
    const strokeDashoffset =
        circumference - (clampedScore / 100) * circumference;

    const tintVar =
        score >= 80
            ? "--success"
            : score >= 60
            ? "--warning"
            : "--danger";

    const ringColor = `var(${tintVar})`;

    // A soft wash of the score's color blended into whatever the
    // current surface color is -- color-mix() means this adapts
    // automatically to light/dark mode instead of needing a
    // hardcoded tint per theme. This gives the most important number
    // on the dashboard a visual "moment" instead of looking
    // identical to every other card.
    const tintBackground = `color-mix(in srgb, var(${tintVar}) 12%, var(--surface))`;

    return (
        <Card
            className="flex flex-col items-center text-center"
            style={{ background: tintBackground }}
        >

            <p className="text-[var(--text-light)] font-medium">
                Financial Health
            </p>

            <div className="mt-6 relative w-40 h-40 flex items-center justify-center">

                <svg
                    height={radius * 2}
                    width={radius * 2}
                    className="-rotate-90"
                >

                    {/* Background track */}
                    <circle
                        stroke="var(--border)"
                        fill="transparent"
                        strokeWidth={stroke}
                        r={normalizedRadius}
                        cx={radius}
                        cy={radius}
                    />

                    {/* Progress arc -- length reflects the actual score */}
                    <circle
                        stroke={ringColor}
                        fill="transparent"
                        strokeWidth={stroke}
                        strokeLinecap="round"
                        strokeDasharray={`${circumference} ${circumference}`}
                        style={{
                            strokeDashoffset,
                            transition: "stroke-dashoffset 0.6s ease",
                        }}
                        r={normalizedRadius}
                        cx={radius}
                        cy={radius}
                    />

                </svg>

                <div className="absolute inset-0 flex flex-col items-center justify-center">

                    <h1 className="text-5xl font-bold">
                        {score}
                    </h1>

                    <p className="text-sm text-[var(--text-light)]">
                        {grade}
                    </p>

                </div>

            </div>

            <p
                className={`mt-6 font-semibold ${
                    score >= 80
                        ? "text-green-600"
                        : score >= 60
                        ? "text-yellow-500"
                        : "text-red-500"
                }`}
            >
                {status}
            </p>

        </Card>
    );
}