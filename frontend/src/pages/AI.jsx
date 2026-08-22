import { useState } from "react";

import MainLayout from "../layouts/MainLayout";

import { chat } from "../api/ai";

import ChatHeader from "../components/ai/ChatHeader";
import FinancialAdvice from "../components/ai/FinancialAdvice";
import SuggestedQuestions from "../components/ai/SuggestedQuestions";
import ChatWindow from "../components/ai/ChatWindow";
import ChatInput from "../components/ai/ChatInput";

export default function AI() {

    const currentDate = new Date();

    const [message, setMessage] = useState("");

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    async function handleSend(customMessage = message) {

        if (!customMessage.trim()) {
            return;
        }

        setMessages((prev) => [

            ...prev,

            {
                role: "user",
                text: customMessage,
            },

        ]);

        setLoading(true);

        try {

            const response = await chat(

                customMessage,

                currentDate.getMonth() + 1,

                currentDate.getFullYear(),

            );

            setMessages((prev) => [

                ...prev,

                {
                    role: "assistant",
                    text: response.response,
                    agentsUsed: response.agents_used,
                },

            ]);

        } catch {

            setMessages((prev) => [

                ...prev,

                {
                    role: "assistant",
                    text: "Unable to contact SmartBudget AI.",
                },

            ]);

        } finally {

            setLoading(false);

            setMessage("");

        }

    }

    return (

        <MainLayout>

            <ChatHeader />

            <FinancialAdvice />

            <SuggestedQuestions
                onSelect={handleSend}
            />

            <ChatWindow
                messages={messages}
            />

            <ChatInput
                message={message}
                setMessage={setMessage}
                loading={loading}
                onSend={handleSend}
            />

        </MainLayout>

    );

}