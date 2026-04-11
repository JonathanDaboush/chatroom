import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import RoomsPage from './pages/RoomsPage';
import RoomPage from './pages/RoomPage';
import CallPage from './pages/CallPage';
import './App.css';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected Routes */}
        <Route path="/app" element={<AppLayout />}>
          <Route index element={<Navigate to="/app/rooms" replace />} />
          <Route path="rooms" element={<RoomsPage />} />
          <Route path="room/:id" element={<RoomPage />} />
          <Route path="call/:id" element={<CallPage />} />
        </Route>
        
        {/* Default Redirect */}
        <Route path="*" element={<Navigate to="/app/rooms" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
