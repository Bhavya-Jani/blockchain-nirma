import React from "react";
import WalletConnection from "./components/WalletConnection";
import WalletList from "./WalletList"; // Import the WalletList component


function App() {
    return (
      <div>
            <h1 style={{ textAlign: "center" }}>Blockchain Wallet Demo</h1>
            <WalletConnection />
        </div>
    );
}

export default App;