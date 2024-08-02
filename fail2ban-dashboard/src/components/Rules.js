import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Rules = () => {
    const [rules, setRules] = useState([]);
    const [newRule, setNewRule] = useState({ ip: '', attempts: '', duration: '' });

    useEffect(() => {
        axios.get('http://localhost:5000/api/rules')
            .then(response => {
                setRules(response.data);
            })
            .catch(error => console.error('Erreur lors de la récupération des règles:', error));
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewRule({ ...newRule, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://localhost:5000/api/rules', newRule)
            .then(response => {
                setRules([...rules, response.data]);
                setNewRule({ ip: '', attempts: '', duration: '' });
            })
            .catch(error => console.error('Erreur lors de l\'ajout de la règle:', error));
    };

    const handleDelete = (id) => {
        axios.delete(`http://localhost:5000/api/rules/${id}`)
            .then(() => {
                setRules(rules.filter(rule => rule.id !== id));
            })
            .catch(error => console.error('Erreur lors de la suppression de la règle:', error));
    };

    return (
        <div>
            <h1>Gestion des Règles</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="ip"
                    placeholder="IP"
                    value={newRule.ip}
                    onChange={handleChange}
                />
                <input
                    type="number"
                    name="attempts"
                    placeholder="Tentatives"
                    value={newRule.attempts}
                    onChange={handleChange}
                />
                <input
                    type="number"
                    name="duration"
                    placeholder="Durée (minutes)"
                    value={newRule.duration}
                    onChange={handleChange}
                />
                <button type="submit">Ajouter</button>
            </form>
            <ul>
                {rules.map(rule => (
                    <li key={rule.id}>
                        {rule.ip} - {rule.attempts} tentatives - {rule.duration} minutes
                        <button onClick={() => handleDelete(rule.id)}>Supprimer</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Rules;
