import React from 'react';
import { useParams } from 'react-router-dom';
import CallPanel from '@/components/call/CallPanel';
import './CallPage.css';

const CallPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="call-page">
      <div className="call-page-content">
        <h1>Call in Progress</h1>
        <p>Call ID: {id}</p>
      </div>
      <CallPanel />
    </div>
  );
};

export default CallPage;
