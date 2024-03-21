import React, { useState } from 'react';
import Login from './service/Login.js';
import Signup from './service/Signup.js';
import axios from 'axios';

function App() {
  const [showLogin, setShowLogin] = useState(true);

  const handleToggleForm = () => {
    setShowLogin(prevState => !prevState);
  };

  const handleLoginSubmit = async (formData) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/user/login', formData);
      console.log('Login Response:', response.data);

    } catch (error) {
      console.error('Login Error:', error);

    }
  };

  const handleSignupSubmit = async (formData) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/user/signup', formData);
      console.log('Signup Response:', response.data);

    } catch (error) {
      console.error('Signup Error:', error);

    }
  };

  return (
    <div className="App">
      <h1>Página inicial</h1>
      {showLogin ? (
        <Login onSubmit={handleLoginSubmit} />
      ) : (
        <Signup onSubmit={handleSignupSubmit} />
      )}

      <div>
        <button onClick={handleToggleForm}>
          {showLogin ? "Criar conta" : "Fazer login"}
        </button>
      </div>
    </div>
  );
}

export default App;
