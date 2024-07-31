// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword ,signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/10.12.1/firebase-auth.js";
import {getFirestore , doc, setDoc } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-firestore.js"; 


// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDuxAtaRH6IZ2MeYFA3R6xrQ_5oEhGkV9I",
  authDomain: "dscp-236a9.firebaseapp.com",
  projectId: "dscp-236a9",
  storageBucket: "dscp-236a9.appspot.com",
  messagingSenderId: "883956853164",
  appId: "1:883956853164:web:d365713d2bae66925bf209"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
console.log("Firestore initialized:", db);

// Register button
const register = document.getElementById('register');
register.addEventListener('click', async (e) => {
    e.preventDefault();
    console.log('Register clicked');

    // Inputs
    const username = document.getElementById('reg_username').value;
    const reg_email = document.getElementById('reg_email').value;
    const reg_password = document.getElementById('reg_password').value;
    console.log('Username:', username);
    console.log('Email:', reg_email);

    try {
        const userCredential = await createUserWithEmailAndPassword(auth, reg_email, reg_password);
        const user = userCredential.user;
        console.log('User created:', user);

        await setDoc(doc(db, "users", user.uid), {
            username: username,
            email: reg_email
        });

        console.log('User data stored in Firestore');
        alert("User created and data saved to Firestore");
        window.location.href = "LoggedIn.html";
    } catch (error) {
        console.error('Error:', error);
        alert("Error: " + error.message);
    }
});

// Login button
const login = document.getElementById('login');
login.addEventListener('click', async (e) => {
    e.preventDefault();
    console.log('Login clicked');

    // Inputs
    const login_email = document.getElementById('login_email').value;
    const login_password = document.getElementById('login_password').value;
    console.log('Login Email:', login_email);

    try {
        const userCredential = await signInWithEmailAndPassword(auth, login_email, login_password);
        const user = userCredential.user;
        console.log('User logged in:', user);
        alert("Logged in");
        window.location.href = "loggedIn.html";
    } catch (error) {
        console.error('Error:', error);
        alert("Error: " + error.message);
    }
});