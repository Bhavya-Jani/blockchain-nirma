import { useEffect, useState } from "react";

const WalletList = () => {
    const [wallets, setWallets] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/wallets/") // Django API URL
            .then(response => response.json())
            .then(data => setWallets(data))
            .catch(error => console.error("Error fetching wallets:", error));
    }, []);

    return (
        <div>
            <h2>Available Wallets</h2>
            <ul>
                {wallets.map(wallet => (
                    <li key={wallet.id}>{wallet.name} - {wallet.network}</li>
                ))}
            </ul>
        </div>
    );
};

export default WalletList;
