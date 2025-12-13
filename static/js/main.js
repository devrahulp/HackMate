<<<<<<< HEAD
console.log("HackMate Home Loaded");
=======
async function loadProfiles() {
    try {
        const res = await fetch("/api/profiles");
        const profiles = await res.json();

        console.log("Profiles loaded:", profiles); // DEBUG

        const container = document.getElementById("profilesContainer");
        container.innerHTML = "";

        if (!profiles.length) {
            container.innerHTML = "<p>No profiles found.</p>";
            return;
        }

        profiles.forEach(user => {
            const card = document.createElement("div");
            card.className = "profile-card";

            card.innerHTML = `
                <img src="${user.profile_pic_url || 'https://i.pravatar.cc/150'}">
                <h3>${user.name || "Anonymous"}</h3>
                <p>Skills: ${(user.skills || []).join(", ")}</p>
                <button class="btn-primary" onclick="viewProfile('${user.uid}')">
                    View Profile
                </button>
            `;

            container.appendChild(card);
        });
    } catch (err) {
        console.error("Failed to load profiles:", err);
    }
}

function viewProfile(uid) {
    alert("View profile: " + uid);
}

document.addEventListener("DOMContentLoaded", loadProfiles);
>>>>>>> d704920af0694b0bc13572e0b351b8c3399ccc6d
