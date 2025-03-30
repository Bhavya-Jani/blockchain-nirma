import React, { useState } from "react";
import { ethers } from "ethers";

const WalletConnection = () => {
  const [selectedNetwork, setSelectedNetwork] = useState("ethereum");
  const [walletAddress, setWalletAddress] = useState("");

  const connectWallet = async () => {
    if (selectedNetwork === "ethereum" || selectedNetwork === "polygon" || selectedNetwork === "base") {
      if (!window.ethereum) {
        alert("MetaMask is not installed!");
        return;
      }

      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const accounts = await provider.send("eth_requestAccounts", []);
        setWalletAddress(accounts[0]);
      } catch (error) {
        console.error("Error connecting to MetaMask:", error);
      }
    } 
    
    else if (selectedNetwork === "solana") {
      if (!window.phantom) {
        alert("Phantom Wallet is not installed!");
        return;
      }

      try {
        const solana = window.phantom.solana;
        const response = await solana.connect();
        setWalletAddress(response.publicKey.toString());
      } catch (error) {
        console.error("Error connecting to Phantom:", error);
      }
    }

    else if (selectedNetwork === "starknet") {
      if (!window.argentX) {
        alert("ArgentX Wallet is not installed!");
        return;
      }

      try {
        const starknet = window.argentX;
        const response = await starknet.enable();
        setWalletAddress(response[0]);
      } catch (error) {
        console.error("Error connecting to ArgentX:", error);
      }
    }
  };

  return (
    <div className="flex flex-col items-center bg-gray-900 text-white p-6 rounded-2xl shadow-lg max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4">Connect Your Wallet</h2>
      
      <select 
        className="mb-4 p-2 bg-gray-800 text-white rounded-lg border border-gray-600 focus:ring-2 focus:ring-blue-500"
        onChange={(e) => setSelectedNetwork(e.target.value)}
      >
        <option value="ethereum">Ethereum (MetaMask)</option>
        <option value="polygon">Polygon (MetaMask)</option>
        <option value="solana">Solana (Phantom)</option>
        <option value="starknet">StarkNet (ArgentX)</option>
        <option value="base">Base (MetaMask)</option>
      </select>

      <button 
        onClick={connectWallet} 
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-all"
      >
        Connect Wallet
      </button>

      {walletAddress && (
        <p className="mt-4 bg-gray-800 p-2 rounded-lg border border-gray-600 text-center">
          Connected: {walletAddress}
        </p>
      )}
    </div>
  );
};

export default WalletConnection;
