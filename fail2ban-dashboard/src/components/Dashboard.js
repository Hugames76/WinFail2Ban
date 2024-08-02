import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import Chart from 'chart.js/auto';

const Dashboard = () => {
    const [data, setData] = useState({
        labels: [],
        datasets: [
            {
                label: 'Tentatives échouées',
                data: [],
                backgroundColor: 'rgba(255,99,132,0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1,
            },
            {
                label: 'Tentatives totales',
                data: [],
                backgroundColor: 'rgba(54,162,235,0.2)',
                borderColor: 'rgba(54,162,235,1)',
                borderWidth: 1,
            },
        ],
    });

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [combinedData, setCombinedData] = useState({});
    const chartRef = useRef(null);
    const chartInstanceRef = useRef(null);

    useEffect(() => {
        axios.get('http://localhost:5000/api/dashboard')
            .then(response => {
                const { failed_attempts, total_attempts } = response.data;
                
                // Combine data
                const combined = {};
                for (const [ip, details] of Object.entries(failed_attempts)) {
                    if (!combined[ip]) {
                        combined[ip] = { failed: 0, total: 0, lastTimestamp: details.lastTimestamp };
                    }
                    combined[ip].failed += details.count;
                    if (total_attempts[ip]) {
                        combined[ip].total = total_attempts[ip].count;
                    }
                    if (new Date(details.lastTimestamp) > new Date(combined[ip].lastTimestamp)) {
                        combined[ip].lastTimestamp = details.lastTimestamp;
                    }
                }

                const labels = Object.keys(combined).map(ip => `${ip} (${combined[ip].lastTimestamp})`);
                const failedAttemptsData = Object.values(combined).map(item => item.failed);
                const totalAttemptsData = Object.values(combined).map(item => item.total);

                setCombinedData(combined);
                setData({
                    labels,
                    datasets: [
                        {
                            label: 'Tentatives échouées',
                            data: failedAttemptsData,
                            backgroundColor: 'rgba(255,99,132,0.2)',
                            borderColor: 'rgba(255,99,132,1)',
                            borderWidth: 1,
                        },
                        {
                            label: 'Tentatives totales',
                            data: totalAttemptsData,
                            backgroundColor: 'rgba(54,162,235,0.2)',
                            borderColor: 'rgba(54,162,235,1)',
                            borderWidth: 1,
                        },
                    ],
                });
                setIsLoading(false);
            })
            .catch(error => {
                setError(error);
                setIsLoading(false);
            });
    }, []);

    useEffect(() => {
        if (chartRef.current && !chartInstanceRef.current && !isLoading) {
            const ctx = chartRef.current.getContext('2d');
            chartInstanceRef.current = new Chart(ctx, {
                type: 'bar',
                data,
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            beginAtZero: true,

                        },
                        y: {
                            beginAtZero: true,
                        }
                    }
                }
            });
        }
    }, [data, isLoading]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div>
            <h1>Tableau de Bord</h1>
            <div className="chart-container">
                <canvas ref={chartRef} id="dashboard"></canvas>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>IP</th>
                        <th>Dernier Timestamp</th>
                        <th>Nombre de tentatives échouées</th>
                        <th>Nombre de tentatives totales</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.keys(combinedData).map((ip, index) => (
                        <tr key={index}>
                            <td>{ip}</td>
                            <td>{combinedData[ip].lastTimestamp}</td>
                            <td>{combinedData[ip].failed}</td>
                            <td>{combinedData[ip].total}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Dashboard;