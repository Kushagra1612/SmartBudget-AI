import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import LoginForm from "../../components/auth/LoginForm";
import { AuthProvider } from "../../context/AuthContext";
import { login, getProfile } from "../../api/auth";
import toast from "react-hot-toast";

const { mockNavigate } = vi.hoisted(() => ({
    mockNavigate: vi.fn(),
}));

vi.mock("react-router-dom", async (importOriginal) => {
    const actual = await importOriginal();
    return {
        ...actual,
        useNavigate: () => mockNavigate,
    };
});

vi.mock("../../api/auth", () => ({
    login: vi.fn(),
    getProfile: vi.fn(),
}));

vi.mock("react-hot-toast", () => ({
    default: {
        error: vi.fn(),
        success: vi.fn(),
    },
}));

function renderLoginForm() {

    return render(
        <MemoryRouter>
            <AuthProvider>
                <LoginForm />
            </AuthProvider>
        </MemoryRouter>
    );

}

describe("LoginForm", () => {

    beforeEach(() => {

        vi.clearAllMocks();
        localStorage.clear();

    });

    it("renders email and password fields and a submit button", () => {

        renderLoginForm();

        expect(screen.getByPlaceholderText("Email")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Password")).toBeInTheDocument();
        expect(screen.getByRole("button", { name: "Login" })).toBeInTheDocument();

    });

    it("on success: stores tokens, fetches the profile, and navigates to the dashboard", async () => {

        const user = userEvent.setup();

        login.mockResolvedValue({
            data: { access_token: "abc123", token_type: "bearer" },
        });

        getProfile.mockResolvedValue({
            data: { id: "1", full_name: "Ada Lovelace", email: "ada@example.com" },
        });

        renderLoginForm();

        await user.type(screen.getByPlaceholderText("Email"), "ada@example.com");
        await user.type(screen.getByPlaceholderText("Password"), "hunter2222");
        await user.click(screen.getByRole("button", { name: "Login" }));

        await waitFor(() => {
            expect(mockNavigate).toHaveBeenCalledWith("/dashboard");
        });

        expect(login).toHaveBeenCalledWith({
            email: "ada@example.com",
            password: "hunter2222",
        });
        expect(localStorage.getItem("access_token")).toBe("abc123");
        expect(localStorage.getItem("token_type")).toBe("bearer");
        expect(getProfile).toHaveBeenCalled();

    });

    it("on failure: shows the server's error message and does not navigate", async () => {

        const user = userEvent.setup();

        login.mockRejectedValue({
            response: { data: { detail: "Incorrect email or password." } },
        });

        renderLoginForm();

        await user.type(screen.getByPlaceholderText("Email"), "ada@example.com");
        await user.type(screen.getByPlaceholderText("Password"), "wrongpassword");
        await user.click(screen.getByRole("button", { name: "Login" }));

        await waitFor(() => {
            expect(toast.error).toHaveBeenCalledWith("Incorrect email or password.");
        });

        expect(mockNavigate).not.toHaveBeenCalled();
        expect(localStorage.getItem("access_token")).toBe(null);

    });

    it("falls back to a generic message when the server gives no detail", async () => {

        const user = userEvent.setup();

        login.mockRejectedValue(new Error("network down"));

        renderLoginForm();

        await user.type(screen.getByPlaceholderText("Email"), "ada@example.com");
        await user.type(screen.getByPlaceholderText("Password"), "hunter2222");
        await user.click(screen.getByRole("button", { name: "Login" }));

        await waitFor(() => {
            expect(toast.error).toHaveBeenCalledWith("Login failed");
        });

    });

});
