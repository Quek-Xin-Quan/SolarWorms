// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/10.12.1/firebase-auth.js";


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


//Login button
const login = document.getElementById('login');
login.addEventListener('click', (e) => {
    e.preventDefault();
    console.log('login clicked');
    //inputs
    const reg_email = document.getElementById('login_email').value;
    const reg_password = document.getElementById('login_password').value;
    signInWithEmailAndPassword(auth, login_email, login_password)
    .then((userCredential) => {
        // Signed up 
        const user = userCredential.user;
        alert("Logged in");
        window.location.href = "LoggedIn.html";
        // ...
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        alert("Error") ;
        // ..
    });

});