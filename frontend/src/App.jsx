import { useState } from 'react'
import LearnerProfile from './components/LearnerProfile'
import ChatInterface from './components/ChatInterface'

function App() {
    const [profile, setProfile] = useState(null)
    const [session, setSession] = useState(null)

    const handleProfileComplete = async (profileData) => {
        setProfile(profileData)
        // Auto-create a default session to jump right in
        try {
            const res = await fetch('http://localhost:8000/sessions/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    learner_id: profileData.id,
                    course_name: "General Study",
                    topic: "New Session",
                    session_duration_minutes: 60
                })
            });
            const sessionData = await res.json();

            // Need to format how the ChatInterface expects it
            setSession({
                session: sessionData,
                history: []
            });
        } catch (e) {
            console.error(e)
        }
    }

    const handleNewSession = () => {
        setSession(null); // Simple reset, would normally show a modal to name the new session
        handleProfileComplete(profile); // Re-trigger default session creation
    }

    return (
        <div className="min-h-screen bg-surface-muted selection:bg-brand-100 selection:text-brand-900">
            {!profile ? (
                <LearnerProfile onComplete={handleProfileComplete} />
            ) : !session ? (
                <div className="flex h-screen items-center justify-center">
                    <div className="animate-pulse text-brand-600 font-medium">Setting up your study session...</div>
                </div>
            ) : (
                <ChatInterface session={session} onNewSession={handleNewSession} />
            )}
        </div>
    )
}

export default App
