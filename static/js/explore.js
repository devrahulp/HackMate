console.log("Explore JS loaded");

const container = document.getElementById("profilesContainer");

// TEMP hardcoded profiles
const demoProfiles = [
    { name: "Alice", skills: "Python, Flask" },
    { name: "Bob", skills: "React, Node" }
];

demoProfiles.forEach(user => {
    const card = document.createElement("div");
    card.className = "profile-card";
    card.innerHTML = `
        <h3>${user.name}</h3>
        <p>Skills: ${user.skills}</p>
    `;
    container.appendChild(card);
});

document.getElementById("backBtn").onclick = () => {
    window.location.href = "/";
};