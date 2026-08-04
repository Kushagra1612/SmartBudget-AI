export default function DashboardGrid({ children }) {
    return (
        <div
            className="
                grid
                grid-cols-12
                gap-6
                mt-8
            "
        >
            {children}
        </div>
    );
}