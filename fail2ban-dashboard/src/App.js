import React from 'react';
import { BrowserRouter as Router, Route, Routes  } from 'react-router-dom';

import Dashboard from './components/Dashboard';
import Rules from './components/Rules';
import Logs from './components/Logs';

const App = () => {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/rules" element={<Rules />} />
                    <Route path="/logs" element={<Logs />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;