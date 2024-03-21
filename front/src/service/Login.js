import React, { useState } from 'react';
import axios from 'axios';

const Loguin = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = event => {
    const { name, value } = event.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async event => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/user/signup', formData);
      console.log('Response:', response.data);
      
    } catch (error) {
      console.error('Error:', error);
      
    }
  };

  return (
    <div>
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
};

export default Loguin;
