import { useState } from 'react';

export default function LearnerProfile({ onComplete }) {
    const [profile, setProfile] = useState({
        name: '',
        level_of_education: 'highschool',
        school_name: ''
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch('http://localhost:8000/profiles/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profile)
            });
            const data = await res.json();
            onComplete(data);
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-16 bg-white p-8 rounded-2xl shadow-xl ring-1 ring-gray-900/5">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 font-inter">Let's get started</h2>
            <p className="text-gray-500 mb-8 font-inter">Tell us a bit about yourself to personalize your study experience.</p>

            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label className="block text-sm font-medium text-gray-700 font-inter">What's your name?</label>
                    <input
                        type="text"
                        required
                        className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 font-inter"
                        value={profile.name}
                        onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 font-inter">Education Level</label>
                    <select
                        className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 font-inter"
                        value={profile.level_of_education}
                        onChange={(e) => setProfile({ ...profile, level_of_education: e.target.value })}
                    >
                        <option value="highschool">High School</option>
                        <option value="college">College / Graduate</option>
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 font-inter">School Name</label>
                    <input
                        type="text"
                        required
                        className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 font-inter"
                        value={profile.school_name}
                        onChange={(e) => setProfile({ ...profile, school_name: e.target.value })}
                    />
                </div>

                <button
                    type="submit"
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-brand-600 hover:bg-brand-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-colors font-inter"
                >
                    Start Studying
                </button>
            </form>
        </div>
    );
}
