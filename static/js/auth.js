// -----------------------------
// Firebase Auth Helper Functions
// -----------------------------

// SIGN UP FUNCTION
async function signup(email, password, displayName) {
  try {
    const res = await firebase.auth().createUserWithEmailAndPassword(email, password);
    const user = res.user;

    await user.updateProfile({ displayName });

    const idToken = await user.getIdToken();

    // Send user to backend
    const response = await fetch('/api/save_user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + idToken
      },
      body: JSON.stringify({
        email: user.email,
        displayName: displayName
      })
    });

    if (!response.ok) {
      const msg = await response.text();
      alert("Backend error: " + msg);
      return;
    }

    window.location.href = '/dashboard';

  } catch (err) {
    alert(err.message);
  }
}


// LOGIN FUNCTION
async function login(email, password) {
  try {
    const res = await firebase.auth().signInWithEmailAndPassword(email, password);
    window.location.href = "/dashboard";
  } catch (err) {
    alert(err.message);
  }
}


// LOGOUT FUNCTION
function logout() {
  firebase.auth().signOut().then(() => {
    window.location.href = "/login";
  });
}


// AUTH STATE LISTENER
function onAuthState(callback) {
  firebase.auth().onAuthStateChanged((user) => {
    callback(user);
  });
}
