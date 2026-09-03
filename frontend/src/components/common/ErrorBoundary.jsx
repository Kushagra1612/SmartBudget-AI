import { Component } from "react";

// Error boundaries have no hook equivalent -- this has to be a class
// component. Catches render-time errors anywhere below it in the tree
// and shows a recoverable message instead of leaving a blank page with
// no way back in.
export default class ErrorBoundary extends Component {

    constructor(props) {

        super(props);

        this.state = {
            hasError: false,
        };

    }

    static getDerivedStateFromError() {

        return {
            hasError: true,
        };

    }

    componentDidCatch(error, info) {

        console.error("Uncaught error:", error, info);

    }

    render() {

        if (this.state.hasError) {

            return (

                <div
                    style={{
                        minHeight: "100vh",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        background: "var(--bg)",
                        padding: "24px",
                    }}
                >

                    <div
                        style={{
                            maxWidth: "420px",
                            textAlign: "center",
                            background: "var(--surface)",
                            borderRadius: "var(--radius)",
                            boxShadow: "var(--shadow)",
                            padding: "40px",
                        }}
                    >

                        <h1
                            style={{
                                fontSize: "22px",
                                fontWeight: 700,
                                color: "var(--text)",
                            }}
                        >
                            Something went wrong
                        </h1>

                        <p
                            style={{
                                marginTop: "12px",
                                color: "var(--text-light)",
                            }}
                        >
                            This page hit an unexpected error. Reloading usually fixes it.
                        </p>

                        <button
                            onClick={() => window.location.reload()}
                            style={{
                                marginTop: "24px",
                                background: "var(--primary)",
                                color: "#fff",
                                border: "none",
                                borderRadius: "12px",
                                padding: "12px 28px",
                                fontWeight: 600,
                                cursor: "pointer",
                            }}
                        >
                            Reload
                        </button>

                    </div>

                </div>

            );

        }

        return this.props.children;

    }

}
