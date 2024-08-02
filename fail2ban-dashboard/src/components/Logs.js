import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Logs = () => {
    const [logs, setLogs] = useState([]);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        axios.get('http://localhost:5000/api/logs')
            .then(response => {
                setLogs(response.data);
            })
            .catch(error => console.error('Erreur lors de la récupération des logs:', error));
    }, []);

    const handleChange = (e) => {
        setFilter(e.target.value);
    };

    const filteredLogs = logs.filter(log => log.ip.includes(filter));

    return (
        <div>
            <h1>Logs et Historique</h1>
            <input
                type="text"
                placeholder="Filtrer par IP"
                value={filter}
                onChange={handleChange}
            />
            <ul>
                {filteredLogs.map(log => (
                    <li key={log.id}>
                        {log.timestamp} - {log.ip} - {log.action}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Logs;
